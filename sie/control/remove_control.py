from sie.gui.subframes.remove_frame import *
from sie.data.data_manager import DataManager
from sie.gui.utils.canvas_util import PostDrawListner


class RemovePostDrawHandler(PostDrawListner):
    def do_post_draw(self, canvas, image_reduced_ratio):
        print(f'RemovePostDrawHandler.do_post_draw() : reduced_ratio={image_reduced_ratio}')
        
        # get position info for the selected texts
        from sie.gui.gui_manager import GuiManager
        remove_frame = GuiManager().get_low_frame().get_remove_frame()

        if remove_frame.get_check_list().get_type() == ScrollableListType.CHECK_BUTTON:
            check_items = remove_frame.get_check_list().get_check_vars().items()
            idx = 0
            for item, var in check_items:
                if var.get() == 1:
                    position_info = DataManager().get_work_file().get_text_by_index(idx).get_position_info()
                    canvas.draw_rect(position_info)
                idx += 1
        if remove_frame.get_check_list().get_type() == ScrollableListType.RADIO_BUTTON:
            radio_var = remove_frame.get_check_list().get_radio_var()
            val = None
            if radio_var:
                val = radio_var.get()
            print(f'########> RADIO VAR={radio_var}, get={val}')

class RemoveTextListHandler(ScrollableListListener):
    def on_list_selected(self, index, text):
        print(f'RemoveTextListHandler.on_list_selected() : index={index}, text={text}')

        # redraw images to draw rect for selected text in work image
        from sie.gui.gui_manager import GuiManager
        GuiManager().get_mid_frame().redraw_images()


class RemoveControl:
    def clicked_search_text():
        
        # TODO: search OCR text from the image (now, fake sample data is used)
        test_list = [
                ([[24, 48], [345, 48], [345, 109], [24, 109]], '下载手机天猫APP', 0.8471784057548907), 
                ([[24, 130], [368, 130], [368, 204], [24, 204]], '享388元礼包', 0.9837027854197318), 
                ([[190, 306], [290, 306], [290, 336], [190, 336]], '立即扫码', 0.9933473467826843), 
                ([[160, 348], [334, 348], [334, 372], [160, 372]], '下载手机天猫APP领福利', 0.858102917437849)
            ]
        
        # set text data to data manager
        work_file = DataManager().get_work_file()
        work_file.set_texts(test_list)
        text_list = work_file.get_texts_as_string()

        # update list
        from sie.gui.gui_manager import GuiManager
        remove_frame = GuiManager().get_low_frame().get_remove_frame()
        remove_frame.reset_text_list(text_list)
