# Install Using Docker On MacOs

# Install Docker
Best thing I can do for this bit is send you to follow the instructions in the official docker documentation.

- [Docker on Mac](https://docs.docker.com/desktop/mac/install/)


# Use the image from docker-hub

Every successful build of my code produces a Docker image that is stored [here](https://hub.docker.com/r/epith/axie-scholar-utilities).

After you've downloaded docker, you simply need to execute this command to download the latest image:

    docker pull epith/axie-scholar-utilities

If you go this route, I recomend also setting up these alias in your terminal to execute commands easier:

    # Alias to generate secrets
        axie-utils-gen-secrets() {docker run -it -v ${PWD}/${1}:/opt/app/files/payments.json -v ${PWD}/${2}:/opt/app/files/secrets.json epith/axie-scholar-utilities generate_secrets files/payments.json files/secrets.json}
    # Alias to generate payments
        axie-utils-gen-payments() {docker run -it -v ${PWD}/${1}:/opt/app/files/payments.csv -v ${PWD}/${2}:/opt/app/files/payments.json epith/axie-scholar-utilities generate_payments files/payments.csv files/payments.json}
    # Alias to mass update secrets
        axie-utils-mass-update() {docker run -it -v ${PWD}/${1}:/opt/app/files/update.csv -v ${PWD}/${2}:/opt/app/files/secrets.json epith/axie-scholar-utilities mass_update_secrets files/update.csv files/secrets.json}
    # Alias to execute claims
        axie-utils-claim() {docker run -it -v ${PWD}/${1}:/opt/app/files/payments.json -v ${PWD}/${2}:/opt/app/files/secrets.json epith/axie-scholar-utilities claim files/payments.json files/secrets.json}
    # Alias to execute payments
        axie-utils-payout() {docker run -it -v ${PWD}/${1}:/opt/app/files/payments.json  -v ${PWD}/${2}:/opt/app/files/secrets.json -v ${PWD}/${3}:/opt/app/results.log epith/axie-scholar-utilities payout files/payments.json files/secrets.json}
    # Alias to execute auto-payments (no confirmation)
        axie-utils-auto-payout() {docker run -it -v ${PWD}/${1}:/opt/app/files/payments.json -v ${PWD}/${2}:/opt/app/files/secrets.json -v ${PWD}/${3}:/opt/app/results.log epith/axie-scholar-utilities payout files/payments.json files/secrets.json -y}
    # Alias to execute axie transfers
        axie-utils-transfer-axies() {docker run -it -v ${PWD}/${1}:/opt/app/files/transfers.json -v ${PWD}/${2}:/opt/app/files/secrets.json epith/axie-scholar-utilities transfer_axies files/transfers.json files/secrets.json}
    #Alias to generate transfers file
        axie-utils-gen-transfers() {docker run -it -v ${PWD}/${1}:/opt/app/files/transfers.csv -v ${PWD}/${2}:/opt/app/files/transfers.json epith/axie-scholar-utilities generate_transfer_axies files/transfers.csv files/transfers.json}
    # Alias to execute generate_qr
        axie-utils-gen-QR() {docker run -it -v ${PWD}/${1}:/opt/app/files/payments.json -v ${PWD}/${2}:/opt/app/files/secrets.json -v ${PWD}:/opt/app/files epith/axie-scholar-utilities generate_QR files/payments.json files/secrets.json}
    #Alias to generate breedings file
        axie-utils-gen-breedings() {docker run -it -v ${PWD}/${1}:/opt/app/files/breedings.csv -v ${PWD}/${2}:/opt/app/files/breedings.json epith/axie-scholar-utilities generate_breedings files/breedings.csv files/breedings.json}
    # Alias to breed axies
        axie-utils-axie-breeding() {docker run -it -v ${PWD}/${1}:/opt/app/files/breedings.json -v ${PWD}/${2}:/opt/app/files/secrets.json epith/axie-scholar-utilities axie_breeding files/breedings.json files/secrets.json}
    # Alias to morph axies
        axie-utils-axie-morphing() {docker run -it -v ${PWD}/${1}:/opt/app/files/secrets.json epith/axie-scholar-utilities axie_morphing files/secrets.json}


To learn how to run the commands, please follow this [link](../pages/docker_hub_cmds.html)


# Build docker image from repository

If you do not want to rely on the image I provide on docker hub, you can build it from the repository.
To do that, first you need to download my code, either download it as a zip and unzip it, or git clone it (whatever is easier for you).

After that, navigate using your terminal to the [docker folder](axie-scholar-utilities/docker).Once there create a folder named **files** (this is where we will place our payments and secret file and a file called results.log which is empty), we will link that folder from our host to the docker container.

Once we reach this point. Use the following command to build the docker image:

    docker-compose build scholar-utilities

To learn how to run the commands, please follow this [link](../pages/docker_compose_cmds.html)
