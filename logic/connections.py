from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.storage.types import Provider as StorageProvider
import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.cloudwatch
import boto.sns
import boto.cloudformation
from ConfigParser import ConfigParser


class Connection:
    """
    The connection class take care of managing the user credentials and authenticating the user
    in the different providers
    """

    def __init__(self):
        """
        The constructor will read the config.ini file and load the properties as class constants
        """

        # Read the file
        cloud_config = ConfigParser()
        cloud_config.read("config.ini")

        # AWS configuration
        self.AWS_ACCESS_ID = cloud_config.get('aws', 'aws_access_key_id')
        self.AWS_SECRET_KEY = cloud_config.get('aws', 'aws_secret_access_key')
        self.AWS_REGION = cloud_config.get('aws', 'aws_region')

        # OpenStack configuration
        self.OPENSTACK_USER = cloud_config.get('openstack', 'openstack_user')
        self.OPENSTACK_PASS = cloud_config.get('openstack', 'openstack_password')
        self.OPENSTACK_URL = cloud_config.get('openstack', 'openstack_url')

        # Other config
        self.DEFAULT_ALERT_EMAIL = cloud_config.get('general', 'default_alert_email')

    def ec2_connection(self):
        """
        Obtain a EC2 connection
        The credentials are directly extracted from the boto config file

        :return: EC2 (boto) connection
        """
        return boto.ec2.connect_to_region(self.AWS_REGION)

    def ec2_elb_connection(self):
        """
        Obtain a EC2 elastic load balancer connection
        The credentials are directly extracted from the boto config file

        :return: EC2 ELB (boto) connection
        """
        return boto.ec2.elb.connect_to_region(self.AWS_REGION)

    def cloudwatch_connection(self):
        """
        Obtain a CloudWatch (boto) connection
        The credentials are directly extracted from the boto config file

        :return: CloudWatch (boto) connection
        """
        return boto.ec2.cloudwatch.connect_to_region(self.AWS_REGION)

    def sns_connection(self):
        """
        Obtain a SNS (boto) connection
        The credentials are directly extracted from the boto config file

        :return: SNS (boto) connection
        """
        return boto.sns.connect_to_region(self.AWS_REGION)

    def cloudformation_connection(self):
        """
        Obtain a CloudFormation connection
        The credentials are directly extracted from the boto config file

        :return: CloudFormation (boto) connection
        """
        return boto.cloudformation.connect_to_region(self.AWS_REGION)

    def s3_connection(self):
        """
        Obtain a S3 connection

        :return: S3 (libcloud) connection
        """
        driver = get_storage_driver(StorageProvider.S3_EU_WEST)
        return driver(self.AWS_ACCESS_ID, self.AWS_SECRET_KEY)


    def openstack_connection(self):
        """
        Obtain a OpenStack connection

        :return: OpenStack (libcloud) connection
        """
        driver = get_driver(Provider.OPENSTACK)
        return driver(self.OPENSTACK_USER, self.OPENSTACK_PASS,
                      ex_force_auth_url=self.OPENSTACK_URL,
                      ex_force_auth_version='2.0_password',
                      ex_tenant_name=self.OPENSTACK_USER,
                      ex_force_service_region='RegionOne')

    def openstack_swift_connection(self):
        """
        Obtain a OpenStack Swift connection

        :return: OpenStack Swift (libcloud) connection
        """
        driver = get_storage_driver(StorageProvider.OPENSTACK_SWIFT)
        return driver(self.OPENSTACK_USER, self.OPENSTACK_PASS,
                      ex_force_auth_url=self.OPENSTACK_URL,
                      ex_force_auth_version='2.0_password',
                      ex_tenant_name=self.OPENSTACK_USER,
                      ex_force_service_region='RegionOne')
