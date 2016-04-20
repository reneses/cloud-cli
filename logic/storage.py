import os


# noinspection PyBroadException
class Storage:
    """
    This class abstracts Storage operation, common for any provider
    """

    def __init__(self, conn):
        """
        Store the connection that will be used

        :param conn: Storage (libcloud) connection
        """
        self.conn = conn

    def _find_container(self, container_name):
        """
        Find a container given its name

        :param container_name: Container name
        :return: Container object
        """
        try:
            return self.conn.get_container(container_name)
        except Exception:
            print 'There is no container with the given name %s' % container_name
            return None

    def get_containers_names(self):
        """
        Obtain the name of the containers

        :return: Name of the containers
        """
        return map(lambda c: c.name, self.conn.list_containers())

    def list_containers(self):
        """
        List (print) the containers
        """
        containers = self.get_containers_names()
        if not len(containers):
            print 'You do not have any containers!'
            return
        for name in containers:
            print '- %s' % name

    def create_container(self, container_name):
        """
        Create a container

        :param container_name: Container name to create
        :return: True if the container was created, false otherwise
        """
        try:
            self.conn.create_container(container_name)
            return True
        except Exception:
            return False

    def delete_container(self, container_name):
        """
        Delete a container

        :param container_name: Name of the container to delete
        :return: True if deleted, false otherwise
        """

        # First, find the container and return if it does not exist
        container = self._find_container(container_name)
        if not container:
            return False

        try:

            # First, delete all the objects within the container
            for o in container.list_objects():
                o.delete()

            # Finally delete the container
            container.delete()
            return True

        except Exception:
            return False

    def get_objects_names(self, container_name):
        """
        Get the names of the objects within a container

        :param container_name: Container name
        :return: Name of the objects
        """

        # First, find the container and return if it does not exist
        container = self._find_container(container_name)
        if not container:
            return None

        # Map each object to its name
        return map(lambda o: o.name, container.list_objects())

    def list_objects(self, container_name):
        """
        List the objects within a container

        :param container_name: Name of the container
        """

        # First, find the container and return if it does not exist
        container = self._find_container(container_name)
        if not container:
            return

        # Print each object information
        objects = container.list_objects()
        if not len(objects):
            print 'The container does not have any object!'
            return
        for o in objects:
            print '- %s (%d bytes)' % (o.name, o.size)

    def delete_object(self, container_name, object_name):
        """
        Delete a certain object

        :param container_name: Name of the container where the object is
        :param object_name: Name fo the object to delete
        :return: True if the object was deleted, false otherwise
        """

        # First, find the container and return false if it does not exist
        container = self._find_container(container_name)
        if not container:
            return False

        # Then, find the object and return false if it does not exist
        obj = container.get_object(object_name)
        if not obj:
            return False

        # Finally try to delete it
        try:
            obj.delete()
            return True
        except Exception:
            return False

    def download_object(self, container_name, object_name, download_path):
        """
        Download a certain object

        :param container_name: Container where the object is
        :param object_name: Name of the object to download
        :param download_path: Path to download the object (empty for current folder)
        :return: True if the object was downloaded, false otherwise
        """

        # First, find the container and return false if it does not exist
        container = self._find_container(container_name)
        if not container:
            return False

        # Then, find the object and return false if it does not exist
        obj = container.get_object(object_name)
        if not obj:
            return False

        # Try to download the file
        try:
            download_path = os.path.join(download_path, object_name)
            obj.download(download_path, True)
            return True
        except Exception:
            return False

    def upload_object(self, container_name, file_path):
        """
        Upload a file to a container

        :param container_name: Name of the container to upload the file to
        :param file_path: Path of the file to upload
        :return: True if uploaded, false otherwise
        """

        # First, find the container and return if it does not exist
        container = self._find_container(container_name)
        if not container:
            return False

        # Try to upload the file
        try:
            filename = os.path.basename(file_path)
            container.upload_object(file_path=file_path, object_name=filename)
            return True
        except Exception:
            return False
