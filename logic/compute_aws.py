from logic.connections import Connection


# noinspection PyBroadException
class AwsCompute:
    """
    AWS EC2 operations
    """

    # Default AMI for Linux machines
    DEFAULT_LINUX_AMI = 'ami-8b8c57f8'

    # Default AMI for Windows machines
    DEFAULT_WINDOWS_AMI = 'ami-c6972fb5'

    def __init__(self):
        """
        EC2Instance Constructor, initiating the EC2 (boto) connection
        """
        self.conn = Connection().ec2_connection()

    def _get_instances(self):
        """
        Get all the instances
        :return: Instances
        """

        # ouput list
        output = []

        # get all instance reservations associated with this AWS account
        reservations = self.conn.get_all_reservations()

        # loop through reservations and extract instance information
        for r in reservations:

            # get all instances from the reservation
            instances = r.instances

            # loop through instances and print instance information
            for i in instances:
                output.append(i)

        return output

    def _get_running_instances(self):
        """
        Filter the instances and return those running (or pending to run)

        :return: Running instances
        """
        return filter(lambda i: i.state == 'running', self._get_instances())

    def _get_not_running_instances(self):
        """
        Filter the instances and return those which are not running

        :return: Not running instances
        """
        return filter(lambda i: i.state != 'running', self._get_instances())

    def _get_volumes(self):
        """
        Get all the volumes

        :return: Volumes
        """
        return self.conn.get_all_volumes()

    def _get_available_volumes(self):
        """
        Filter the volumes to those which are available

        :return: Available volumes
        """
        return self.conn.get_all_volumes(filters={'status': 'available'})

    def _get_used_volumes(self):
        """
        Filter the volumes to those which are in-use

        :return: Used volumes
        """
        return self.conn.get_all_volumes(filters={'status': 'in-use'})

    def get_available_volumes_ids(self):
        """
        Map the available volumes to their IDs

        :return: IDs of the available volumes
        """
        return map(lambda i: i.id, self._get_available_volumes())

    def get_used_volumes_ids(self):
        """
        Map the used volumes to their IDs

        :return: IDs of the used volumes
        """
        return map(lambda i: i.id, self._get_used_volumes())

    def get_instances_ids(self):
        """
        Map the instances to their IDs

        :return: IDs of the instances
        """
        return map(lambda i: i.id, self._get_instances())

    def get_running_instances_ids(self):
        """
        Map the running instances to their IDs

        :return: IDs of the running instances
        """
        return map(lambda i: i.id, self._get_running_instances())

    def get_not_running_instances_ids(self):
        """
        Map the not running instances to their IDs

        :return: IDs of the not running instances
        """
        return map(lambda i: i.id, self._get_not_running_instances())

    def _get_instance_details(self, instance):
        """
        Get an string containing the details of a provided instance

        :param instance: EC2 Instance object
        :return: Details of the instance
        """
        return '{0} - {1} (AMI: {2}) ({3}): (Running since: {4})'.format(
            instance.id, instance.instance_type, instance.image_id, instance.region, instance.launch_time)

    def monitor_intances(self):
        """
        Start monitoring all the instances

        :return: Number of instances which have been started to be monitored (even if they were already been monitored)
        """
        instances_ids = self.get_instances_ids()
        if len(instances_ids):
            self.conn.monitor_instances(instances_ids)
        return len(instances_ids)

    def list_instances(self):
        """
        List (print) all the EC2 Instances
        """

        instances = self._get_instances()

        # Return if there are not instances
        if not instances:
            print 'There are no instances!'
            return

        # Print the details
        for i, instance in enumerate(instances):
            print '%d: %s [%s]' % (i, self._get_instance_details(instance), instance.state)

    def list_running_instances(self):
        """
        List (print) all the running instances
        """

        instances = self._get_running_instances()

        # Return if there are not instances
        if not instances:
            print 'There are no running instances!'
            return

        # Print the details
        for i, instance in enumerate(instances):
            print '%d: %s' % (i, self._get_instance_details(instance))

    def detail_running_instance(self, instance_id):
        """
        Detail a running instance given its ID

        :param instance_id: Instance ID
        """

        # Get the instance
        instances = filter(lambda i: i.id == instance_id, self._get_running_instances())

        # If the instance is not running
        if len(instances) == 0:
            print 'The supplied ID does not exist!'
            return

        # Print the details
        print self._get_instance_details(instances[0])

    def create_instance_by_image(self, ami):
        """
        Create a new instance given an AMI

        :param ami:
        :return: True if created, false otherwise
        """
        try:
            reservation = self.conn.run_instances(ami, instance_type='t2.micro')
            instance = reservation.instances[0]
            instance.monitor()
            return True
        except Exception:
            return False

    def create_instance_by_os(self, is_linux):
        """
        Create a new instance given its OS

        :param is_linux: True if the machine is Linux, False if Windows
        :return: True if created, false otherwise
        """
        if is_linux:
            return self.create_instance_by_image(self.DEFAULT_LINUX_AMI)
        else:
            return self.create_instance_by_image(self.DEFAULT_WINDOWS_AMI)

    def stop_all_instances(self):
        """
        Stop all the running instances

        :return: Number of instances that have been stopped
        """
        instances = self._get_running_instances()
        for i in instances:
            i.stop()
        return len(instances)

    def start_instance(self, instance_id):
        """
        Start an instance given its ID

        :param instance_id: ID of the instance
        :return: True if started, false otherwise
        """
        try:
            self.conn.start_instances([instance_id])
            return True
        except Exception:
            return False

    def stop_instance(self, instance_id):
        """
        Stop an instance given its ID

        :param instance_id: Instance ID
        """
        try:
            self.conn.stop_instances([instance_id])
            return True
        except Exception:
            return False

    def list_volumes(self):
        """
        List (print) all the volumes
        """

        volumes = self._get_volumes()

        # if volumes found
        if not volumes:
            print 'You do not have any volumes!'
            return

        # loop through volumes
        for i, v in enumerate(volumes):
            instance = ''
            if v.attach_data:
                instance = ' - Attached to: %s' % v.attach_data.instance_id
            print '%d: %s, %sGB (%s) [%s] %s' % (i, v.id, v.size, v.zone, v.status, instance)

    def attach_volume(self, volume_id, instance_id):
        """
        Attach a volume to an instance

        :param volume_id: Volume ID
        :param instance_id: Instance ID
        :return: True if attached, false otherwise
        """
        try:
            self.conn.attach_volume(volume_id, instance_id, '/dev/sdx')
            return True
        except Exception:
            return False

    def detach_volume(self, volume_id):
        """
        Detach a volume

        :param volume_id: Volume ID
        :return: True if detached, false otherwise
        """
        try:
            self.conn.detach_volume(volume_id)
            return True
        except Exception:
            return False
