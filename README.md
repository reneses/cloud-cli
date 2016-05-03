# Cloud CLI
This program eases the automatition and management of cloud infrastructures, using the libraries **Boto** and
**Libcloud** to operate with **Amazon Web Services** and **OpenStack**, specifically with:

- AWS Elastic Cloud Computing (EC2)
- AWS Simple Storage Service (S3)
- AWS WatchCloud and Simple Notification Service (SNS)
- AWS Elastic Load Balancer (ELB)
- AWS CloudFormation
- OpenStack computing services
- OpenStack Swift storage services

Developed by [Álvaro Reneses](http://www.reneses.io).

## Disclaimer

This repository is an autonomous assignment part of the **Cloud Computing with Python** module offered by the [CIT](http://www.cit.ie). The original specifications of the assignment are included in the `assignment.pdf` file.

Due to the time limitations of the assignment and the guidelines it had to follow, this repository should be used as a sample or proof of concept, rather than for production purposes.

## Requirements

- Python 2.7
- Boto 2.39
- Libcloud

## Configuration

- Boto uses its own [configuration file](boto config file)
- In addition to it, the program has its own config file:


First, create a `config.ini` file from the model and edit it:

```
cp config.ini.sample config.ini
nano config.ini
```

Then, complete the configuration

```
[aws]
aws_access_key_id =
aws_secret_access_key =
aws_region = eu-west-1

[openstack]
openstack_user =
openstack_password =
openstack_url =

[general]
default_alert_email =
```

## Execution
In order to run the program, just execute

```
python main.py
```
