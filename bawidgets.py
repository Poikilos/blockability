
#include this file then make a subclass of BAWidgetProgram (for example see baspriteframer)
import os
import pygame

program = None
screen = None
is_visual_debug = True
debug_indent = ""
dialog = None

def draw():
    #program.trunk_widget.layout()
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
    #dialog = None

    def __init__(self, display_size):
        global screen
        self.antialias = True
        self.display_size = display_size
        pygame.init()
        screen = pygame.display.set_mode(display_size)
        if not pygame.font: print('Warning, fonts disabled')
        else:
            self.font = pygame.font.Font(None, 30)
        self.trunk_widget = BAWidget("trunk", None, minimum_rect=pygame.Rect(0,0,display_size[0],display_size[1]), padding=(0,0,0,0), margin=(0,0,0,0))
        self.trunk_widget.background_color = (0,0,0,255)

class BAWidget:
    LEFT_INDEX = 0
    TOP_INDEX = 1
    RIGHT_INDEX = 2
    BOTTOM_INDEX = 3
    

    _text = None
    _text_rect = None
    _text_image = None
    _text_image_rendered_text = None
    _text_image_rendered_enabled = None
    _text_image_rendered_color = None
    _is_layout_suspended = None
    _minimum_rect = None
    _enabled = None
    _visible = None
    _high_quality_valign = None
    
    align = None
    valign = None
    padded_rect = None
    rect = None
    orientation = None
    subwidgets = None
    form = None
    result = None
    container = None
    handler = None
    last_clicked_key = None
    image = None
    name = None
    index = None
    key = None
    folder = None
    file_count = None
    kind = None
    value = None
    #last_x = 0
    #last_y = 0
    listing_path = None
    desired_target = None
    margin = None
    padding = None
    background_color = None
    color = None
    padding_color = None
    is_position_relative = None
    listview_lines_count = 10
    
    def __init__(self, name, callback_such_as_trunk_or_dialog_form, minimum_rect=pygame.Rect(0,0,0,0), orientation='vertical', text=None, is_position_relative=True, key=None, align="left", valign="top", margin=(8,8,8,8), padding=(16,16,16,16), background_color=None):
        #NOTE: callback_such_as_trunk_or_dialog_form (set on BAWidget creation) is where button clicks will set variables. container is for layout, and is set by add_widget
        self.form = callback_such_as_trunk_or_dialog_form
        self.name = name
        self.background_color = background_color
        self.listview_lines_count = 10
        self.align = align
        self.valign = valign
        self._high_quality_valign = True
        self.subwidgets = list()
        self._enabled = True
        self._minimum_rect = pygame.Rect(minimum_rect.left, minimum_rect.top, minimum_rect.width, minimum_rect.height)
        self.rect = pygame.Rect(minimum_rect.left, minimum_rect.top, minimum_rect.width, minimum_rect.height)
        self.orientation = orientation
        self.margin = margin
        self.padding = padding
        self.color = (255, 255, 255, 255)
        self._text = text
        self._is_layout_suspended = False
        self._visible = True
        self.is_position_relative = is_position_relative
        #self.padding_color = (40,40,40,255)
        self.layout()
        self.key = key
        #self.regen()
        #if BAWidget._test_image_rect is None:
            #if program is not None:
                #if program.font is not None:
                    #BAWidget._test_image = program.font.render( "|", program.antialias, (128,128,128,255))
                    #BAWidget._test_image_rect = _test_image.get_rect()

    def suspend_layout(self):
        self._is_layout_suspended = True
    
    
    def resume_layout(self):
        self._is_layout_suspended = False
        self.regen()
    
    def add_widget(self, sub_widget):
        if not isinstance(sub_widget,BAWidget):
            if is_visual_debug:
                print("WARNING: non-widget sent to add_widget, so nothing done.")
        sub_widget.index = len(self.subwidgets)
        self.subwidgets.append(sub_widget)
        sub_widget.container = self
        #NOTE: callback_such_as_trunk_or_dialog_form (set on BAWidget creation) is where button clicks will set variables. container is for layout, and is set by add_widget
        if not self._is_layout_suspended:
            #self.rect = self.get_autosize()
            self.layout()
            #self.regen()

    def move_pos(self, relative_padded_pos):
        self.rect.left += relative_padded_pos[0]
        self.padded_rect.left += relative_padded_pos[0]
        if len(relative_padded_pos) > 1:
            self.rect.top += relative_padded_pos[1]
            self.padded_rect.top += relative_padded_pos[1]
    
    #moves both rect and padded_rect by relative position (x,y) tuple or list
    def move_pos_recursively(self, relative_padded_pos):
        if self.subwidgets is not None:
            for subwidget in self.subwidgets:
                subwidget.move_pos_recursively(relative_padded_pos)
        self.rect.left += relative_padded_pos[0]
        self.padded_rect.left += relative_padded_pos[0]
        if len(relative_padded_pos) > 1:
            self.rect.top += relative_padded_pos[1]
            self.padded_rect.top += relative_padded_pos[1]
    
    def set_pos(self, absolute_padded_pos):
        self.padded_rect.left = absolute_padded_pos[0]
        self.rect.left = self.padded_rect.left + self.padding[BAWidget.LEFT_INDEX]
        if len(absolute_padded_pos) > 1:
            self.padded_rect.top = absolute_padded_pos[1]
            self.rect.top = self.padded_rect.top + self.padding[BAWidget.TOP_INDEX]
        
    #sets both padded_rect and adjusts rect accordingly, to position (x,y) tuple or list, then moves children by the relative difference from the old location
    def set_pos_recursively(self, absolute_padded_pos):
        deltas = [absolute_padded_pos[0]-self.padded_rect.left]
        if len(absolute_padded_pos) > 1:
            deltas = (absolute_padded_pos[0]-self.padded_rect.left, absolute_padded_pos[1]-self.padded_rect.top)
        if self.subwidgets is not None:
            for subwidget in self.subwidgets:
                subwidget.move_pos_recursively(deltas)
        self.padded_rect.left = absolute_padded_pos[0]
        self.rect.left = self.padded_rect.left + self.padding[BAWidget.LEFT_INDEX]
        if len(absolute_padded_pos) > 1:
            self.padded_rect.top = absolute_padded_pos[1]
            self.rect.top = self.padded_rect.top + self.padding[BAWidget.TOP_INDEX]
    #_minimum_scrollwidget_rect = None
    def layout(self, pushed_pos=(0,0), this_debug_indent=""):
        #if this_debug_indent=="":
        #    print("")
        #left_margin = 0
        #top_margin = 0
        #right_margin = 0
        #bottom_margin = 0
        #pushed_x = 0
        #pushed_y = 0
        elements_width = 0
        elements_height = 0
        if self._text is not None and len(self._text) > 0:
            self.regen_text()
            elements_width = self._text_rect.width
            elements_height = self._text_rect.height
        
        if self.rect is None:
            self.rect = pygame.Rect(0, 0, self._minimum_rect.width, self._minimum_rect.height)
        else:
            self.rect.left = 0
            self.rect.top = 0
            self.rect.width = self._minimum_rect.width
            self.rect.height = self._minimum_rect.height
        if self.padded_rect is None:
            self.padded_rect = pygame.Rect(0, 0, self.padding[BAWidget.LEFT_INDEX]+self.rect.width+self.padding[BAWidget.RIGHT_INDEX], self.padding[BAWidget.TOP_INDEX]+self.rect.height+self.padding[BAWidget.BOTTOM_INDEX])
        else:
            self.padded_rect.top = 0
            self.padded_rect.left = 0
            self.padded_rect.width = self.padding[BAWidget.LEFT_INDEX]+self.rect.width+self.padding[BAWidget.RIGHT_INDEX]
            self.padded_rect.height = self.padding[BAWidget.TOP_INDEX]+self.rect.height+self.padding[BAWidget.BOTTOM_INDEX]
        self.padded_rect.left = pushed_pos[0]
        self.padded_rect.top = pushed_pos[1]
        self.rect.left = self.padded_rect.left + self.padding[BAWidget.LEFT_INDEX]
        self.rect.top = self.padded_rect.top + self.padding[BAWidget.TOP_INDEX]
        #if self.container is not None:
            #print(this_debug_indent+"using container '"+self.container.name+"' "+str(self.container.rect)+" for '"+self.name+"'")
            #print(this_debug_indent+"using container '"+self.container.name+"' "+str(self.container.rect.left)+","+str(self.container.rect.top)+" for '"+self.name+"'")
        abs_expected_size = (self._minimum_rect.width, self._minimum_rect.height)
        if self.is_position_relative:
            if self.container is not None:
                self.padded_rect.left += self.container.rect.left
                self.padded_rect.top += self.container.rect.top
                self.padded_rect.left += self.container.margin[BAWidget.LEFT_INDEX]
                self.padded_rect.top +=  self.container.margin[BAWidget.TOP_INDEX]
                self.rect.left += self.container.rect.left
                self.rect.top += self.container.rect.top
                self.rect.left += self.container.margin[BAWidget.LEFT_INDEX]
                self.rect.top += self.container.margin[BAWidget.TOP_INDEX]
        else:
            self.set_pos((self._minimum_rect.left, self._minimum_rect.top))
        #NOTE: now position is RELATIVE, but layout method of container will push the rect past the previous widget
        is_orientation_ok = True
        #if self.margin is not None:
            #left_margin = self.margin[BAWidget.LEFT_INDEX]
            #right_margin = self.margin[BAWidget.RIGHT_INDEX]
            #top_margin = self.margin[BAWidget.TOP_INDEX]
            #bottom_margin = self.margin[BAWidget.BOTTOM_INDEX]
        known_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)
        if self.subwidgets is not None:
            for this_widget in self.subwidgets:
                this_widget_push_pos = (0, elements_height)
                if self.orientation == 'horizontal':
                    this_widget_push_pos = (elements_width, 0)
                if not this_widget.is_position_relative:
                    this_widget_push_pos = (0, 0)
                this_widget.layout(pushed_pos=this_widget_push_pos, this_debug_indent=this_debug_indent+"  ")
                if self.orientation == 'horizontal':
                    #this_widget.padded_rect.left += elements_width
                    #this_widget.rect.left += elements_width
                    if this_widget.is_position_relative:
                        elements_width += this_widget.padded_rect.width
                        if this_widget.padded_rect.height > elements_height:
                            elements_height = this_widget.padded_rect.height
                    #this_widget.rect.top += 0
                    #if this_widget._minimum_rect is not None:
                        #this_widget.rect.top += this_widget._minimum_rect.top 
                    #pushed_x = this_widget.padded_rect.width
                else:
                    if self.orientation != 'vertical':
                        is_orientation_ok = False
                    #this_widget.padded_rect.top += elements_height
                    #this_widget.rect.top += elements_height
                    if this_widget.is_position_relative:
                        elements_height += this_widget.padded_rect.height
                        if this_widget.padded_rect.width > elements_width:
                            elements_width = this_widget.padded_rect.width
                    #this_widget.rect.left += 0
                    #if this_widget._minimum_rect is not None:
                        #this_widget.rect.left += this_widget._minimum_rect.left 
                    #pushed_y += this_widget.padded_rect.height
            if not is_orientation_ok:
                print("ERROR in widget named '"+str(self.name)+"': orientation '"+str(this.orientation)+"' is not known")
        if self.margin[BAWidget.LEFT_INDEX] + elements_width + self.margin[BAWidget.RIGHT_INDEX] > self.rect.width:
            self.rect.width = self.margin[BAWidget.LEFT_INDEX] + elements_width + self.margin[BAWidget.RIGHT_INDEX]
        if self.margin[BAWidget.TOP_INDEX] + elements_height + self.margin[BAWidget.BOTTOM_INDEX] > self.rect.height:
            self.rect.height = self.margin[BAWidget.TOP_INDEX] + elements_height + self.margin[BAWidget.BOTTOM_INDEX]
        if self.padding[BAWidget.LEFT_INDEX] + self.rect.width + self.padding[BAWidget.RIGHT_INDEX] > self.padded_rect.width:
            self.padded_rect.width = self.padding[BAWidget.LEFT_INDEX] + self.rect.width + self.padding[BAWidget.RIGHT_INDEX]
        if self.padding[BAWidget.TOP_INDEX] + self.rect.height + self.padding[BAWidget.BOTTOM_INDEX] > self.padded_rect.height:
            self.padded_rect.height = self.padding[BAWidget.TOP_INDEX] + self.rect.height + self.padding[BAWidget.BOTTOM_INDEX]
        #if not self.is_position_relative:
            #size_deltas = abs_expected_size[0]-self.padded_rect.width, abs_expected_size[1]-self.padded_rect.height
            ##pos_deltas = abs_expected_size[0]-self.padded_rect.width, abs_expected_size[1]-self.padded_rect.height
            ##self.move_pos([size_deltas[0]])
            #self.set_pos_recursively( (self._minimum_rect.left+size_deltas[0]/2, self._minimum_rect.top+size_deltas[1]/2) )
        if self.subwidgets is not None:
            push_x = 0
            for this_widget in self.subwidgets:
                #if this_widget.is_position_relative:
                if self.align == 'center':
                    start_x = self.rect.left + self.margin[0]
                    space_x = self.rect.width - self.margin[0] - self.margin[2]
                    if self.orientation == 'horizontal':
                        #this_widget.padded_rect.left = start_x+int((space_x-elements_width)/2.0+.5)+push_x
                        this_widget.set_pos_recursively( [start_x+int((space_x-elements_width)/2.0+.5)+push_x] )
                    else:
                        #this_widget.padded_rect.left = start_x+int((space_x-this_widget.padded_rect.width)/2.0+.5)  # +.5 for rounding
                        this_widget.set_pos_recursively( [start_x+int((space_x-this_widget.padded_rect.width)/2.0+.5)] )
                    #this_widget.rect.left = this_widget.padded_rect.left+this_widget.padding[BAWidget.LEFT_INDEX]
                elif self.align == 'right':
                    if self.orientation == 'horizontal':
                        #this_widget.padded_rect.left = self.rect.right-elements_width+push_x
                        this_widget.set_pos_recursively( [self.rect.right-elements_width+push_x] )
                    else:
                        #this_widget.padded_rect.left = self.rect.right-this_widget.padded_rect.width
                        this_widget.set_pos_recursively( [self.rect.right-this_widget.padded_rect.width] )
                    #this_widget.rect.left = this_widget.padded_rect.left+this_widget.padding[BAWidget.LEFT_INDEX]
                else:
                    #adjust subwidget for changes made to container during autosize which can only be done after subwidgets are initially sized: 
                    this_widget.rect.left += known_rect.left - self.rect.left
                    this_widget.rect.top += known_rect.top - self.rect.top
                    this_widget.padded_rect.left += known_rect.left - self.rect.left
                    this_widget.padded_rect.top += known_rect.top - self.rect.top
                if self.orientation == 'horizontal': push_x += this_widget.padded_rect.width
        self.regen()
        #print(this_debug_indent+self.name)
        #print(this_debug_indent+"  elements size:"+str((elements_width,elements_height)))
        #print(this_debug_indent+"  _minimum_rect:"+str(self._minimum_rect))
        #print(this_debug_indent+"  rect:"+str(self.rect))
        #print(this_debug_indent+"  margin:"+str(self.margin))
        #print(this_debug_indent+"  padded_rect:"+str(self.padded_rect))
        #print(this_debug_indent+"  padding:"+str(self.padding))
        
        
    def get_autosize_rect(self):
        return pygame.Rect(0,0,self.get_autosize_width_padded(),self.get_autosize_height_padded())
        
    def set_text(self, text):
        self._text = text
        self.regen()
    
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
    
    def set_last_clicked_key(self, last_clicked_key):
        is_ok_target = False
        if last_clicked_key is not None:
            if self.desired_target is None:
                self.last_clicked_key = last_clicked_key
                self.set_ok_enabled(True)
            elif self.desired_target == "file":
                if os.path.isfile(last_clicked_key):
                    self.last_clicked_key = last_clicked_key
                    self.set_ok_enabled(True)
                else:
                    self.set_ok_enabled(False)
                    self.set_list_path(last_clicked_key)
            elif self.desired_target == "folder":
                if os.path.isdir(last_clicked_key):
                    self.last_clicked_key = last_clicked_key
                    self.set_ok_enabled(True)
                    #still set_list_path in case a subfolder is desired instead:
                    self.set_list_path(last_clicked_key)
                else:
                    self.set_ok_enabled(False)
        else:
            print("ERROR: None received by set_last_clicked_key in widget named '"+self.name+"'")
        return is_ok_target
        
    def regen_text(self):
        global program
        if self._text is not None:
            if self.color is None:
                self.color = (192,0,192,255)
                print("WARNING: color was not set for widget named '"+self.name+"' so set to '"+str(self.color)+"'")
            if self._text_image is None or self._text_image_rendered_text != self._text or self._text_image_rendered_enabled != self._enabled:
                if self._enabled:
                    self._text_image_rendered_color = self.color
                else:
                    self._text_image_rendered_color = (192,192,192,128)
                self._text_image = program.font.render( self._text, program.antialias, self._text_image_rendered_color).convert_alpha()
                self._text_image_rendered_text = self._text
                self._text_image_rendered_enabled = self._enabled
                self._text_rect = self._text_image.get_rect()
            if self._text_rect is None:
                self._text_rect = self._text_image.get_rect()
        else:
            self._text_image = None
            self._text_rect = None
        
    
    
    def regen(self):
        #print(debug_indent+"regen '"+self.name+"' at ("+str(self.rect.left)+","+str(self.rect.top)+","+str(self.rect.width)+","+str(self.rect.height)+")")
        #width = self.padded_rect.width - self.padding[self.LEFT_INDEX] - self.padding[self.RIGHT_INDEX]
        #height = self.padded_rect.height - self.padding[self.TOP_INDEX] - self.padding[self.BOTTOM_INDEX]
        #if height < 0:
            #height = 0
        #if width < 0:
            #width = 0
        #self.rect = pygame.Rect(self.rect.left+self.margin[self.LEFT_INDEX], self.rect.top+self.margin[self.TOP_INDEX], width, height)
        #is_text_bigger = False
        #self._text_image = None
        #self._text_rect = None
        self.regen_text()
        #try:
        got_rect = None
        if self.image is not None:
            got_rect = self.image.get_rect()
            if self.rect is None:
                self.rect = got_rect
        if self.rect is None:
            self.rect=pygame.Rect(0,0,0,0)
            print(debug_indent+"  ERROR: rect was null for widget named '"+self.name+"' during regen")
        if self.rect.width > 0 and self.rect.height > 0 and ( (self.image is None) or (got_rect.width != self.rect.width or got_rect.height != self.rect.height) ):
            self.image = pygame.Surface( (self.rect.width, self.rect.height) ).convert_alpha()
        #except:
        #    print("Could not finish BAWidget surface with rect: "+str(self.rect))]
        if self.image is not None:
            if self.background_color is not None:
                if self._enabled:
                    self.image.fill( self.background_color )
                else:
                    self.image.fill( (128, 128, 128, self.background_color[3]) )
            else:
                #Necessary so that widget with no background_color has a transparent background, and so that, for example, when text is blitted to self.image, smooth edge is maintained (since alpha of dest [self.image] is less than alpha of source [self._text_image]):
                #self.image.fill((0,0,0,0))  
                #self.image.fill((255,0,255))
                #self.image.set_colorkey((0,255,0))
                #self.image.fill((0,255,0))
                #if self.name=="trunk":
                self.image.fill((0,0,0,0))
            if self._text_image is not None:
                text_left = self.margin[BAWidget.LEFT_INDEX]
                text_top = self.margin[BAWidget.TOP_INDEX]
                bottoms = list()
                descender_last_y_average = 0.0
                text_half_height = self._text_rect.height / 2
                descenders_part = 0
                if self._high_quality_valign and (self.valign=="middle" or self.valign=="bottom"):
                    step = 5  # for speed
                    x = step
                    while x < self._text_rect.width:
                    #for x in range(0,self._text_rect.width):
                        for i in range(0,self._text_rect.height):
                            y = self._text_rect.height - 1 - i
                            if y < text_half_height:
                                break
                            color = self._text_image.get_at( (x,y) )
                            if color == self._text_image_rendered_color:
                                bottoms.append(y)
                                descender_last_y_average+=float(i-1)
                                break
                        x += step
                    if len(bottoms) > 0:
                        descender_last_y_average = int(descender_last_y_average/float(len(bottoms))+.5)
                        #get median:
                        for i in range(0,len(bottoms)):
                            if abs(bottoms[i]-descender_last_y_average) < abs(descenders_part-descender_last_y_average):
                                descenders_part = bottoms[i]
                if self.valign=="middle":
                    text_top = (self.rect.height-self._text_rect.height)/2
                    text_top += descenders_part
                elif self.valign=="bottom":
                    text_top = self.rect.height-self._text_rect.height-self.margin[BOTTOM_INDEX]
                    text_top += descenders_part
                if self.align=="center":
                    text_left = (self.rect.width-self._text_rect.width)/2
                elif self.align=="right":
                    text_left = self.rect.width-self._text_rect.width-self.margin[RIGHT_INDEX]
                self.image.blit( self._text_image, (text_left, text_top) )
            
    def set_enabled(self, set_is_enabled):
        if self._enabled != set_is_enabled:
            self._enabled = set_is_enabled
            self.regen()

    def set_visible(self, set_is_visible):
        if self._visible != set_is_visible:
            self._visible = set_is_visible
            self.regen()
        
        
    def set_ok_enabled(self,set_is_enabled):
        this_button = self.get_subwidget_by_key("ok")
        if this_button is not None:
            if this_button._enabled != set_is_enabled:
                this_button.background_color = (128,128,192,255)
                this_button.color = (0,0,0,128)
                this_button.set_enabled(set_is_enabled)
        else:
            print("no ok button in "+self.name+" which contains:")
            for sub in self.subwidgets:
                print("  - "+str(sub.key)+":"+str(sub.name))
    
    def set_form_last_clicked_to_key(self):
        if self.key is None:
            print("ERROR in set_form_last_clicked_to_key Uh, oh, key is None for widget named '"+self.name+"'")
            
        if self.form is not None:
            if self.key is not None:
                self.form.set_last_clicked_key(self.key)
            else:
                self.form.set_last_clicked_key(self._text)
            print("set form last clicked key:"+str(self.form.last_clicked_key))
            print("  self.key:"+str(self.key))
            print("  self._text:"+str(self._text))
            

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
                if item._text is not None:
                    if item._text == text:
                        result = index
                        break
            else:
                text_lower = text.lower()
                if item._text is not None:
                    if item._text.lower() == text_lower:
                        result = index
                        break
        return result

    #recursive
    def get_subwidget_by_key(self, key):
        result = None
        if self.subwidgets is not None:
            index = self.index_of_subwidget_by_key(key)
            if index is not None:
                result = self.subwidgets[index]
            else:
                for subwidget in self.subwidgets:
                    result = subwidget.get_subwidget_by_key(key)
                    if result is not None:
                        break
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

    #recursive
    def get_subwidget_by_name(self, name):
        result = None
        if self.subwidgets is not None:
            index = self.index_of_subwidget_by_name(name)
            if index is not None:
                result = self.subwidgets[index]
            else:
                for subwidget in self.subwidgets:
                    result = subwidget.get_subwidget_by_name(name)
                    if result is not None:
                        break
        return result

    def index_of_subwidget_by_name(self, name):
        result = None
        for index in range(0,len(self.subwidgets)):
            item = self.subwidgets[index]
            if item.name is not None:
                if item.name == name:
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
        files_widget = self.get_subwidget_by_name("files_widget")
        if files_widget is not None:
            files_widget.remove_subwidgets()
            #while index is not None:
            #    index = self.index_of_subwidget_by_kind("listitem")
            #    if index is not None:
            #        self.subwidgets.pop(index)
            #print("done (cleared listitems)")
        else:
            if is_visual_debug:
                print("WARNING: no files_widget during clear_listitems")

    def form_list_files_starting_at_value(self):
        if self.form is not None:
            self.form.list_files(self.value)
            
    def create_listitem(self, name, form, display_text, key=None):
        this_widget = BAWidget(name, form, align="left", valign="middle")  # formerly file_widget
        this_widget.color = (0,0,0,255)
        #this_widget.background_color = (192,192,192,0)
        #this_widget.background_color=(0,0,0,0)
        this_widget.margin = (1,0,0,1)
        this_widget.padding = (0,1,0,0)
        this_widget.set_text(display_text)
        #this_image_rect = this_image.get_rect()
        #this_widget.set_text(filename)
        this_widget.key = key
        #if filename == "..":
        #    this_widget.key = parent_dir_path
        #if os.path.isdir(file_fullname):
        #    this_widget.handler = this_widget.set_form_list_path_to_key
        #elif os.path.isfile(file_fullname):
        #    this_widget.handler = this_widget.set_form_last_clicked_to_key
        #this_widget.image = this_image
        this_widget.kind = "listitem"
        
        return this_widget
        
        
    def list_files(self, start_index = 0):
        global dialog
        global program
        self.clear_listitems()
        #element_padding = 8
        #dialog = program.trunk_widget.dialog
        #dialog = None
        #dialog_index = self.index_of_subwidget_by_kind("dialog")
        #if dialog_index is not None:
        #    dialog = self.subwidgets[dialog_index]
            
        #dialog = self  # this can REALLY mess things up if list_files was called on the wrong thing (warning shown below)
        if dialog is not None:
            if dialog.kind != "dialog":
                print("WARNING: list_files only supported in dialog not '"+dialog.kind+"'")
            #self.last_x = dialog.padded_rect.left+element_padding
            #self.last_y = dialog.padded_rect.top+element_padding
            #any_button = self.get_subwidget_by_kind("button")
            #buttons_top = program.display_size[1]
            #if any_button is not None:
            #    buttons_top = any_button.padded_rect.top
            #else:
            #    print("no buttons, so clipping file list to "+str(buttons_top))
            
            #list_rect = pygame.Rect(0, 0, dialog.rect.width, buttons_top-self.last_y-element_padding)
            is_scroll_widget_new = False
            scroll_widget = self.get_subwidget_by_name("scroll_widget")
            if scroll_widget is None:
                is_scroll_widget_new = True
                scroll_widget = BAWidget("scroll_widget", dialog, valign="middle", align="left", orientation='vertical', padding=(0,0,0,0), margin=(0,0,0,0))
                #scroll_widget.background_color = (0,0,0,255)

            is_scrollbar_widget_new = False
            scrollbar_widget = self.get_subwidget_by_name("scrollbar_widget")
            if scrollbar_widget is None:
                is_scrollbar_widget_new = True
                scrollbar_widget = BAWidget("scrollbar_widget", dialog, align="right", orientation='horizontal', padding=(0,0,0,0), margin=(0,0,0,0))
                scrollbar_widget.background_color = (128,128,128,255)
                
            is_files_widget_new = False
            files_widget = self.get_subwidget_by_name("files_widget")
            if files_widget is None:
                is_files_widget_new = True
                files_widget = BAWidget("files_widget", dialog, valign="top", minimum_rect=dialog._minimum_rect, padding=(0,0,0,0))
                files_widget.background_color = (255,255,255,255)
            file_index = 0
            parent_dir_path = "."
            if (self.listing_path is not None):
                parent_dir_path = self.listing_path
            is_start = False
            back_widget = None
            #slot_height = _test_image_rect.height
            if (start_index is None) or (start_index<=0):
                is_start = True
            this_widget = self.get_subwidget_by_name("files_scroll_back")
            scroll_spacer_widget = None
            is_back_widget_new = False
            if this_widget is None:
                is_back_widget_new = True
                this_widget = BAWidget("files_scroll_back", dialog, valign="middle")
                scroll_spacer_widget = BAWidget("scroll_spacer_widget", dialog, minimum_rect=pygame.Rect(0,0,files_widget._minimum_rect.width-22, 10), padding=(0,0,0,0), margin=(0,0,0,0))
                this_widget.color = (0,0,0,255)
                this_widget.margin = (0,0,0,0)
                this_widget.padding = (0,1,0,0)
                this_widget.set_text("«")
                this_widget.key = "«"
                this_widget.handler = this_widget.form_list_files_starting_at_value
                this_widget.kind = "listitem"
            back_widget = this_widget
            if is_back_widget_new:
                scrollbar_widget.add_widget(this_widget)
                scrollbar_widget.add_widget(scroll_spacer_widget)

            if not is_start:
                this_widget.set_enabled(True)
                this_widget.set_visible(True)
            else:
                if this_widget is not None:
                    this_widget.set_enabled(False)
                    this_widget.set_visible(False)
            #self.last_y += slot_height
            is_end = True
            filename_list = [".."]+os.listdir(parent_dir_path)
            file_count = 0
            #slots_height = list_rect.bottom - self.last_y
            #slots_count = int(slots_height/slot_height)
            #files_widget.suspend_layout()
            
            filename_list_sorted = list()
            is_listing_hidden_files = False
            for filename in filename_list:
                file_fullname = os.path.abspath(os.path.join(parent_dir_path,filename))
                if os.path.isdir(file_fullname):
                    if is_listing_hidden_files or (filename != "__pycache__" and (filename==".." or filename[0]!=".")):
                        filename_list_sorted.append(filename)
            for filename in filename_list:
                file_fullname = os.path.abspath(os.path.join(parent_dir_path,filename))
                if os.path.isfile(file_fullname):
                    if is_listing_hidden_files or (filename[0]!="."):
                        filename_list_sorted.append(filename)
            filename_list = filename_list_sorted
            for filename in filename_list:
                if file_index >= start_index:
                    
                    display_text = filename
                    file_fullname = os.path.abspath(os.path.join(parent_dir_path,filename))
                    if os.path.isdir(file_fullname):
                        display_text = "["+filename+"]"
                    this_widget = self.create_listitem("file"+str(file_index), dialog, display_text)
                    this_widget.key = file_fullname
                    this_widget.handler = this_widget.set_form_last_clicked_to_key
                    
                    
                    files_widget.add_widget(this_widget)  #OK to add to a different widget than form (since form is set to dialog, dialog variables will be set on click, not container variables) 
                    #self.last_y += slot_height
                    file_count += 1
                    #if self.last_y + this_image_rect.height >= list_rect.bottom:
                    if file_count >= self.listview_lines_count:
                        if file_index < len(filename_list):
                            is_end = False
                        file_index += 1
                        break
                file_index += 1
                
            #To keep autosize consistent:
            for extra_index in range(0, self.listview_lines_count-file_count):
                this_widget = self.create_listitem("file"+str(file_index), dialog, " ")
                files_widget.add_widget(this_widget)
            #files_widget.resume_layout()
            if is_files_widget_new:
                scroll_widget.add_widget(files_widget)
            if is_scrollbar_widget_new:
                scroll_widget.add_widget(scrollbar_widget)
            if is_scroll_widget_new:
                dialog.add_widget(scroll_widget)
            if back_widget is not None:
                back_widget.value = file_index - self.listview_lines_count*2
            is_forward_widget_new = False
            this_widget = self.get_subwidget_by_name("files_scroll_forward")
            if this_widget is None:
                is_forward_widget_new = True
                this_widget = BAWidget("files_scroll_forward", dialog, valign="middle")
                this_widget.color = (0,0,0,255)
                this_widget.margin = (0,0,0,0)
                this_widget.padding = (0,1,0,0)
                this_widget.set_text("»")
                this_widget.key = "»"
                this_widget.kind = "listitem"
                this_widget.handler = this_widget.form_list_files_starting_at_value
            if is_forward_widget_new:
                scrollbar_widget.add_widget(this_widget)
            if not is_end:
                this_widget.set_enabled(True)
                this_widget.set_visible(True)
                #this_image = program.font.render( "»", program.antialias, (128,128,128,255))
                #this_image_rect = this_image.get_rect()
                #this_widget.key="»"
                this_widget.value = file_index
                #this_widget.image = this_image
                #self.last_y += this_image_rect.height
            #files_widget.regen()
            else:
                this_widget.set_enabled(False)
                this_widget.set_visible(False)
            dialog.layout()
        else:
            print("Could not finish list_files: dialog is not present")

    def return_form_result(self):
        if self.form is not None:
            #if self.key is not None:
            #    self.container.result = self.key
            #else:
            #ALWAYS set result to self._text, so result is predictable from the perspective of whoever called show_dialog
            # from the standpoint of the person using the API
            # [key is automatically changed to ok if text.lower() is ok, open or save]
            self.form.result = self._text

    def remove_widget_by_index(self, subwidget_index):
        if self.subwidgets is not None:
            if (subwidget_index>=0) and (subwidget_index<len(self.subwidgets)):
                self.subwidgets[subwidget_index].remove_subwidgets()
                self.subwidgets.pop(subwidget_index)
        
    def remove_subwidgets(self):
        while len(self.subwidgets) > 0:
            self.subwidgets[len(self.subwidgets)-1].remove_subwidgets()
            self.subwidgets.pop()
        if not self._is_layout_suspended:
            self.form.layout()

def dismiss_dialog():
    global dialog
    if program is not None:
        index = program.trunk_widget.index_of_subwidget_by_kind("dialog")
        if index is not None:
            program.trunk_widget.remove_widget_by_index(index)
            dialog = None
            #print("dialog finished")
        else:
            print("could not remove dialog since couldn't be found")
    else:
        print("could not remove dialog since program is None")

#Shows a new dialog and sets dialog (caller should check bawidgets.dialog.result and if not None, call bawidgets.dismiss_dialog())
def show_dialog(container, button_strings, element_strings, desired_target, file_start_index = 0, file_prev_index = None, key=None):
    width = container.rect.width/2
    #height = (container.rect.height/5)*4
    #height = program.trunk_widget.rect.height/5*4
    height = 0
    global dialog
    global program
    if dialog is None:
        dialog = BAWidget("dialog", container, minimum_rect=pygame.Rect((container.rect.width-width)/2,50,width,height), is_position_relative=False, key=key, align="center", valign="middle")
        global program
        program.trunk_widget.dialog = dialog
        if container.name != "trunk":
            print(str(container.name)+" cannot be container for dialog. Use program.trunk_widget instead.")
        dialog.kind = "dialog"
        dialog.background_color = (64,64,64,255)
        button_w = 150
        button_h = 24
        #button_spacing = 8
        #button_padding_bottom = 8
        #buttons_w = 0
        #for index in range(0,len(button_strings)):
        #    buttons_w += button_w
        #    if index != 0:
        #        buttons_w += button_spacing
        #dialog.last_x = dialog.rect.left+int((dialog.rect.width-buttons_w)/2)
        #dialog.last_y = int(dialog.rect.bottom-button_h-button_padding_bottom)
        #buttons_top = dialog.last_y
        is_ready = True
        for element_string in element_strings:
            if (element_string=="fileopener"):
                choose_text = "Pick:"
                if desired_target is not None:
                    "Choose a "+desired_target+":"
                #label_widget = BAWidget("label_widget", dialog, minimum_rect=pygame.Rect(0,0,100,20), text=choose_text, margin=(0,0,0,0), padding=(0,0,0,0))
                #dialog.add_widget(label_widget)
                dialog.valign = "top"
                dialog.set_text(choose_text)
                dialog.list_files()
                is_ready = False
        dialog.desired_target = desired_target
        #container.last_x = dialog.last_x
        #container.last_y = dialog.last_y

        buttons_layout_w = BAWidget("buttons_layout_w", dialog, orientation='horizontal')
        for index in range(0,len(button_strings)):
            button_string = button_strings[index]
            this_button = BAWidget(button_string+"_button", dialog, minimum_rect=pygame.Rect(0,0,button_w,button_h), text=button_string)
            this_button.background_color = (128,192,192,255)
            this_button.kind = "button"
            if (button_string.lower() == "ok") or (button_string.lower() == "open") or (button_string.lower() == "save"):
                this_button.key = "ok"
            this_button.color = (0,0,0,128)
            this_button.regen()
            #self._text_image = program.font.render( button_string, program.antialias, (0,0,0,128))
            #this_button._text = button_string
            #self._text_rect = self._text_image.get_rect()
            #this_button.image.blit( self._text_image, ((this_button.rect.width-self._text_rect.width)/2,(this_button.rect.height-self._text_rect.height)/2) )
            this_button.handler = this_button.return_form_result
            buttons_layout_w.add_widget(this_button)
            #dialog.last_x += button_w + button_spacing
        dialog.add_widget(buttons_layout_w)
        dialog.set_ok_enabled(is_ready)
        dialog.layout()
        if container is not None:
            container.add_widget(dialog)
        #return dialog
    else:
        print("ERROR: there is already a dialog, so cannot create one.")
    
def blit_widget(screen, widget, this_debug_indent=""):
    #print(this_debug_indent+"drawing '"+widget.name+"' at ("+str(widget.rect.left)+","+str(widget.rect.top)+","+str(widget.rect.width)+","+str(widget.rect.height)+")")
    if screen is not None:
        if widget is not None and widget._visible:
            if widget.padding_color is not None and widget.padded_rect is not None:
                pad_image = pygame.Surface( (widget.padded_rect.width, widget.padded_rect.height) ).convert_alpha()
                #except:
                #    print("Could not finish BAWidget surface with rect: "+str(widget.rect))]
                if pad_image is not None:
                    #if widget.padding_color is not None:
                    if widget._enabled:
                        pad_image.fill( widget.padding_color )
                    else:
                        pad_image.fill( (64, 64, 64, widget.padding_color[3]) )
                    screen.blit( pad_image, (widget.padded_rect.left, widget.padded_rect.top) )

            if widget.image is not None:
                screen.blit(widget.image,(widget.rect.left,widget.rect.top))
            if widget.subwidgets is not None:
                for subwidget in widget.subwidgets:
                    blit_widget(screen, subwidget, this_debug_indent=this_debug_indent+"  ")

#Caller must check whether the returned result is not None and result._enabled 
def get_top_widget_at(lowest_widget, pos, this_debug_indent=""):
    result = None
    global dialog
    #if this_debug_indent=="":
        #print("")
    #print(this_debug_indent+lowest_widget.name+": Looking for clicked widget")
    if (dialog is not None) and (lowest_widget.name=="trunk"):
        print(this_debug_indent+"ERROR: lowest_widget was trunk, but dialog is present which should have been used instead")
    if (lowest_widget.subwidgets is not None) and (len(lowest_widget.subwidgets)>0):
        for subwidget in lowest_widget.subwidgets:
            if subwidget.name == lowest_widget.container:
                print(this_debug_indent+"ERROR: "+lowest_widget.name+" contains its container "+subwidget.name)
            if subwidget.name == "trunk":
                print(this_debug_indent+"ERROR: "+lowest_widget.name+" contains "+subwidget.name)
            if subwidget.name == "dialog":
                print(this_debug_indent+"ERROR: "+lowest_widget.name+" contains "+subwidget.name+", so dialog should be sent to get_top_widget_at instead")
                print(this_debug_indent+"program.trunk_widget:"+str(program.trunk_widget))
                print(this_debug_indent+"program.trunk_widget.dialog:"+str(dialog))
            result = get_top_widget_at(subwidget, pos, this_debug_indent=this_debug_indent+"  ")
            if result is not None:
                break
    if result is None:
        if lowest_widget.rect is not None and lowest_widget._visible:
            #ignore lowest_widget._enabled since disabled item should block clicking under it (caller must check _enabled) 
            if (lowest_widget.rect.collidepoint(pos)):
                result = lowest_widget
                #print(this_debug_indent+"self ("+result.name+") is top widget at "+str(pos))
    return result
