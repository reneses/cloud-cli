from connections import Connection
from storage import Storage


class OpenStackStorage(Storage):
    """
    OpenStack storage
    """

    def __init__(self):
        """
        Create an storage instance with an OpenStack (Swift) storage connection
        """
        Storage.__init__(self, Connection().openstack_swift_connection())
