from menu import Menu, MenuEntry
from logic.cloudformation import CloudFormation

class CloudFormationCli:
    """
    Menu for the AWS CloudFormation operations
    """

    def __init__(self):
        """
        Run the menu
        """

        # Init the logic handler
        self.cloudformation = CloudFormation()

        # Init the menu
        Menu('Amazon Web Services (AWS) Elastic Load Balancer', [
            MenuEntry('Go back', None),
            MenuEntry('Generate web bucket', self.generate_web_bucket),
        ]).run()

    def generate_web_bucket(self):
        """
        Generate a web bucket
        """
        print '# Generating web bucket'
        self.cloudformation.generate_web_bucket()
        print 'Web bucket generated'
