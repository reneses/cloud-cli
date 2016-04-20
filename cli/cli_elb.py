from menu import Menu, MenuEntry
from logic.elastic_load_balancer import ElasticLoadBalancing


class ElbCli:
    """
    Amazon Elastic Cloud Balancer CLI
    """

    def __init__(self):
        """
        Init the logic handler and run the menu
        """
        self.elb = ElasticLoadBalancing()
        Menu('Amazon Web Services (AWS) Elastic Load Balancer', [
            MenuEntry('Go back', None),
            MenuEntry('List all the load balancers', self.list_balancers),
            MenuEntry('Create a load balancer', self.create_balancer),
            MenuEntry('Delete a load balancer', self.delete_balancer),
            MenuEntry('Add instance to load balancer', self.register_instance_to_balancer),
            MenuEntry('Remove instance from load balancer', self.deregister_instance_from_balancer),
        ]).run()

    def _choose_among_load_balancers(self):
        """
        Ask the user to choose among the load balancers
        :return: Load balancer name, false value if cancelled
        """

        balancers = self.elb.get_load_balancers_names()

        # No instances
        if not balancers:
            print 'You do not have any load balancers!'
            return None

        # List the name of the instances
        print 'Choose a load balancer:'
        for i, balancer in enumerate(balancers):
            print '%d) %s' % ((i + 1), balancer)
        print

        # Choose an instance
        balancer_name = ''
        while True:

            choice = raw_input("Load balancer target number (empty to cancel): ")

            # Cancel
            if not choice:
                return None

            # Valid choice
            choice = int(choice)
            if 1 <= choice <= len(balancers):
                balancer_name = balancers[choice - 1]
                break

            # Invalid option
            print 'Incorrect option!'
            continue

        print
        return balancer_name

    def list_balancers(self):
        """
        List (print) the balancers
        """
        print '# Listing load balancers'
        self.elb.list_load_balancers()

    def create_balancer(self):
        """
        Create a new load balancer, asking the user for its name
        """
        name = raw_input("Name for the new load balancer (empty to cancel): ")

        # Cancel
        if not name:
            print 'Operation cancelled!'
            return
        print

        # Create the load balancer
        print '# Creating load balancer "%s"' % name
        if self.elb.create_load_balancer(name):
            print 'Load balancer created!'
        else:
            print 'The load balancer could not be created'

    def delete_balancer(self):
        """
        Delete a load balancer
        The user will be asked for the load balancer name
        """

        balancer_name = self._choose_among_load_balancers()

        # Cancel operation
        if not balancer_name:
            print 'Operation cancelled!'
            return

        # Delete the load balancer
        print '# Delenting load balancer "%s"' % balancer_name
        if self.elb.delete_load_balancer(balancer_name):
            print 'Load balancer deleted!'
        else:
            print 'The load balancer could not be deleted'

    def register_instance_to_balancer(self):
        """
        Add an EC2 instance to the load balancer
        The user will me prompt for the instance id
        """

        # Ask for the balancer
        balancer_name = self._choose_among_load_balancers()

        # Cancel operation
        if not balancer_name:
            print 'Operation cancelled!'
            return

        # Ask for the instance
        instance_id = raw_input("Enter the instance id (empty to cancel): ")

        # Cancel operation
        if not instance_id:
            print 'Operation cancelled!'
            return
        print

        # Add the instance to the balancer
        print '# Adding instance "%s" to the load balancer "%s"' % (instance_id, balancer_name)
        if self.elb.register_instance_to_load_balancer(balancer_name, instance_id):
            print 'Instance added!'
        else:
            print 'The instance could not be added'

    def deregister_instance_from_balancer(self):
        """
        Remove an instance from a balancer
        """

        # Ask for the balancer
        balancer_name = self._choose_among_load_balancers()

        # Cancel
        if not balancer_name:
            print 'Operation cancelled!'
            return

        # Ask for the instance
        instance_id = raw_input("Enter the instance id (empty to cancel): ")

        # Cancel
        if not instance_id:
            print 'Operation cancelled!'
            return
        print

        # Remove the instance
        print '# Removing instance "%s" from the load balancer "%s"' % (instance_id, balancer_name)
        if self.elb.deregister_instance_from_load_balancer(balancer_name, instance_id):
            print 'Instance removed!'
        else:
            print 'The instance could not be removed'
