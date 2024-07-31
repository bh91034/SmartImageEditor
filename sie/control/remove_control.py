
from sie.gui.subframes.remove_frame import *

class RemoveTextListHandler(ScrollableListListener):
    def on_list_selected(self, index, text):
        print(f'RemoveTextListHandler.on_list_selected() : index={index}, text={text}')

class RemoveControl:
    def clicked_search_text():
        
        # TODO: search OCR text from the image (now, fake data is used)
        test_list = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL"]

        # update list
        from sie.gui.gui_manager import GuiManager
        remove_frame = GuiManager().get_low_frame().get_remove_frame()
        remove_frame.reset_text_list(test_list)
