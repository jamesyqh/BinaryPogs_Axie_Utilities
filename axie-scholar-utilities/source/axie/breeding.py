import sys
import json
import asyncio
import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from web3 import Web3, exceptions

from axie.schemas import breeding_schema
from axie.utils import get_nonce, load_json, RONIN_PROVIDER_FREE, AXIE_CONTRACT, check_balance
from axie.payments import Payment, PaymentsSummary, CREATOR_FEE_ADDRESS


class Breed:
    def __init__(self, sire_axie, matron_axie, address, private_key, nonce=None):
        self.w3 = Web3(Web3.HTTPProvider(RONIN_PROVIDER_FREE))
        self.sire_axie = sire_axie
        self.matron_axie = matron_axie
        self.address = address.replace("ronin:", "0x")
        self.private_key = private_key
        if not nonce:
            self.nonce = get_nonce(self.address)
        else:
            self.nonce = max(get_nonce(self.address), nonce)

    def execute(self):
        # Prepare transaction
        with open("axie/axie_abi.json") as f:
            axie_abi = json.load(f)
        axie_contract = self.w3.eth.contract(
            address=Web3.toChecksumAddress(AXIE_CONTRACT),
            abi=axie_abi
        )
        # Build transaction
        transaction = axie_contract.functions.breedAxies(
            self.sire_axie,
            self.matron_axie
        ).buildTransaction({
            "chainId": 2020,
            "gas": 500000,
            "gasPrice": self.w3.toWei("0", "gwei"),
            "nonce": self.nonce
        })
        # Sign transaction
        signed = self.w3.eth.account.sign_transaction(
            transaction,
            private_key=self.private_key
        )
        # Send raw transaction
        self.w3.eth.send_raw_transaction(signed.rawTransaction)
        # get transaction hash
        hash = self.w3.toHex(self.w3.keccak(signed.rawTransaction))
        # Wait for transaction to finish
        logging.info("{self} about to start!")
        try:
            recepit = self.w3.eth.wait_for_transaction_receipt(hash, timeout=300, poll_latency=5)
        except exceptions.TimeExhausted:
            logging.info("{self}, Transaction could not be processed within 5min, skipping it!")

        if recepit['status'] == 1:
            logging.info("Important: {self} completed successfully")
        else:
            logging.info("Important: {self} failed")

    def __str__(self):
        return (f"Breeding axie {self.sire_axie} with {self.matron_axie} in account "
                f"{self.address.replace('0x', 'ronin:')}")


class AxieBreedManager:

    def __init__(self, breeding_file, secrets_file, payment_account):
        self.secrets = load_json(secrets_file)
        self.breeding_file = load_json(breeding_file)
        self.payment_account = payment_account
        self.breeding_costs = 0

    def verify_inputs(self):
        validation_error = False
        logging.info("Validating file inputs...")
        try:
            validate(self.breeding_file, breeding_schema)
        except ValidationError as ex:
            logging.critical(f'Validation of breeding file failed. Error given: {ex.message}\n'
                             f'For attribute in: {list(ex.path)}')
            validation_error = True
        for acc in self.breeding_file:
            if acc['AccountAddress'] not in self.secrets:
                logging.critical(f"Account '{acc['AccountAddress']}' is not present in secret file, please add it.")
                validation_error = True
        if self.payment_account not in self.secrets:
            logging.critical(f"Payment account '{self.payment_account}' is not present in secret file, please add it.")
            validation_error = True
        if validation_error:
            sys.exit()

    def calculate_cost(self):
        return self.calculate_fee_cost() + self.breeding_costs

    def calculate_breeding_cost(self):
        # TODO: We need to calculate how much will all breeding cost, pending for the future!
        return 0

    def calculate_fee_cost(self):
        number_of_breeds = len(self.breeding_file)
        if number_of_breeds <= 15:
            cost = number_of_breeds * 30
        if 15 < number_of_breeds <= 30:
            cost = (15 * 30) + ((number_of_breeds - 15) * 25)
        if 30 < number_of_breeds <= 50:
            cost = (15 * 30) + (15 * 25) + ((number_of_breeds - 30) * 20)
        if number_of_breeds > 50:
            cost = (15 * 30) + (15 * 25) + (20 * 20) + ((number_of_breeds - 50) * 15)
        return cost

    def execute(self):
        if check_balance(self.payment_account) < self.calculate_cost():
            logging.critical("Not enough SLP funds to pay for breeding and the fee")
            sys.exit()

        logging.info("About to start breeding axies")
        for bf in self.breeding_file:
            b = Breed(
                sire_axie=bf['Sire'],
                matron_axie=bf['Matron'],
                address=bf['AccountAddress'],
                private_key=self.secrets[bf['AccountAddress']]
            )
            b.execute()
        logging.info("Done breeding axies")
        fee = self.calculate_fee_cost()
        logging.info(f"Time to pay the fee for breeding. For this session it is: {fee} SLP")
        p = Payment(
            "Breeding Fee",
            "donation",
            self.payment_account,
            self.secrets[self.payment_account],
            CREATOR_FEE_ADDRESS,
            fee,
            PaymentsSummary()
        )
        p.execute()
