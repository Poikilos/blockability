
import pygame
from pygame import *
import sys
import os
import bawidgets
from bawidgets import *

status_text = None
status_text_image = None
status_text_image_rect = None
screen = None

def set_status(text):
    global status_text
    global status_text_image
    global status_text_image_rect
    status_text = text
    status_text_image = bawidgets.program.font.render( text, bawidgets.program.antialias, (128,128,128,255))
    status_text_image_rect = status_text_image.get_rect()

def show_status(screen):
    if status_text_image is not None:
        screen.blit(status_text_image, (0, bawidgets.program.display_size[1]-status_text_image_rect.height))    
        

class BASpriteFramer(BAWidgetProgram):

    def run(self):
        this_frame_image = None
        #dialog = BAWidget("dialog",pygame.Rect(display_size[0]/2,display_size[1]/2,display_size[0],display_size[1]))
        playing = True
        clock = pygame.time.Clock()
        mode = 'drawing'
        dialog = None
        title_w = BAWidget("title_w", pygame.Rect(0,0,0,0), dialog, orientation='horizontal')
        title_w.text = "(no game folder loaded)"
        tabs_layout_w = BAWidget("tabs_layout_w", list_rect, self.trunk_widget, orientation='horizontal')
        open_button_w = BAWidget("open_button_w", list_rect, self.trunk_widget)
        open_button_w.text = "Open Game"
        open_button_w.background_color = (64,64,64,255)
        self.trunk_widget.add_widget(title_w)
        self.trunk_widget.add_widget(open_button_w)
        self.trunk_widget.add_widget(tabs_layout_w)
        worlds_button = BAWidget("worlds_button", list_rect, self.trunk_widget, text="Worlds")
        tabs_layout_w.add_widget(worlds_button)
        while playing:
            #for e in pygame.event.get():
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                elif event.type == KEYDOWN:
                    if event.key == K_o:
                        #if mode != 'openimage':
                        if dialog is None:
                            mode = 'openimage'
                            dialog = show_dialog(self.trunk_widget,list(["Open","Cancel"]),list(["fileopener"]))
                elif event.type == MOUSEBUTTONDOWN:
                    #if this_frame_image is None:
                    #    set_status("opening image")
                    #    #if mode!='openimage':
                    #    if dialog is None:
                    #        mode='openimage'
                    #        dialog = create_dialog(self.trunk_widget,list(["Open","Cancel"]),list(["fileopener"]))
                    clicked_widget = get_top_widget_at(self.trunk_widget, pygame.mouse.get_pos())
                    
                    if clicked_widget is not None:
                        if bawidgets.is_visual_debug:
                            if clicked_widget.key is not None:
                                set_status("clicked: "+clicked_widget.key)
                            elif clicked_widget.name is not None:
                                set_status("clicked: "+clicked_widget.name)
                            else:
                                set_status("clicked a widget")
                        if (clicked_widget.enabled) and (clicked_widget.handler is not None):
                            clicked_widget.handler()
                    else:
                        if bawidgets.is_visual_debug:
                            set_status("clicked")
            
            if this_frame_image is not None:
                screen.blit(this_frame_image,(0,0))
            if dialog is not None:
                if dialog.result is not None:
                    if dialog.result is not None:
                        if dialog.last_clicked_key is not None:
                            if dialog.result == "Open":
                                print("open image: "+dialog.last_clicked_key)
                                mode = 'drawing'
                            else:
                                print("dialog result:"+str(dialog.result))
                        else:
                            if dialog.result == "Open":
                                print("ERROR: Cannot open since there is no dialog.last_clicked_key (this should never happen)")
                        index = self.trunk_widget.index_of_subwidget_by_kind("dialog")
                        if index is not None:
                            self.trunk_widget.remove_widget_by_index(index)
                            dialog = None
                            #print("dialog finished")
                        else:
                            print("could not remove dialog")
                    
            #if mode == 'openimage':
            #    pass
            bawidgets.draw()
            #clock.tick(60)
            show_status(screen)
            pygame.display.flip()
    
    
def main():
    display_size = (800,600)
    this_program = BASpriteFramer(display_size)
    set_BAWidgetProgram(this_program)
    #global program
    if bawidgets.program is None:
        print("program is None")
    global screen
    screen = bawidgets.screen
    bawidgets.program.run()

if __name__ == "__main__":
    main()
