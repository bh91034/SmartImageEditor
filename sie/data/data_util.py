import glob


class FolderData:
    """
    This class is designed to manage a working folder used for image editing tasks.
    Initially, a pre-saved folder in this repository (./data/images) is used, 
    but it can be changed to another folder by the user. 
    
    There can be only one working folder, which can be modified by the user. 
    All folder paths are handled as absolute paths.

    The files within the folder are managed in the __files variable 
    as a list of instances of the FileData class.
    """
    def __init__(self, path):
        self.__folder_name = path   # The path of the folder: absolute path.
        self.__files = []           # The list of FileData class instance
        self.__work_file = None     # FileData class instance
        self.__init_work_folder()   # 

    def __str__(self):
        return self.__folder_name

    def to_string(self):
        return self.__folder_name

    def __init_work_folder(self):
        FILE_EXT = ['png', 'jpg', 'gif']
        target_files = []
        [target_files.extend(glob.glob(self.__folder_name + '/' + '*.' + e)) for e in FILE_EXT]

        # Sorting
        target_files.sort()

        # List up instances of FileData
        for tf in target_files:
            self.__files.append(FileData(tf)) # tf: file's absolute path(full path)
        
        # Assign work file
        if len(self.__files) > 0:
            self.__work_file = self.__files[0]

    def get_work_file(self):
        """
        Returns an instance of the `FileData` class for the image file currently 
        in use in the working directory.

        Returns:
            FileData: An instance of the `FileData` class for the currently used image file,
                    or None if no file is in use.
        """        
        return self.__work_file
        
    def get_files(self):
        """
        Returns a list of `FileData` class instances for all files in the current working directory.

        Returns:
            List[FileData]: A list of `FileData` instances for all files in the current working directory.
        """
        return self.__files
    
    def get_file_by_index(self, index):
        return self.__files[index]


class FileData:
    """
    All file paths are handled as absolute paths.
    """
    def __init__(self, file):
        """
        Args:
            file (str): The file path provided is an absolute path.
        """        
        self.__file_name = file
        self.__texts = []
        self.__is_ocr_executed = False

    def __str__(self):
        return self.__file_name

    def to_string(self):
        return self.__file_name

    def is_ocr_executed(self):
        return self.__is_ocr_executed        
        
    def set_texts(self, ocr_texts):
        """
        Sets the OCR text data for this file.

        Args:
            ocr_texts (list of tuples): A list where each tuple contains:
                - A list of four coordinate pairs representing the bounding box of the text in the image.
                - A string representing the recognized text.
                - A float representing the confidence score of the text recognition.
            
            Example:
                [
                    ([[24, 48], [345, 48], [345, 109], [24, 109]], 'Downloaded Tmall App', 0.847),
                    ([[24, 130], [368, 130], [368, 204], [24, 204]], '388 Yuan Gift Pack', 0.984),
                    ([[190, 306], [290, 306], [290, 336], [190, 336]], 'Scan Now', 0.993),
                    ([[160, 348], [334, 348], [334, 372], [160, 372]], 'Download Tmall App for Benefits', 0.858)
                ]
        """
        self.__texts = []
        for t in ocr_texts:
            self.__texts.append(TextData(t[1], t[0]))
        self.__is_ocr_executed = True

    def get_texts(self):
        """
        Returns a list of `TextData` objects.

        The `TextData` objects encapsulate information related to text data, such as text content,
        bounding box coordinates, and confidence score.

        Returns:
            list of TextData: A list of `TextData` instances containing the text information.
        """
        return self.__texts     # TextData 객체 반환
    
    def get_text_by_index(self, index):
        """
        Returns a `TextData` object at a specific index.

        Args:
            index (int): The index of the `TextData` object to retrieve.

        Returns:
            TextData: The `TextData` object at the specified index.
        """
        return self.__texts[index]      # TextData 객체 반환

    def get_texts_as_string(self):
        """
        Returns a list of text strings from the `TextData` objects.

        Returns:
            list of str: A list of text strings extracted from `TextData` objects.
        """
        return [t.get_text()  for t in self.__texts]


class TextData:
    """
    Represents text data extracted from an image, including the recognized text and its position.

    Attributes:
        __text (str): The recognized text.
        __tr_text (str or None): Optional field for translated text, default is None.
        __position_info (list of lists): List of coordinate pairs representing the bounding box of the text.
    """
    
    def __init__(self, text, position):
        """
        Initializes a `TextData` instance.

        Args:
            text (str): The recognized text.
            position (list of lists): A list of four coordinate pairs representing the bounding box of the text.
                Example: [[24, 48], [345, 48], [345, 109], [24, 109]]
        """
        self.__text = text
        self.__tr_text = None
        self.__position_info = position

    def get_text(self):
        """
        Returns the recognized text.

        Returns:
            str: The recognized text.
        """
        return self.__text

    def get_position_info(self):
        """
        Returns the position information of the text.

        Returns:
            list of lists: A list of four coordinate pairs representing the bounding box of the text.
        """
        return self.__position_info

    def get_tr_text(self):
        """
        Returns the translated text, if available.

        Returns:
            str or None: The translated text, or None if translation is not available.
        """
        return self.__tr_text