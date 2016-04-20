from cli_storage import StorageCli
from logic.storage_aws import AwsStorage


class AwsStorageCli(StorageCli):
    """
    AWS S3 Storage menu
    """

    def __init__(self):
        """
        Init an StorageCli instance with an AWS storage
        """
        title = 'AWS Storage operations'
        StorageCli.__init__(self, title, AwsStorage())
