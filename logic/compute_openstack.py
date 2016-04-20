from logic.connections import Connection


class OpenStackCompute:
    """
    OpenStack compute operations
    """

    def __init__(self):
        """
        Init the OpenStack connection
        """
        self.conn = Connection().openstack_connection()

    def list_running_instances(self):
        """
        List (print) all the running instances
        """
        for i, node in enumerate(self.conn.list_nodes()):
            if not node.state:
                print '%d: %s - %s (Zone: %s)' % (i, node.name, node.id, node.extra['availability_zone'])
