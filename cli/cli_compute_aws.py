from menu import Menu, MenuEntry
from logic.compute_aws import AwsCompute


class AwsComputeCli:
    """
    AWS CLI menu for computing operations
    """

    def __init__(self):
        """
        Init the logic handler and run the menu
        """
        self.compute = AwsCompute()
        Menu('Amazon Web Services (AWS) Compute operations', [
            MenuEntry('Go back', None),
            MenuEntry('List all the instances', self.list_instances),
            MenuEntry('Stop all the instances', self.stop_all_instances),
            MenuEntry('List running instances', self.list_running_instances),
            MenuEntry('Detail a running instance', self.detail_running_instance),
            MenuEntry('Start a specific instance', self.start_instance),
            MenuEntry('Stop a specific instance', self.stop_instance),
            MenuEntry('Start a new instance given an AMI', self.create_instance_by_image),
            MenuEntry('Start a new instance given the Operating System', self.create_instance_by_os),
            MenuEntry('List volumes', self.list_volumes),
            MenuEntry('Attach a volume', self.attach_volume),
            MenuEntry('Detach a volume', self.detach_volume),
        ]).run()

    def _choose_among_running_instances(self):
        """
        Ask the user to choose one running instance
        :return: Instance id of a running instance, false value if cancelled
        """

        instances = self.compute.get_running_instances_ids()

        # No instances
        if not instances:
            print 'You do not have any running instances!'
            return None

        # List the name of the instances
        print 'Choose an instance:'
        for i, instance in enumerate(instances):
            print '%d) %s' % ((i + 1), instance)
        print

        # Choose an instance
        instance_id = ''
        while True:

            choice = raw_input("Instance target number or ID (empty to cancel): ")

            # Cancel
            if not choice:
                return None

            # Valid choice
            if choice in instances:
                instance_id = choice
                break
            choice = int(choice)
            if 1 <= choice <= len(instances):
                instance_id = instances[choice - 1]
                break

            # Invalid option
            print 'Incorrect option!'
            continue

        print
        return instance_id

    def _choose_among_stopped_instances(self):
        """
        Ask the user to choose one stopped instance
        :return: Instance id of a stopped instance, false value if cancelled
        """

        instances = self.compute.get_not_running_instances_ids()

        # No instances
        if not instances:
            print 'You do not have any instances!'
            return None

        # List the name of the instances
        print 'Choose an instance:'
        for i, instance in enumerate(instances):
            print '%d) %s' % ((i + 1), instance)
        print

        # Choose an instance
        instance_id = ''
        while True:

            choice = raw_input("Instance target number or ID (empty to cancel): ")

            # Cancel
            if not choice:
                return None

            # Valid choice
            if choice in instances:
                instance_id = choice
                break
            choice = int(choice)
            if 1 <= choice <= len(instances):
                instance_id = instances[choice - 1]
                break

            # Invalid option
            print 'Incorrect option!'
            continue

        print
        return instance_id

    def _choose_among_available_volumes(self):
        """
        Ask the user to choose an available volume
        :return: Volume id of an available volume, false value if cancelled
        """

        volumes = self.compute.get_available_volumes_ids()

        # No instances
        if not volumes:
            print 'You do not have any available volumes!'
            return None

        # List the name of the instances
        print 'Choose a volume:'
        for i, v in enumerate(volumes):
            print '%d) %s' % ((i + 1), v)
        print

        # Choose an instance
        volume_id = ''
        while True:

            choice = raw_input("Volume target number or ID (empty to cancel): ")

            # Cancel
            if not choice:
                return None

            # Valid choice
            if choice in volumes:
                volume_id = choice
                break
            choice = int(choice)
            if 1 <= choice <= len(volumes):
                volume_id = volumes[choice - 1]
                break

            # Invalid option
            print 'Incorrect option!'
            continue

        print
        return volume_id

    def _choose_among_used_volumes(self):
        """
        Ask the user to choose an used volume
        :return: Volume id of an used volume, false value if cancelled
        """

        volumes = self.compute.get_used_volumes_ids()

        # No instances
        if not volumes:
            print 'You do not have any used volumes!'
            return None

        # List the name of the instances
        print 'Choose a volume:'
        for i, v in enumerate(volumes):
            print '%d) %s' % ((i + 1), v)
        print

        # Choose an instance
        volume_id = ''
        while True:

            choice = raw_input("Volume target number or ID (empty to cancel): ")

            # Cancel
            if not choice:
                return None

            # Valid choice
            if choice in volumes:
                volume_id = choice
                break
            choice = int(choice)
            if 1 <= choice <= len(volumes):
                volume_id = volumes[choice - 1]
                break

            # Invalid option
            print 'Incorrect option!'
            continue

        print
        return volume_id

    def list_instances(self):
        """
        List (print) the EC2 instances
        """
        print '# AWS EC2 instances'
        self.compute.list_instances()

    def list_running_instances(self):
        """
        List (print) the running EC2 instances
        """
        print '# Running AWS EC2 instances'
        self.compute.list_running_instances()

    def detail_running_instance(self):
        """
        Detail a given EC2 running instance
        The instance id is asked to the user
        """

        instance_id = self._choose_among_running_instances()

        # Exit option
        if not instance_id:
            print 'Operation cancelled'
            return

        # Print the details
        print '# Details of the "%s" instance' % instance_id
        self.compute.detail_running_instance(instance_id)

    def create_instance_by_image(self):
        """
        Create an EC2 instance given an AMI
        """
        print '# Start a new instance based on an existing AMI'
        ami = raw_input('Enter AMI (empty to cancel): ')

        # Cancel
        if not ami:
            print 'Operation cancelled'
            return

        # Start the instance
        if self.compute.create_instance_by_image(ami):
            print 'Instance started!'
        else:
            print 'It was not possible to create an instance with the given AMI'

    def create_instance_by_os(self):
        """
        Create an EC2 instance given the OS
        The user will be asked to choose between Windows or Linux

        """
        print '# Start a new instance based on the OS'

        # Choose between linux or windows
        is_linux = True
        while True:

            os = raw_input('Enter the OS (windows/linux or empty to cancel): ')

            # Cancel
            if not os:
                print 'Operation cancelled'
                return

            # Check if linux
            if os.lower() == 'linux':
                is_linux = True
                break

            # Check windows
            if os.lower() == 'windows':
                is_linux = False
                break

            # Error
            print 'Invalid input!'

        # Create the instance
        if self.compute.create_instance_by_os(is_linux):
            print 'Instance started!'
        else:
            print 'It was not possible to create an instance with the given OS'

    def stop_all_instances(self):
        """
        Stop all the EC2 instances
        """
        print '# Stopping all the instances'
        number = self.compute.stop_all_instances()
        print '%d instances were stopped' % number

    def stop_instance(self):
        """
        Stop a certain instance
        The instance ID will be asked to the user
        """
        instance_id = self._choose_among_running_instances()

        # Cancel
        if not instance_id:
            print 'Operation cancelled'
            return

        print '# Stopping the instance "%s"' % instance_id
        self.compute.stop_instance(instance_id)
        print 'The instance has been stopped'

    def start_instance(self):
        """
        Start an stopped instance
        The instance id wil be asked to the user
        """
        instance_id = self._choose_among_stopped_instances()

        # Cancel
        if not instance_id:
            print 'Operation cancelled'
            return

        print '# Starting the instance "%s"' % instance_id
        if self.compute.start_instance(instance_id):
            print 'The instance has been started'
        else:
            print 'The instance could not be started'

    def attach_volume(self):
        """
        Attach an available volume to an instance
        """

        # Choose volume
        volume_id = self._choose_among_available_volumes()

        # Cancel
        if not volume_id:
            print 'Operation cancelled'
            return

        # Choose instance
        instance_id = self._choose_among_running_instances()

        # Cancel
        if not instance_id:
            print 'Operation cancelled'
            return

        # Attach the volume
        print '# Attaching volume "%s"!' % volume_id
        if self.compute.attach_volume(volume_id, instance_id):
            print 'The volume has been attached!'
        else:
            print 'The volume could not been attached'

    def detach_volume(self):
        """
        Dettach a volume from an instance
        """

        # Choose the volume
        volume_id = self._choose_among_used_volumes()

        # Cancel
        if not volume_id:
            print 'Operation cancelled'
            return

        # Detach the volume
        print '# Detaching volume "%s"!' % volume_id
        if self.compute.detach_volume(volume_id):
            print 'The volume has been detached!'
        else:
            print 'The volume could not been detached'

    def list_volumes(self):
        """
        List (print) all the volumes
        """
        print '# Listing existing volumes'
        self.compute.list_volumes()
