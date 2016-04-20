from menu import Menu, MenuEntry
from logic.cloudwatch import CloudWatch


class CloudWatchCli:
    """
    Menu for AWS CloudWatch
    """

    def __init__(self):
        """
        Create the logic handler and run the menu
        """
        self.cloudwatch = CloudWatch()
        Menu('AWS CloudWatch operations', [
            MenuEntry('Go back', None),
            MenuEntry('Monitor all the instances', self.monitor_instances),
            MenuEntry('Print metrics', self.print_metrics),
            MenuEntry('List CPU alarms', self.list_cpu_alarms),
            MenuEntry('Enable CPU alarm in an instance', self.enable_cpu_alarm_instance),
            MenuEntry('Delete CPU alarm in an instance', self.delete_cpu_alarm),
            MenuEntry('Delete all the CPU alarms', self.delete_all_cpu_alarms),
            MenuEntry('Change email recipient for CPU alarms', self.change_email_cpu_alarms),
        ]).run()

    def monitor_instances(self):
        """
        Monitor all the instances
        """
        print '# Monitoring all the instances'
        self.cloudwatch.monitor_instances()

    def print_metrics(self):
        """
        Print all the available metrics for a given instance
        :return:
        """

        # Ask for the instance ID
        instance_id = raw_input('Instance ID to show metrics of (empty to cancel): ')

        # Cancel option
        if not instance_id:
            print 'Operation canceled!'
            return
        print

        # Print the metrics
        print '# Metrics available for the instance %s' % instance_id
        self.cloudwatch.list_metrics(instance_id)

    def list_cpu_alarms(self):
        """
        List all the cpu alarms
        """
        print '# Listing CPU alarms'
        self.cloudwatch.list_cpu_alarms()

    def enable_cpu_alarm_instance(self):
        """
        Enable the CPU alarm for a given instance
        """

        # Ask for the instance ID
        instance_id = raw_input('Instance ID to enable CPU alarm on (empty to cancel): ')

        # Cancel option
        if not instance_id:
            print 'Operation canceled!'
            return
        print

        # Enable the alarm
        print '# Enabling CPU alarm in the instance "%s"' % instance_id
        if self.cloudwatch.enable_cpu_alarm(instance_id):
            print 'The alarm was enabled'
        else:
            print 'The alarm could not be enabled'

    def delete_cpu_alarm(self):
        """
        Delete a CPU alarm for a given instance ID
        """

        # Ask for the instance ID
        instance_id = raw_input('Instance ID to delete CPU alarm from (empty to cancel): ')

        # Cancel option
        if not instance_id:
            print 'Operation canceled!'
            return
        print

        # Delete the alarm
        print '# Deleting CPU alarm from the instance "%s"' % instance_id
        if self.cloudwatch.delete_cpu_alarm(instance_id):
            print 'The alarm was deleted'
        else:
            print 'The alarm could not be deleted'

    def delete_all_cpu_alarms(self):
        """
        Delete all the CPU alarms
        """
        print '# Deleting all the CPU alarms'
        self.cloudwatch.delete_all_cpu_alarms()
        print 'Alarms deleted'

    def change_email_cpu_alarms(self):
        """
        Change the email address used in the CPU alarms
        """

        # Ask for the new email
        email = raw_input('New email for CPU alarms (empty to cancel): ')

        # Cancel operation
        if not email:
            print 'Operation canceled!'
            return
        print

        # Change the email
        print '# Changing email for CPU alerts to "%s"' % email
        if self.cloudwatch.sns.set_only_subscriber_to_cloudwatch(email):
            print 'Email changed'
        else:
            print 'The email could not be changed'
