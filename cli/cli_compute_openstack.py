from menu import Menu, MenuEntry
from logic.compute_openstack import OpenStackCompute


class OpenStackComputeCli:
    """
    OpenStack computing operations menu
    """

    def __init__(self):
        """
        Init the logic handler and run the menu
        """
        self.compute = OpenStackCompute()
        Menu('Openstack Compute operations', [
            MenuEntry('Go back', None),
            MenuEntry('List running instances', self.list_running_instances),
        ]).run()

    def list_running_instances(self):
        """
        List the running instances
        """
        self.compute.list_running_instances()
