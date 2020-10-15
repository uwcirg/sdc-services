Structured Data Capture Services
================================
Implementation of select services and features from [FHIR SDC Implementation Guide](https://build.fhir.org/ig/HL7/sdc/)


Development
-----------
To start the application follow the below steps in the checkout root

Copy default environment variable file and modify as necessary

    cp sdc_services.env.default sdc_services.env

Build the docker image. Should only be necessary on first run or if dependencies change.

    docker-compose build

Start the container in detached mode

    docker-compose up --detach

Read application logs

    docker-compose logs --follow


Test
----
This project uses tox to manage testing environments. To trigger a test run, invoke `tox` without arguments:
    tox

License
-------
BSD
