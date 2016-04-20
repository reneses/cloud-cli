from cli_storage import StorageCli
from logic.storage_openstack import OpenStackStorage


class OpenStackStorageCli(StorageCli):
    """
    OpenStack storage menu
    """

    def __init__(self):
        """
        Init an StorageCli instance with an OpenStack storage
        """
        title = 'OpenStack Storage operations'
        StorageCli.__init__(self, title, OpenStackStorage())
