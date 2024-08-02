import glob

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

    def get_texts_as_string(self):
        return [t.get_text()  for t in self.__texts]

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