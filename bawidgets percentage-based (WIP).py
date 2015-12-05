
#include this file then make a subclass of BAWidgetProgram (for example see baspriteframer)
import os
import pygame

program = None
screen = None
is_visual_debug = False

def draw():
    blit_widget(screen,program.trunk_widget)

def set_BAWidgetProgram(bawidgetprogram):
    global program
    program = bawidgetprogram
    #result = None
    #return result

class BAWidgetProgram:
    font = None
    display_size = None
    antialias = None
    trunk_widget = None
    
    def __init__(self, display_size):
        global screen
        self.antialias = True
        self.display_size = display_size
        pygame.init()
        screen = pygame.display.set_mode(display_size)
        if not pygame.font: print('Warning, fonts disabled')
        else:
            self.font = pygame.font.Font(None, 30)
        self.trunk_widget = BAWidget("trunk", pygame.Rect(0,0,display_size[0],display_size[1]), None)

class BAWidget:
    rect = None
    size = None
    align = None
    subwidgets = None
    form = None
    result = None
    container = None
    handler = None
    last_clicked_key = None
    image = None
    text = None
    name = None
    index = None
    key = None
    folder = None
    file_count = None
    kind = None
    value = None
    last_x = 0
    last_y = 0
    listing_path = None
    desired_target = None
    enabled = None
    margin = None
    padding = None
    background_color = None
    
    def add_widget(self, subwidget_widget):
        if isinstance(subwidget_widget, BAWidget):
            subwidget_widget.index = len(self.subwidgets)
            self.subwidgets.append(subwidget_widget)
            subwidget_widget.container = self
        else:
            print("ERROR: non-widget sent to add_widget, so nothing done.") 
    
    def __init__(self, name, size, on_form):
        self.form = on_form
        self.name = name
        self.size = size
        self.subwidgets = list()
        self.enabled = True
        self.align = 'vertical'
        self.margin = (.01, .01, .01, .01)
        self.padding = (.01, .01, .01, .01)
        #try:
        #    self.image = pygame.Surface( (self.rect.width,self.rect.height) )
        #except:
        #    print("Could not finish BAWidget surface with rect: "+str(self.rect))
    
    def set_form_list_path_to_key(self):
        if self.container is not None:
            self.container.set_list_path(self.key)
            #self.container.listing_path = self.key
            ##self.container.set_last_clicked_key(self.key)
            #self.container.list_files()

    def set_list_path(self, val):
        self.listing_path = val
        #self.set_last_clicked_key(val)
        self.list_files()
    
    def set_last_clicked_key(self, set_last_clicked_key):
        is_ok_target = False
        if self.desired_target is None:
            self.last_clicked_key = set_last_clicked_key
            self.set_ok_enabled(True)
        elif self.desired_target == "file":
            if os.path.isfile(set_last_clicked_key):
                self.last_clicked_key = set_last_clicked_key
                self.set_ok_enabled(True)
            else:
                self.set_ok_enabled(False)
                self.set_list_path(set_last_clicked_key)
        elif self.desired_target == "folder":
            if os.path.isdir(self.last_clicked_key):
                self.last_clicked_key = set_last_clicked_key
                self.set_ok_enabled(True)
                #still set_list_path in case a subfolder is desired instead:
                self.set_list_path(set_last_clicked_key)
            else:
                self.set_ok_enabled(False)
        return is_ok_target
    
        
    def set_ok_enabled(self,set_is_enabled):
        
        this_button = self.get_subwidget_by_key("ok")
        if this_button is not None:
            this_button.enabled = set_is_enabled
            text_image = None
            if set_is_enabled:
                this_button.image.fill( (128,128,192,255) )
                text_image = program.font.render( this_button.text, program.antialias, (0,0,0,128))
            else:
                this_button.image.fill( (128,128,128,255) )
                text_image = program.font.render( this_button.text, program.antialias, (192,192,192,128))
            text_rect = text_image.get_rect()
            this_button.image.blit( text_image, ((this_button.rect.width-text_rect.width)/2,(this_button.rect.height-text_rect.height)/2) )

            
        else:
            print("no ok button in "+self.name+":")
            for sub in self.subwidgets:
                print("  - "+str(sub.key)+":"+str(sub.name))
    
    def set_form_last_clicked_to_key(self):
        if self.form is not None:
            if self.key is not None:
                self.form.set_last_clicked_key(self.key)
            else:
                self.form.set_last_clicked_key(self.text)
            #print("set form last clicked key:"+str(self.form.last_clicked_key))
            #print("  self.key:"+str(self.key))
            #print("  self.text:"+str(self.text))
            

    def index_of_subwidget_by_kind(self, val):
        result = None
        for index in range(0,len(self.subwidgets)):
            item = self.subwidgets[index]
            if item.kind == val:
                result = index
                break
        return result
    
    def index_of_subwidget_by_text(self, text, is_case_sensitive = False):
        result = None
        for index in range(0,len(self.subwidgets)):
            item = self.subwidgets[index]
            if is_case_sensitive:
                if item.text is not None:
                    if item.text == text:
                        result = index
                        break
            else:
                text_lower = text.lower()
                if item.text is not None:
                    if item.text.lower() == text_lower:
                        result = index
                        break
        return result
    
    def get_subwidget_by_key(self, key):
        result = None
        index = self.index_of_subwidget_by_key(key)
        if index is not None:
            result = self.subwidgets[index]
        return result
    
    def index_of_subwidget_by_key(self, key):
        result = None
        for index in range(0,len(self.subwidgets)):
            item = self.subwidgets[index]
            if item.key is not None:
                if item.key == key:
                    result = index
                    break
        return result
    
    def get_subwidget_by_kind(self, val):
        result = None
        index = self.index_of_subwidget_by_kind(val)
        if index is not None:
            result = self.subwidgets[index]
        return result
        
    def get_subwidget_by_text(self, text, is_case_sensitive):
        result = None
        index = self.index_of_subwidget_by_text(text, is_case_sensitive)
        if index is not None:
            result = self.subwidgets[index]
        return result
    
    def clear_listitems(self):
        index = True
        #print("clearing listitems...")
        while index is not None:
            index = self.index_of_subwidget_by_kind("listitem")
            if index is not None:
                self.subwidgets.pop(index)
        #print("done (cleared listitems)")

    def form_list_files_starting_at_value(self):
        if self.form is not None:
            self.form.list_files(self.value)
    
    def list_files(self, start_index = 0):
        self.clear_listitems()
        element_padding = 8
        dialog = self
        #dialog = None
        #dialog_index = self.index_of_subwidget_by_kind("dialog")
        #if dialog_index is not None:
        #    dialog = self.subwidgets[dialog_index]
            
        if dialog is not None:
            self.last_x = dialog.rect.left+element_padding
            self.last_y = dialog.rect.top+element_padding
            any_button = self.get_subwidget_by_kind("button")
            buttons_top = program.display_size[1]
            if any_button is not None:
                buttons_top = any_button.rect.top
            else:
                print("no buttons, so clipping file list to "+str(buttons_top))
            
            #list_rect = pygame.Rect(self.last_x, self.last_y, dialog.rect.width-element_padding*2, buttons_top-self.last_y-element_padding)
            files_widget = BAWidget("files_widget", (1.0,.8), dialog)
            files_widget.background_color = (1.0,1.0,1.0,1.0)
            #files_widget.image.fill( (255,255,255,255) )
            #dialog.add_widget(files_widget)
            file_index = 0
            parent_dir_path = "."
            if (self.listing_path is not None):
                parent_dir_path = self.listing_path
            is_start = False
            back_widget = None
            test_image = program.font.render( "|", program.antialias, (128,128,128,255))
            test_image_rect = test_image.get_rect()
            slot_height = test_image_rect.height
            if (start_index is None) or (start_index<=0):
                is_start = True
            if not is_start:
                this_image = program.font.render( "«", program.antialias, (128,128,128,255))
                this_image_rect = this_image.get_rect()
                this_widget = BAWidget("«", pygame.Rect(self.last_x, self.last_y, this_image_rect.width, this_image_rect.height),dialog)
                this_widget.key="<"
                back_widget = this_widget
                this_widget.handler = this_widget.form_list_files_starting_at_value
                this_widget.image = this_image
                this_widget.kind = "listitem"
                dialog.add_widget(this_widget)
            self.last_y += slot_height
            is_end = True
            filename_list = [".."]+os.listdir(parent_dir_path)
            file_count = 0
            slots_height = list_rect.bottom - self.last_y
            slots_count = int(slots_height/slot_height)
            for filename in filename_list:
                if file_index >= start_index:
                    display_text = filename
                    file_fullname = os.path.abspath(os.path.join(parent_dir_path,filename))
                    if os.path.isdir(file_fullname):
                        display_text = "["+filename+"]"
                    this_image = program.font.render( display_text, program.antialias, (128,128,128,255))
                    this_image_rect = this_image.get_rect()
                    file_widget = BAWidget("file"+str(file_index), pygame.Rect(self.last_x, self.last_y, this_image_rect.width, this_image_rect.height),dialog)
                    file_widget.text = filename
                    file_widget.key = file_fullname
                    #if filename == "..":
                    #    file_widget.key = parent_dir_path
                    file_widget.handler = file_widget.set_form_last_clicked_to_key
                    #if os.path.isdir(file_fullname):
                    #    file_widget.handler = file_widget.set_form_list_path_to_key
                    #elif os.path.isfile(file_fullname):
                    #    file_widget.handler = file_widget.set_form_last_clicked_to_key
                    file_widget.image = this_image
                    file_widget.kind = "listitem"
                    dialog.add_widget(file_widget)
                    self.last_y += slot_height
                    file_count += 1
                    if self.last_y + this_image_rect.height >= list_rect.bottom:
                        if file_index < len(filename_list):
                            is_end = False
                        file_index += 1
                        break
                file_index += 1
            if back_widget is not None:
                back_widget.value = file_index - slots_count*2
            if not is_end:
                this_image = program.font.render( "»", program.antialias, (128,128,128,255))
                this_image_rect = this_image.get_rect()
                this_widget = BAWidget("»", pygame.Rect(self.last_x, self.last_y, this_image_rect.width, this_image_rect.height),dialog)
                this_widget.key="»"
                this_widget.value = file_index
                this_widget.handler = this_widget.form_list_files_starting_at_value
                this_widget.image = this_image
                this_widget.kind = "listitem"
                dialog.add_widget(this_widget)
                self.last_y += this_image_rect.height
        else:
            print("Could not finish list_files: dialog is not present")

    def close_container(self):
        if self.container is not None:
            #if self.key is not None:
            #    self.container.result = self.key
            #else:
            #ALWAYS set result to self.text, so result is predictable
            # from the standpoint of the person using the API
            # [key is automatically changed to ok if text.lower() is ok, open or save]
            self.container.result = self.text

    def remove_widget_by_index(self, subwidget_index):
        if self.subwidgets is not None:
            if (subwidget_index>=0) and (subwidget_index<len(self.subwidgets)):
                self.subwidgets[subwidget_index].remove_subwidgets()
                self.subwidgets.pop(subwidget_index)
        
    def remove_subwidgets(self):
        while len(self.subwidgets) > 0:
            self.subwidgets[len(self.subwidgets)-1].remove_subwidgets()
            self.subwidgets.pop()

#formerly show_dialog
def create_file_open_dialog(container, button_strings, element_strings, file_start_index = 0, file_prev_index = None):
    #width = container.rect.width/2
    #height = container.rect.height/2
    dialog = BAWidget("dialog", (.5,.5), container)
    dialog.kind = "dialog"
    dialog.image.fill((32,64,64,255))
    if container is not None:
        container.subwidgets.append(dialog)            
        
    button_w = 150
    button_h = 24
    button_spacing = 8
    button_padding_bottom = 8
    buttons_w = 0
    for index in range(0,len(button_strings)):
        buttons_w += button_w
        if index != 0:
            buttons_w += button_spacing
    dialog.last_x = dialog.rect.left+int((dialog.rect.width-buttons_w)/2)
    dialog.last_y = int(dialog.rect.bottom-button_h-button_padding_bottom)
    buttons_top = dialog.last_y
    for index in range(0,len(button_strings)):
        button_string = button_strings[index]
        this_button = BAWidget(button_string+"Button", pygame.Rect(dialog.last_x,dialog.last_y,button_w,button_h), dialog)
        this_button.image.fill( (128,192,192,255) )
        this_button.kind = "button"
        if (button_string.lower() == "ok") or (button_string.lower() == "open") or (button_string.lower() == "save"):
            this_button.key = "ok"
        text_image = program.font.render( button_string, program.antialias, (0,0,0,128))
        this_button.text = button_string
        text_rect = text_image.get_rect()
        this_button.image.blit( text_image, ((this_button.rect.width-text_rect.width)/2,(this_button.rect.height-text_rect.height)/2) )
        this_button.handler = this_button.close_container
        dialog.add_widget(this_button)
        dialog.last_x += button_w + button_spacing
    
    for element_string in element_strings:
        if (element_string=="fileopener"):
            dialog.desired_target = "file"
            dialog.list_files()
            dialog.set_ok_enabled(False)
    container.last_x = dialog.last_x
    container.last_y = dialog.last_y
                
    return dialog
    
def blit_widget(screen, widget):
    if screen is not None:
        if widget is not None:
            if widget.image is not None:
                screen.blit(widget.image,(widget.rect.left,widget.rect.top))
            if widget.subwidgets is not None:
                for subwidget in widget.subwidgets:
                    blit_widget(screen, subwidget)

def get_top_widget_at(lowest_widget, pos):
    result = None
    if (lowest_widget.subwidgets is not None) and (len(lowest_widget.subwidgets)>0):
        for subwidget in lowest_widget.subwidgets:
            result = get_top_widget_at(subwidget, pos)
            if result is not None:
                break
    if result is None:
        if lowest_widget.rect is not None:
            if (lowest_widget.rect.collidepoint(pos)):
                result = lowest_widget
    return result
