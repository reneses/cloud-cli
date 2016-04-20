from cli_storage_aws import AwsStorageCli
from cli_storage_openstack import OpenStackStorageCli
from cli_cloudformation import CloudFormationCli
from cli_cloudwatch import CloudWatchCli
from cli_compute_openstack import OpenStackComputeCli
from cli_elb import ElbCli
from cli_compute_aws import AwsComputeCli
from menu import Menu, MenuEntry


class Cli:
    """
    The CLI class represents the main menu, offering access to different sub menus
    """

    def __init__(self):
        """
        Main menu
        """
        Menu('Select provider', [
            MenuEntry('Exit', None),
            MenuEntry('Amazon AWS', self.aws),
            MenuEntry('OpenStack', self.openstack),
        ]).run()

    def aws(self):
        """
        AWS menu
        """
        Menu('[AWS] Select type of operations', [
            MenuEntry('Go back', None),
            MenuEntry('Compute', self.aws_compute),
            MenuEntry('Storage', self.aws_storage),
            MenuEntry('CloudWatch', self.aws_cloudwatch),
            MenuEntry('Elastic Load Balancer', self.aws_elb),
            MenuEntry('CloudFormation', self.aws_cloudformation),
        ]).run()

    def openstack(self):
        """
        OpenStack menu
        :return:
        """
        Menu('[OpenStack] Select type of operations', [
            MenuEntry('Go back', None),
            MenuEntry('Compute', self.openstack_compute),
            MenuEntry('Storage', self.openstack_storage),
        ]).run()

    def aws_compute(self):
        """
        AWS Compute sub menu
        """
        AwsComputeCli()

    def aws_storage(self):
        """
        AWS Storage sub menu
        """
        AwsStorageCli()

    def aws_cloudwatch(self):
        """
        AWS CloudWatch sub menu
        """
        CloudWatchCli()

    def aws_elb(self):
        """
        AWS Elastic Load Balancer sub menu
        """
        ElbCli()

    def aws_cloudformation(self):
        """
        AWS CloudFormation sub menu
        """
        CloudFormationCli()

    def openstack_storage(self):
        """
        OpenStack storage sub menu
        """
        OpenStackStorageCli()

    def openstack_compute(self):
        """
        OpenStack compute sub menu
        """
        OpenStackComputeCli()
