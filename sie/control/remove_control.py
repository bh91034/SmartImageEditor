from sie.gui.subframes.remove_frame import *
from sie.data.data_manager import DataManager
from sie.gui.utils.canvas_util import PostDrawListner


class RemovePostDrawHandler(PostDrawListner):
    def do_post_draw(self, canvas, image_reduced_ratio):
       
        # get selected items
        from sie.gui.gui_manager import GuiManager
        check_list = GuiManager().get_low_frame().get_remove_frame().get_check_list()
        selected_items = check_list.get_selected_items()
        if selected_items is None or len(selected_items) == 0:
            return

        # draw rect on image for selected text
        for item in selected_items:
            position_info = DataManager().get_work_file().get_text_by_index(item["index"]).get_position_info()
            canvas.draw_rect(position_info)


class RemoveTextListListener(ScrollableListListener):
    def on_state_changed(self, index, text, state, selected_items):
        print(f'RemoveTextListListener.on_list_selected() : index={index}, text={text}, state={state}')
        if selected_items is not None and len(selected_items) > 0:
            for idx, item in enumerate(selected_items):
                print(f'     - index={item["index"]}, text={item["text"]}')

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
