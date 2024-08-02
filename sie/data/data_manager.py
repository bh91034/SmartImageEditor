import os
import shutil

from sie.data.data_util import FolderData


class DataManager:
    """
    This class is designed as 'Singleton pattern'.
    Reference: https://wikidocs.net/69361
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):             # 클래스 객체에 _init 속성이 없다면
            # 최초로 생성된 instance 에 의해서만 한번 불림
            cls._init = True
            self.__init()
        # 일반적인 생성자에서 처리할 부분을 여기에 처리(중복해서 불리는 부분임)
    
    def __init(self):
        curr_path = os.getcwd()
        default_image_path = curr_path + os.sep + "data" + os.sep + "images"
        self.__reset_work_folder(target_folder=default_image_path)
    
    def __reset_work_folder(self, target_folder):
        print ('[DataManager.reset] reset, target=', target_folder)
        target_path = os.path.abspath(target_folder)
        self.__folder_data = FolderData(target_path)
        self.__init_output_folder(target_path)
    
    def __init_output_folder(self, target_folder):
        print ('[DataManager] initOutputFiles() called...')
        print ('[DataManager] initOutputFiles() : target_folder = ', target_folder)

        output_folder = os.path.join(target_folder + os.sep + '__OUTPUT_FILES__')
        print ('[DataManager] initOutputFiles() : output_folder = ', output_folder)

        # create output folder if not exist
        if os.path.isdir(output_folder) == False:
            os.makedirs(output_folder)
            print ('[DataManager] initOutputFiles() : output_folder newly created!')
        
        if target_folder == None or len(target_folder) == 0:
            print ('[DataManager] initOutputFiles() : no source files!')
            return
        
        # copy files to output folder if source image file doesn't exist in output folder
        target_images = [file_data.to_string() for file_data in self.__folder_data.get_files()]
        for src_file in target_images:
            src_file_name = os.path.basename(src_file)
            out_file = os.path.join(target_folder, '__OUTPUT_FILES__', src_file_name)
            if not os.path.isfile(out_file):
                shutil.copy(src_file, out_file)

    def get_work_folder(self):
        return self.__folder_data

    def get_output_folder(self):
        print ('[DataManager] get_output_file() called...')
        out_file_dir = self.__folder_data.to_string()
        return os.path.join(out_file_dir, '__OUTPUT_FILES__')

    def get_work_file(self):
        return self.__folder_data.get_work_file()

    def get_output_file(self):
        print ('[DataManager] get_output_file() called...')
        out_file_name = os.path.basename(self.__folder_data.get_work_file().to_string())
        return os.path.join(self.get_output_folder(), out_file_name)
