from connections import Connection
from storage import Storage


class AwsStorage(Storage):
    """
    AWS (S3) Storage
    """

    def __init__(self):
        """
        Create an storage instance passing an Amazon S3 connection
        """
        Storage.__init__(self, Connection().s3_connection())
