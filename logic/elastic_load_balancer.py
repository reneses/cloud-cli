from boto.ec2.elb import HealthCheck

from logic.connections import Connection


# noinspection PyBroadException
class ElasticLoadBalancing:
    """
    The Elastic Load Balancing AWS service automatically distributes incoming  traffic across multiple Amazon EC2
    instances, which provides fault tolerance and load distribution

    This class provides operations to create and delete load balancers, as well as registering or removing instances
    from each constructor

    It's effectiveness can be tested by executing requests to the load balancer and observing how they are redirected
    """

    def __init__(self):
        """
        Init the ELB (boto) connection
        """
        self.conn = Connection().ec2_elb_connection()

    def _get_load_balancers(self):
        """
        Get all the load balancers

        :return: Load balancers
        """
        return self.conn.get_all_load_balancers()

    def get_load_balancers_names(self):
        """
        Map the list of load balancers to their names

        :return: Names of the load balancers
        """
        return map(lambda lb: lb.name, self._get_load_balancers())

    def _get_load_balancer(self, load_balancer_name):
        """
        Get a load balancer object given its name

        :param load_balancer_name: Name of the load balancer to retrieve
        :return: The load balancer if it exists, None otherwise
        """
        balancers = self.conn.get_all_load_balancers([load_balancer_name])
        if not len(balancers):
            return None
        return balancers[0]

    def list_load_balancers(self):
        """
        List (print) all the load balancers
        """
        balancers = self._get_load_balancers()

        if len(balancers) == 0:
            print 'There are no load balancers created!'
            return

        for i, lb in enumerate(balancers):
            print '%d: %s (Instances: %s) (DNS: %s) (Zones: %s)' % (
                i, lb.name, lb.instances, lb.dns_name, lb.availability_zones)

    def create_load_balancer(self, load_balancer_name):
        """
        Create a load balancer

        :param load_balancer_name: Name of the load balance to create
        :return: True if created, false otherwise
        """
        try:

            # First, the load balancer is created
            zones = ['eu-west-1b', 'eu-west-1c', 'eu-west-1a']
            ports = [(80, 8080, 'http'), (443, 8443, 'tcp')]
            lb = self.conn.create_load_balancer(load_balancer_name, zones, ports)

            # Then, a health check is created and associated with it
            hc = HealthCheck(
                interval=20,
                healthy_threshold=3,
                unhealthy_threshold=5,
                target='HTTP:8080/health'
            )
            lb.configure_health_check(hc)
            return True

        except Exception:
            return False

    def delete_load_balancer(self, load_balancer_name):
        """
        Delete a load balancer

        :param load_balancer_name: Name of the load balancer to delete
        :return: True if deleted, false otherwise
        """

        balancer = self._get_load_balancer(load_balancer_name)

        # Return if the balancer does not exist
        if not balancer:
            return False

        try:
            balancer.delete()
            return True

        except Exception:
            return False

    def register_instance_to_load_balancer(self, load_balancer_name, instance_id):
        """
        Register an instance to a load balancer

        :param load_balancer_name: Load balancer name
        :param instance_id: Instance ID to register
        :return: True if registered, false otherwise
        """

        balancer = self._get_load_balancer(load_balancer_name)

        # Return if the balancer does not exist
        if not balancer:
            return False

        try:
            balancer.register_instances([instance_id])
            return True
        except Exception:
            return False

    def deregister_instance_from_load_balancer(self, load_balancer_name, instance_id):
        """
        Remove an instance from a load balancer

        :param load_balancer_name: Load balancer name
        :param instance_id: Instance ID to deregister
        :return: True if deregistered, false otherwise
        """

        balancer = self._get_load_balancer(load_balancer_name)

        # Return if the balancer does not exist
        if not balancer:
            return False

        try:
            balancer.deregister_instances([instance_id])
            return True
        except Exception:
            return False
