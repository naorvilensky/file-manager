from abc import ABC, abstractmethod
from datetime import datetime
import os
from os import path, makedirs


def line_breaks(i: int):
    """
    Creates the line breaks '-' according to the number given
    :param i: the number of line breaks to show
    :return: the corresponding number of line breaks
    """
    return '-' * i + ' '


def format_creation_date(date: datetime):
    return date.strftime('%c')


class _Entity(ABC):
    """
    Abstract class to represent all the entities
    """
    _name: str
    _creation_date: datetime

    def __init__(self, name: str):
        """
        Basic init of an entity
        :param name: the name of the entity
        """
        self._creation_date = datetime.today()
        self.name = name

    @property
    def name(self) -> str:
        """
        Getter for the name
        :return: the name of the entity
        """
        return self._name

    @name.setter
    def name(self, n: str):
        """
        Setter for the name
        :param n: the name to set
        """
        if n is not None and len(n) < 32:
            self._name = n
        else:
            print("Name is not valid")

    @property
    def creation_date(self) -> datetime:
        """
        Getter for the creation date
        :return: The creation date
        """
        return self._creation_date

    @abstractmethod
    def show_data(self, i: int):
        """
        Shows the data
        :raises NotImplementedError
        """
        raise NotImplementedError


class File(_Entity):
    """
    Class representing a File entity
    """

    def show_data(self, i: int):
        """
        Shows the data of the file
        :param i: number of line breaks
        """
        breaks = line_breaks(i)
        print(breaks + ' | Name: ' + str(self.name))
        print(breaks + ' | Type: File')
        print(breaks + ' | Creation Date: ' + format_creation_date(self.creation_date))
        print(breaks + ' | Size: ' + str(self.size))

    _size: int

    def __init__(self, name, size):
        """
        Creates the File entity
        :param name: the name of the File
        :param size: the size of the File
        """
        super().__init__(name)
        self.size = size

    @property
    def size(self) -> int:
        """
        Getter for the size
        :return: the size of the file
        """
        return self._size

    @size.setter
    def size(self, s: int):
        """
        Setter for the size of the File
        :param s: the size of the file
        """
        if s is not None and s > 0:
            self._size = s
        else:
            print("Size is not valid")


class Directory(_Entity):
    """
    Class representing a File entity
    """

    def show_data(self, i: int):
        """
        Shows the data of the directory
        :param i: number of line breaks
        """
        breaks = line_breaks(i)
        print(breaks + " | Name: " + str(self.name))
        print(breaks + ' | Creation Date: ' + format_creation_date(self.creation_date))
        print(breaks + " | Type: Directory")

    _internal_entities: dict
    _root: str

    def __init__(self, name: str, root: str = ''):
        """
        Created the directory
        :param name: the name of the directory
        :param root: the root of the directory (optional)
        """
        self._root = root
        if root and not FileManager.check_if_path_exists(root):
            raise Exception('Path does not exist!')
        super().__init__(name)
        self._internal_entities = dict()

    @property
    def internal_entities(self):
        """
        Getter for the internal entities of the directory
        :return: the internal entities of the directory
        """
        return self._internal_entities

    def add_file(self, parent_dir_name: str, file_name: str, file_size: int):
        """
        Add a new file to the directory
        :param parent_dir_name: the path of the parent directory
        :param file_name: the name of the file
        :param file_size: the size of the file
        :return: a tuple with (message, created)
        """
        parent_dir_path = parent_dir_name.split('/')
        if parent_dir_path[0] != self._root:
            parent_dir_path.insert(0, self._root)
        message, created = FileManager.add_entity(self, File, parent_dir_path, file_name,
                                                  file_size)
        return message, created

    def add_directory(self, parent_dir_name: str, dir_name: str):
        """
        Add a new directory to the directory
        :param parent_dir_name: the path of the parent directory
        :param dir_name: the name of the directory
        :return: a tuple with (message, created)
        """
        parent_dir_path = parent_dir_name.split('/')
        if parent_dir_path[0] != self._root:
            parent_dir_path.insert(0, self._root)
        message, created = FileManager.add_entity(self, Directory, parent_dir_path, dir_name)
        return message, created

    def delete(self, name: str):
        """
        Deletes a file/directory
        :param name: the name of file/directory to delete
        :return: message with the status after the delete
        """
        entity_path, entity_type, internal_entities = self.find_path(name)
        if entity_path is not None:
            entity_path.append(name)
            FileManager.delete_entity(entity_path, entity_type, self._root)
            internal_entities.pop(name, None)
            return 'Deleted!'
        return str(name) + ' Not found!'

    def find_path(self, name: str, entity_path=None):
        """
        Finds the path of a given file/directory
        :param name: the name of the file/directory
        :param entity_path: the path for now of the entity (not needed used for recursion)
        :return: a tuple with (the path of the entity, the type of entity, internal_entities of the parent directory)
        """
        if entity_path is None:
            entity_path = []

        for d in self.internal_entities.values():
            if d.name == name:
                entity_path.append(self.name)
                return entity_path, type(d), self.internal_entities

            if type(d) is Directory:
                lookup_path, lookup_type, internal_entities = d.find_path(name, entity_path)
                if lookup_path is not None:
                    return lookup_path, lookup_type, internal_entities

        return None, None, None

    def show_file_system(self):
        """
        Prints out the file system
        """
        self._show_file_system_helper(self)

    @classmethod
    def _show_file_system_helper(cls, d, i: int = 1):
        """
        Recursive helper to print out the file system
        :param d:
        :param i:
        :return:
        """
        d.show_data(i)

        for internal in d.internal_entities.values():
            if type(internal) is Directory:
                cls._show_file_system_helper(internal, i + 1)
            else:
                internal.show_data(i + 1)


class FileManager:
    """
    The File Manager to change entities on the drive
    """
    @classmethod
    def delete_entity(cls, entity_path: list, entity_class, root):
        """
        Deletes the entity
        :param entity_path: the path to the entity
        :param entity_class: the type of the entity
        :param root: the root directory
        :return: True if deleted False otherwise
        """
        try:
            joined_path = path.join(root, *entity_path)
            if entity_class is Directory:
                os.rmdir(joined_path)
            if entity_class is File:
                os.remove(joined_path)
            return True
        except FileNotFoundError:
            print('File/Directory not found!')
            return False

    @classmethod
    def check_if_path_exists(cls, dir_path: str):
        """
        Checks if the path exists on the drive
        :param dir_path: the drive path
        :return: True if the path exists False if not
        """
        return path.isdir(dir_path)

    @classmethod
    def create_file(cls, parent_dir_path: list, file_name):
        """
        Creates a file
        :param parent_dir_path: the path to the parent directory
        :param file_name: the name of the file
        :return: tuple (message, created)
        """
        try:
            f = open(path.join(*parent_dir_path, file_name), 'x')
            f.close()
            return 'File created!', True
        except FileExistsError:
            return 'file already exists!', False

    @classmethod
    def create_dir(cls, parent_dir_path: list, dir_name):
        """
        Created a directory
        :param parent_dir_path: the path to the parent directory
        :param dir_name: the name of the directory
        :return: tuple (message, created)
        """
        try:
            makedirs(path.join(*parent_dir_path, dir_name))
            return 'Directory created!', True
        except FileExistsError:
            return 'Directory already exists!', False

    @classmethod
    def add_entity(cls, instance, entity_class, parent_dir_path: list,
                   entity_name: str,
                   file_size: int = None,
                   i: int = 1):
        """
        Creates an entity
        :param instance: an instance of the directory
        :param entity_class: the class of the entity
        :param parent_dir_path: the path of the entity
        :param entity_name: the name of the entity
        :param file_size: the file size (if a file is given)
        :param i: the index of the path currently
        :return: tuple (message, created)
        """
        if i == len(parent_dir_path):
            entity = instance.internal_entities.get(entity_name)
            if entity is None:
                message, created = None, None
                entity = None
                if entity_class is Directory:
                    message, created = FileManager.create_dir(parent_dir_path, entity_name)
                    entity = Directory(entity_name)
                if entity_class is File:
                    message, created = FileManager.create_file(parent_dir_path, entity_name)
                    entity = File(entity_name, file_size)
                if created:
                    instance.internal_entities[entity_name] = entity
                return message, created
            return 'File already exists', False
        directory = instance.internal_entities.get(parent_dir_path[i])
        if type(directory) is Directory:
            return cls.add_entity(directory, entity_class, parent_dir_path, entity_name, file_size, i + 1)
        print(f'Path {"/".join(parent_dir_path[i:])} not found')
        return None, False
