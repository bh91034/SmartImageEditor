import glob
import os
import shutil

class FolderData:
    """
    본 Class는 이미지 편집 작업에 사용될 작업 폴더(folder) 를 관리하는 목적의 class 이다.
    최초에는 본 repository 에 미리 저장된 폴더(./data/images)가 사용되며, 사용자에 의해 다른 폴더로 변경이 가능하다.
    작업 폴더는 하나만 존재하며, 사용자에 의해서 변경이 가능하다.
    모든 folder 경로는 절대 경로(absolute path)로 다루어 진다.

    폴더 안에 존재하는 파일들을 FileData 클래스의 instance list 형태로 __files 변수에서 관리한다.
    """
    def __init__(self, path):
        self.__folder_name = path   # Folder 의 경로(text string), 절대경로(absolute path) 임
        self.__files = []           # FileData 객체의 list를 의미
        self.__work_file = None     # FileData 객체
        self.__init_work_folder()   # 

    def __str__(self):
        return self.__folder_name

    def to_string(self):
        return self.__folder_name

    def __init_work_folder(self):
        FILE_EXT = ['png', 'jpg', 'gif']
        target_files = []
        [target_files.extend(glob.glob(self.__folder_name + '/' + '*.' + e)) for e in FILE_EXT]

        # sorting
        target_files.sort()

        # FileData 목록 만들기
        for tf in target_files:
            self.__files.append(FileData(tf))
        
        # work file 지정
        if len(self.__files) > 0:
            self.__work_file = self.__files[0]

    def get_work_file(self):
        """
        Return 현재 작업 폴더에서 화면에 작업중인 이미지 파일의 FileData class의 instance를 반환.
        """
        return self.__work_file
        
    def get_files(self):
        """
        Return 현재 작업 폴더의 모든 파일에 대한 FileData class의 instance 목록(list)을 반환.
        """
        return self.__files     # FileData 반환
    
    def get_file_by_index(self, index):
        return self.__files[index]      # FileData 반환

class FileData:
    """
    모든 file 경로는 절대 경로(absolute path)로 다루어 진다.
    """
    def __init__(self, file):
        self.__file_name = file        # File 의 경로(text string), 절대경로(absolute path) 임
        self.__texts = []              # TextData 객체를 의미
        self.__is_ocr_executed = False

    def __str__(self):
        return self.__file_name

    def to_string(self):
        return self.__file_name

    def is_ocr_executed(self):
        return self.__is_ocr_executed        
        
    def set_texts(self, ocr_texts):
        """
        param ocr_texts: 
            ocr_texts 은 아래와 같은 형태의 data 구조로 들어온다.
            [
                ([[24, 48], [345, 48], [345, 109], [24, 109]], '下载手机天猫APP', 0.8471784057548907), 
                ([[24, 130], [368, 130], [368, 204], [24, 204]], '享388元礼包', 0.9837027854197318), 
                ([[190, 306], [290, 306], [290, 336], [190, 336]], '立即扫码', 0.9933473467826843), 
                ([[160, 348], [334, 348], [334, 372], [160, 372]], '下载手机天猫APP领福利', 0.858102917437849)
            ]
        """
        self.__texts = []
        for t in ocr_texts:
            self.__texts.append(TextData(t[1], t[0]))
        self.__is_ocr_executed = True

    def get_texts(self):
        return self.__texts     # TextData 객체 반환
    
    def get_text_by_index(self, index):
        return self.__texts[index]      # TextData 객체 반환
    
class TextData:
    def __init__(self, text, position):
        self.__text = text
        self.__tr_text = None
        self.__position_info = position  # Example: [[24, 48], [345, 48], [345, 109], [24, 109]]
        
    def get_text(self):
        return self.__text

    def get_position_info(self):
        return self.__position_info

    def get_tr_text(self):
        return self.__tr_text
    
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
