from time import sleep

from entities import Directory
import threading


class InputParser:
    """
    Class to parse the given input from the user
    """
    _root_directory: Directory

    def __init__(self):
        """
        Inits the class and prints a welcome message
        """
        print("Welcome to the best File Manager Ever!")

    def request_input(self):
        """
        Requests input from the user until the user decides to exit
        every input is then delivered to the corresponding method mapped with get_input_map()
        """
        while True:
            root = input("Please enter the root directory:")
            try:
                self._root_directory = Directory('', root)
                break
            except Exception as e:
                print(str(e))
                print('Please try again')

        input_map = self._get_input_map()

        while True:
            inp = input("Please enter your method:")
            method = input_map.get(inp)
            if method is None:
                print("Sorry! this method doesn't see to exist")
                print("If you need any help just type 'help'")
            response = method()
            if response is True:
                return

    @classmethod
    def _make_new_thread(cls, func, args=None):
        """
        Created a new Thread instance and starts it
        :param func: The target function to run
        :param args: The arguments of the function
        """
        if args is None:
            args = tuple()
        threading.Thread(target=func, args=args).start()

    def _get_input_map(self):
        """
        Maps the commands to the corresponding methods
        :return: a dict with keys as commands and values as methods
        """
        return {
            'addFile': self._add_file,
            'addDir': self._add_dir,
            'delete': self._delete,
            'showFileSystem': self._show_file_system,
            'exit': self._exit,
            'help': self._help
        }

    def _help(self):
        """
        Prints help for the user
        """
        print('addFile - Adds a new file to the system')
        print('addDir - Adds a new directory to the system')
        print('delete - Deletes a file/directory in the system')
        print('showFileSystem - Shows the file system hierarchy')
        print('exit - Exits the system')
        print('help - Shows all the commands')

    def _add_file(self):
        """
        Adds a new file to the system and prints a message upon success or failure
        Runs on a separate thread
        """
        parent_dir_name = self._var_input("Insert parent directory name:", str)
        file_name = self._var_input("Insert file name  (String 32 letters max):", str, lambda x: len(x) < 32)
        file_size = self._var_input("Insert file size:", int, lambda x: x >= 0)

        def thread_method(parent_dir_name_1, file_name_1, file_size_1):
            message, created = self._root_directory.add_file(parent_dir_name_1, file_name_1, file_size_1)
            print()
            print(message)

        self._make_new_thread(thread_method, (parent_dir_name, file_name, file_size))

    def _add_dir(self):
        """
        Adds a new directory to the system and prints a message upon success or failure
        Runs on a separate thread
        """
        parent_dir_name = self._var_input("Insert parent directory name:", str)
        dir_name = self._var_input("Insert directory name  (String 32 letters max):", str, lambda x: len(x) < 32)

        def thread_method(parent_dir_name_1, dir_name_1):
            message, created = self._root_directory.add_directory(parent_dir_name_1, dir_name_1)
            print()
            print(message)

        self._make_new_thread(thread_method, args=(parent_dir_name, dir_name))

    def _exit(self):
        """
        Exits the system
        """
        print("Goodbye!")
        return True

    def _delete(self):
        """
        Deletes a file/directory from the system
        """
        name = self._var_input("Insert file/directory name:", str)

        def thread_method(name_1):
            message = self._root_directory.delete(name_1)
            print()
            print(message)

        self._make_new_thread(thread_method, args=(name,))

    def _show_file_system(self):
        """
        Prints the system layout with details on every directory/file
        """
        def thread_method():
            sleep(1)
            print()
            self._root_directory.show_file_system()
        self._make_new_thread(thread_method)

    @classmethod
    def _var_input(cls, message, var_type, constrains_func=None):
        """
        Parses the user input
        Will keep asking if input is not valid
        :param message: Message to display to the user
        :param var_type: The type that is requested
        :param constrains_func:  Any special constrains, optional
        :return: a valid variable
        """
        while True:
            try:
                var = input(message)
                var = var_type(var)
                if constrains_func is None or constrains_func(var) is True:
                    return var
                else:
                    print("Constrains not met!")
            except Exception:
                print("Wrong type entered!")
