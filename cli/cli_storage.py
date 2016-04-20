import os

from menu import Menu, MenuEntry


class StorageCli:
    """
    Storage menu, common for any provider
    """

    def __init__(self, title, storage):
        """
        Store the storage handler and init the menu

        :param title: Menu title
        :param storage: Storage handler
        """
        self.storage = storage
        Menu(title, [
            MenuEntry('Go back', None),
            MenuEntry('List containers', self.list_containers),
            MenuEntry('Create a container', self.create_container),
            MenuEntry('Delete a container', self.delete_container),
            MenuEntry('List objects', self.list_objects),
            MenuEntry('Upload an object', self.upload_object),
            MenuEntry('Download an object', self.download_object),
            MenuEntry('Delete an object', self.delete_object),
        ]).run()

    def _choice_among_containers(self):
        """
        Ask the user to choose among the containers

        :return: Container name, false value if cancelled
        """

        containers = self.storage.get_containers_names()

        # No containers
        if not containers:
            print 'You do not have any containers to upload files to!'
            return None

        # List the name of containers
        print 'Choose a container:'
        for i, c in enumerate(containers):
            print '%d) %s' % ((i + 1), c)
        print

        # Choose a container
        container_name = ''
        while True:

            choice = raw_input("Container target number or name (empty to cancel): ")

            # Cancel
            if not choice:
                break

            # Valid choice
            if choice in containers:
                container_name = choice
                break
            choice = int(choice)
            if 1 <= choice <= len(containers):
                container_name = containers[choice - 1]
                break

            # Invalid option
            print 'Incorrect option!'
            continue

        print
        return container_name

    def _choice_among_objects(self, container_name):
        """
        Ask the user to choose among objects

        :param container_name: Container name containing the objects
        :return: Object name, false value if cancelled
        """

        # List the name of containers
        print 'Choose an object:'
        objects = self.storage.get_objects_names(container_name)

        # No objects
        if not len(objects):
            print 'There are no objects in this container!'
            return None

        # Print the objects
        for i, c in enumerate(objects):
            print '%d) %s' % ((i + 1), c)
        print

        # Choose a container
        object_name = ''
        while True:

            choice = raw_input("Object target number (empty to cancel): ")

            # Cancel
            if not choice:
                break

            # Valid choice
            choice = int(choice)
            if 1 <= choice <= len(objects):
                object_name = objects[choice - 1]
                break

            # Invalid option
            print 'Incorrect option!'
            continue

        print
        return object_name

    def list_containers(self):
        """
        List all the containers
        """
        print "# Containers: "
        self.storage.list_containers()

    def list_objects(self):
        """
        List all the objects within a container
        The parent container will be asked to the user
        """

        # Choose container name
        container_name = self._choice_among_containers()

        # Exit option
        if not container_name:
            print 'Operation cancelled'
            return

        # Display files
        print '# Objects in the "%s" container' % container_name
        self.storage.list_objects(container_name)

    def create_container(self):
        """
        Create a container
        The container name will be asked to the user
        """
        print "# Create a container: \n"
        while True:

            # Ask for the container name
            container_name = raw_input('Container name (empty to cancel): ')

            # Cancel the operation
            if not container_name:
                print 'Operation cancelled'
                break

            # Create a container
            if self.storage.create_container(container_name):
                print 'The container "%s" was created' % container_name
                break

            # Error
            print 'The container "%s" cannot be created' % container_name

    def delete_container(self):
        """
        Delete a container
        The container name will be asked to the user
        """

        print "# Delete a container: \n"

        # Choose container name
        container_name = self._choice_among_containers()

        # Exit option
        if not container_name:
            print 'Operation cancelled'
            return

        # Delete the container
        if self.storage.delete_container(container_name):
            print 'The container "%s" was deleted' % container_name

        # Error
        else:
            print 'The container "%s" cannot be deleted' % container_name

    def delete_object(self):
        """
        Delete an object
        The object name and container will be asked to the user
        """

        print "# Deleting an object: \n"

        # Choose container name
        container_name = self._choice_among_containers()

        # Exit option
        if not container_name:
            print 'Operation cancelled'
            return

        # Choose the object
        object_name = self._choice_among_objects(container_name)

        # Exit option
        if not object_name:
            print 'Operation cancelled'
            return

        # Delete the container
        if self.storage.delete_object(container_name, object_name):
            print 'The object "%s/%s" was deleted' % (container_name, object_name)

        # Error
        else:
            print 'The object "%s/%s" could be deleted' % (container_name, object_name)

    def download_object(self):
        """
        Download an object
        The container name, object name and download path will be asked to the user
        """

        print "# Downloading an object: \n"

        # Choose container name
        container_name = self._choice_among_containers()

        # Exit option
        if not container_name:
            print 'Operation cancelled'
            return

        # Choose the object
        object_name = self._choice_among_objects(container_name)

        # Exit option
        if not object_name:
            print 'Operation cancelled'
            return

        # Ask for the download path
        file_path = ''
        while True:

            file_path = raw_input('File path (empty for current dir): ')

            # Validate the path
            if file_path == '' or os.path.isdir(file_path):
                break

            # If the folder does not exist, continue asking for one
            print 'The folder does not exist!'

        # Download the file
        if self.storage.download_object(container_name, object_name, file_path):
            print 'File downloaded!'
        else:
            print 'The file could not be downloaded'

    def upload_object(self):
        """
        Upload an object
        The container name and object path will be asked to the user
        """

        container_name = self._choice_among_containers()
        if not container_name:
            return

        print '# Uploading a file to the "%s" container' % container_name
        while True:

            file_path = raw_input('File path (empty to cancel): ')

            # Cancel operation
            if not file_path:
                print 'Operation cancelled'
                break

            # Check it exists
            if not os.path.isfile(file_path):
                print 'The file does not exist!'
                continue

            # Upload
            if self.storage.upload_object(container_name, file_path):
                print 'The file was uploaded to the "%s" container' % container_name
            else:
                print 'The file could not be uploaded!'
            break
