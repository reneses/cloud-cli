from logic.compute_aws import AwsCompute
from logic.connections import Connection
from logic.sns import Sns


class CloudWatch:
    """
    AWS CloudWatch (monitoring) operations
    """

    CPU_ALARM_THRESHOLD = 40.0

    def __init__(self):
        """
        Store the connection and inner the Sns handler (for email notifications)
        """
        self.conn = Connection().cloudwatch_connection()
        self.sns = Sns()

    def _get_metrics(self, instance_id):
        """
        Get the metrics of a given instance

        The 'list_metrics' function admits the dimensions parameter, which will filter the metrics according
        to their dimensions; in this case, by the InstanceId

        :param instance_id: Instance we want the metrics of
        :return: Metrics of the instance
        """
        return self.conn.list_metrics(dimensions={'InstanceId': instance_id})

    def _get_cpu_metric(self, instance_id):
        """
        Get the CPU metric of an instance id

        :param instance_id: Instance ID
        :return: CPU metric, None if it does not exist
        """

        # First, retrieve all the metrics of the instance
        metrics = self._get_metrics(instance_id)

        # Then, filter them by name
        cpu_metrics = filter(lambda metric: metric.name == 'CPUUtilization', metrics)

        # If there is one, return it; None otherwise
        if not len(cpu_metrics):
            return None
        return cpu_metrics[0]

    def _get_cpu_alarms(self):
        """
        Get all the CPU alarms configured

        The 'describe_alarms' return all the alarms, which will be filtered by its metric to return only
        those related to the CPUUtilization

        :return: CPU alarms
        """
        return filter(lambda alarm: alarm.metric == 'CPUUtilization', self.conn.describe_alarms())

    def _get_cpu_alarm(self, instance_id):
        """
        Get the cpu alarm associated with a given instance

        :param instance_id: Instance ID
        :return: CPU alarm if existing, None otherwise
        """

        # Get all the cpu alarms
        alarms = self._get_cpu_alarms()

        # Filter by the instance id
        alarms = filter(lambda alarm: instance_id in alarm.dimensions['InstanceId'], alarms)

        # Return it if it exists, none otherwise
        if not len(alarms):
            return None
        return alarms[0]

    def monitor_instances(self):
        """
        Monitor all the instances
        """
        AwsCompute().monitor_intances()

    def list_metrics(self, instance_id):
        """
        List (print) all the metrics associated with a given instance

        :param instance_id: Instance ID
        """
        for i, metric in enumerate(self._get_metrics(instance_id)):
            print '%d: %s (%s)' % (i, metric.name, metric.namespace)

    def list_cpu_alarms(self):
        """
        List (print) all the existing CPU alarms
        """

        # Get the alarms
        alarms = self._get_cpu_alarms()

        # Message if there are no alarms
        if not len(alarms):
            print 'There are not alarms configured!'
            return

        # Print them
        for i, alarm in enumerate(alarms):
            print '%d: %s' % (i, str(alarm))

    def delete_all_cpu_alarms(self):
        """
        Delete all the cpu alarms
        """
        for alarm in self._get_cpu_alarms():
            alarm.delete()

    def delete_cpu_alarm(self, instance_id):
        """
        Delete a specific cpu alarm

        :param instance_id: Instance ID to delete the alarm from
        :return: True if removed, false if not
        """
        alarm = self._get_cpu_alarm(instance_id)
        if not alarm:
            return False
        alarm.delete()
        return True

    def enable_cpu_alarm(self, instance_id):
        """
        Enable a CPU alarm in an specific instance

        :param instance_id: Instance ID
        :return: True if enabled, false otherwise
        """

        # Get the CPU metric
        cpu_metric = self._get_cpu_metric(instance_id)
        if not cpu_metric:
            return False

        # noinspection PyBroadException
        try:
            # Delete any existing alarms
            self.delete_cpu_alarm(instance_id)

            # Get the SNS topic
            sns_arn = self.sns.cloudwatch_arn

            # Create alarm
            cpu_metric.create_alarm(name='CPUAlarm '+instance_id, comparison='<', threshold=self.CPU_ALARM_THRESHOLD,
                                    period=60, evaluation_periods=2, statistic='Average',
                                    alarm_actions=[sns_arn])

            return True

        except Exception:
            return False
