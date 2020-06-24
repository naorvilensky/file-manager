# toga-file-manager

## Classes:

### Entity: 
    Abstract class for an Entity (File or Directory)

#### methods:

- name: 
    - Getter and Setter for name of entity

- creation_date:
    - Getter for creation date

- show_date(i: int)
    - Shows the data of the entity
    - param i: number of line breaks
    - raises NotImplementedError

### File:
        Class representing a File entity
        extends _Entity

#### methods:

- show_data(i: int)
    - same as abstracts method

- size
    - Getter and Setter for size of file

### Directory:
        Class representing a Directory entity
        extends _Entity

#### methods:

- show_data(i: int)
    - same as abstracts method
    
- internal_entities
    - Getter for internal entities of the directory
    
- add_file(parent_dif_name: str, file_name: str, file_size: int)
    - Add a new file to the directory
    - param parent_dir_name: the path of the parent directory
    - param file_name: the name of the file
    - param file_size: the size of the file
    - return: a tuple with (message, created)
    
- add_directory(parent_dir_name: str, dir_name: str)
    - Add a new directory to the directory
    - param parent_dir_name: the path of the parent directory
    - param dir_name: the name of the directory
    - return: a tuple with (message, created)
    
- delete(name: str):
    - Deletes a file/directory
    - param name: the name of file/directory to delete
    - return: message with the status after the delete

- find_path(name: str, entity_path=None):
    - Finds the path of a given file/directory
    - param name: the name of the file/directory
    - param entity_path: the path for now of the entity (not needed used for recursion)
    - return: a tuple with (the path of the entity, the type of entity, internal_entities of the parent directory)
 
- show_file_system():
    - Prints out the file system

### FileManager
        The File Manager to change entities on the drive

- delete_entity(entity_path: list, entity_class, root):
    - class method
    - Deletes the entity
    - param entity_path: the path to the entity
    - param entity_class: the type of the entity
    - param root: the root directory
    - return: True if deleted False otherwise

- check_if_path_exists(dir_path: str):
    - class method
    - Checks if the path exists on the drive
    - param dir_path: the drive path
    - return: True if the path exists False if not

- create_file(parent_dir_path: list, file_name):
    - class method
    - Creates a file
    - param parent_dir_path: the path to the parent directory
    - param file_name: the name of the file
    - return: tuple (message, created)
    
- create_dir(parent_dir_path: list, dir_name):
    - class method
    - Created a directory
    - param parent_dir_path: the path to the parent directory
    - param dir_name: the name of the directory
    - return: tuple (message, created)
    
- add_entity(instance, entity_class, parent_dir_path: list, entity_name: str, file_size: int = None, i: int = 1):
    - class method
    - Creates an entity
    - param instance: an instance of the directory
    - param entity_class: the class of the entity
    - param parent_dir_path: the path of the entity
    - param entity_name: the name of the entity
    - param file_size: the file size (if a file is given)
    - param i: the index of the path currently
    - return: tuple (message, created)
    
### InputParser
    Class to parse the given input from the user

- request_input():
    - Requests input from the user until the user decides to exit
    - every input is then delivered to the corresponding method mapped with get_input_map()

## Architecture Overview:
- Both File and Directory extend _Entity as they are described Entities.
- A Directory can hold both Files and Directories and a dedicated dict object.
- The FileManager is used by Directory for the creation of new Files and Directories
on the drive, as well as adding them to the dedicated dict object for the corresponding directory.
- Input parser sends those commands to the root directory.
- The root directory is the directory object that holds all the files and directories that are going to be created.