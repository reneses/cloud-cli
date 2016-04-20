import sys


class MenuEntry:
    """
    Class representing a menu entry, which has a name and an associated function
    """

    def __init__(self, name, f):
        """
        Entry constructor

        :param name: Name to display
        :param f: Associated function
        """
        self.name = name
        self.f = f


class Menu:
    """
    Class representing a CLI menu
    """

    def __init__(self, name, menu):
        """
        Init the menu

        :param name: Menu name or title
        :param menu: Collection of menu entries
        """
        self.name = name
        self.menu = menu

    def _get_function(self, number):
        """
        Get a function given its number

        :param number: Function number
        :return: Function
        """
        return self.menu[number].f

    def __str__(self):
        """
        Obtain a beautiful printable representation of the menu

        :return: Formatted menu
        """
        hashtags = '#' * (len(self.name) + 10)
        out = hashtags + '\n'
        out += '     ' + self.name + '     \n'
        out += hashtags + '\n'

        for i, entry in enumerate(self.menu):
            out += '%d) %s\n' % (i, entry.name)
        return out

    def run(self):
        """
        Run the menu, allowing the user to navigate between the options
        """

        # Print the menu
        print self.__str__()

        # Run the menu forever
        while True:

            # Ask for the option
            choice = raw_input("Choose an option (empty to exit): ")

            # Exit option
            if not choice:
                print 'Good bye!'
                sys.exit(0)

            # Validate option
            try:
                choice = int(choice)
                if not 0 <= choice < len(self.menu):
                    raise ValueError
            except ValueError:
                print 'Invalid input'
                continue

            # Execute the option and display the menu again
            f = self._get_function(choice)
            if f:
                print
                f()
                print '\n'
                self.run()
                break

            # Go back
            else:
                return
