import os
import shutil

from sie.data.data_util import FolderData


class DataManager:
    """
    This class responsible for managing file paths and directories for data processing.

    This class follows the Singleton pattern to ensure that only one instance is created throughout 
    the application. 

    Reference:
        https://wikidocs.net/69361
    """

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the class if it doesn't already exist, otherwise returns the existing instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Variable length keyword arguments.

        Returns:
            DataManager: The singleton instance of the `DataManager` class.
        """
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the singleton instance of the `DataManager` class.

        This method sets up the working folder and output folder. It ensures that initialization is only 
        performed once by checking the `_init` attribute on the class object.
        """
        cls = type(self)
        if not hasattr(cls, "_init"):  # Ensure initialization only happens once
            cls._init = True
            self.__init()
        # Additional initialization code (if needed) can be placed here

    def __init(self):
        """
        Initializes the working folder and output folder settings.

        Sets the default image path based on the current working directory and resets the working folder.
        """
        curr_path = os.getcwd()
        default_image_path = os.path.join(curr_path, "data", "images")
        self.__reset_work_folder(target_folder=default_image_path)

    def __reset_work_folder(self, target_folder):
        """
        Resets the working folder to the specified target folder.

        Args:
            target_folder (str): The path to the target folder to reset as the working folder.

        This method initializes the output folder and ensures it is set up properly.
        """
        print('[DataManager.reset] reset, target=', target_folder)
        target_path = os.path.abspath(target_folder)
        self.__folder_data = FolderData(target_path)
        self.__init_output_folder(target_path)

    def __init_output_folder(self, target_folder):
        """
        Initializes the output folder within the specified target folder.

        Args:
            target_folder (str): The path to the target folder where the output folder should be created.

        Creates the output folder if it does not already exist and copies files from the source folder 
        to the output folder if they are not present.
        """
        print('[DataManager] initOutputFiles() called...')
        print('[DataManager] initOutputFiles() : target_folder = ', target_folder)

        output_folder = os.path.join(target_folder, '__OUTPUT_FILES__')
        print('[DataManager] initOutputFiles() : output_folder = ', output_folder)

        # Create output folder if it does not exist
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)
            print('[DataManager] initOutputFiles() : output_folder newly created!')
        
        if not target_folder:
            print('[DataManager] initOutputFiles() : no source files!')
            return
        
        # Copy files to the output folder if they do not already exist there
        target_images = [file_data.to_string() for file_data in self.__folder_data.get_files()]
        for src_file in target_images:
            src_file_name = os.path.basename(src_file)
            out_file = os.path.join(target_folder, '__OUTPUT_FILES__', src_file_name)
            if not os.path.isfile(out_file):
                shutil.copy(src_file, out_file)

    def get_work_folder(self):
        """
        Retrieves the current working folder data.

        Returns:
            FolderData: An instance of the `FolderData` class representing the working folder.
        """
        return self.__folder_data

    def get_output_folder(self):
        """
        Retrieves the path to the output folder.

        Returns:
            str: The path to the output folder within the working folder.
        """
        print('[DataManager] get_output_file() called...')
        out_file_dir = self.__folder_data.to_string()
        return os.path.join(out_file_dir, '__OUTPUT_FILES__')

    def get_work_file(self):
        """
        Retrieves the current working file.

        Returns:
            FileData: An instance of the `FileData` class representing the current working file.
        """
        return self.__folder_data.get_work_file()

    def get_output_file(self):
        """
        Retrieves the path to the current output file.

        Returns:
            str: The path to the output file in the output folder, corresponding to the current working file.
        """
        print('[DataManager] get_output_file() called...')
        out_file_name = os.path.basename(self.__folder_data.get_work_file().to_string())
        return os.path.join(self.get_output_folder(), out_file_name)
