
import pygame
#from pygame import *
import sys
import os
import bawidgets
#from bawidgets import *

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
        

class BASpriteFramer(bawidgets.BAWidgetProgram):


    mode = 'drawing'
    
    def open_file_click(self):
        if this_frame_image is None:
            set_status("opening image")
            if bawidgets.dialog is None:
                bawidgets.show_dialog(self.trunk_widget,list(["Open","Cancel"]),list(["fileopener"]),"file",key="open_image")
    
    def open_game_folder_click(self):
        if bawidgets.dialog is None:
            bawidgets.show_dialog(self.trunk_widget,list(["Open","Cancel"]),list(["fileopener"]),"folder",key="open_game_folder")
            
    def open_game_folder(self, path):
        print("NOT YET IMPLEMENTED: open_game_folder '"+path+"'")
    
    def run(self):
        this_frame_image = None
        playing = True
        clock = pygame.time.Clock()
        title_w = bawidgets.BAWidget("title_w",self.trunk_widget, text="(no game folder loaded)", minimum_rect=pygame.Rect(0,0,self.display_size[0],0), orientation='horizontal',padding=(0,0,0,4),margin=(0,0,0,0))
        #title_w.background_color = 
        self.trunk_widget.add_widget(title_w)
        
        open_button_w = bawidgets.BAWidget("open_button_w", self.trunk_widget, text="Open Game", padding=(0,0,0,0), margin=(1,1,1,1))
        open_button_w.background_color = (64,64,64,255)
        open_button_w.handler = self.open_game_folder_click
        self.trunk_widget.add_widget(open_button_w)
        tab_padding = (0,2,2,0)
        tab_margin = (4,1,2,1)  #left, top, right, bottom
        tab_background_color = (64,64,64,255)
        main_tabs_layout_w = bawidgets.BAWidget("main_tabs_layout_w", self.trunk_widget, orientation='horizontal', padding=(0,0,0,0), margin=(0,0,0,0))
        worlds_button = bawidgets.BAWidget("worlds_button", self.trunk_widget, text="Blocks",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        main_tabs_layout_w.add_widget(worlds_button)
        frames_button = bawidgets.BAWidget("frames_button", self.trunk_widget, text="Frames",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        main_tabs_layout_w.add_widget(frames_button)
        sprites_button = bawidgets.BAWidget("sprites_button", self.trunk_widget, text="Sprites",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        main_tabs_layout_w.add_widget(sprites_button)
        tilesets_button = bawidgets.BAWidget("tilesets_button", self.trunk_widget, text="Tilesets",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        main_tabs_layout_w.add_widget(tilesets_button)
        game_button = bawidgets.BAWidget("game_button", self.trunk_widget, text="Game",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        main_tabs_layout_w.add_widget(game_button)
        self.trunk_widget.add_widget(main_tabs_layout_w)
        
        game_tabs_layout_w = bawidgets.BAWidget("game_tabs_layout_w", self.trunk_widget, orientation='horizontal', padding=(0,0,0,0), margin=(0,0,0,0))
        characters_button = bawidgets.BAWidget("characters_button", self.trunk_widget, text="Characters",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        game_tabs_layout_w.add_widget(characters_button)
        players_button = bawidgets.BAWidget("players_button", self.trunk_widget, text="Players",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        game_tabs_layout_w.add_widget(players_button)
        worlds_button = bawidgets.BAWidget("worlds_button", self.trunk_widget, text="Worlds",padding=tab_padding, margin=tab_margin, background_color=tab_background_color)
        game_tabs_layout_w.add_widget(worlds_button)
        self.trunk_widget.add_widget(game_tabs_layout_w)
        self.trunk_widget.layout()
        while playing:
            #for e in pygame.event.get():
            if bawidgets.dialog is not None:
                if bawidgets.dialog.result is not None:
                    if bawidgets.dialog.result is not None:
                        if bawidgets.dialog.key == "open_image":
                            if bawidgets.dialog.last_clicked_key is not None:
                                if bawidgets.dialog.result == "Open":
                                    print("open image: "+bawidgets.dialog.last_clicked_key)
                                else:
                                    print("dialog result:"+str(bawidgets.dialog.result))
                            else:
                                if bawidgets.dialog.result == "Open":
                                    print("ERROR: Cannot open since there is no dialog.last_clicked_key (this should never happen)")
                        elif bawidgets.dialog.key == "open_game_folder":
                            if bawidgets.dialog.last_clicked_key is not None:
                                if bawidgets.dialog.result == "Open":
                                    #print("open image: "+bawidgets.dialog.last_clicked_key)
                                    self.open_game_folder(bawidgets.dialog.last_clicked_key)
                                else:
                                    print("dialog result:"+str(bawidgets.dialog.result))
                            else:
                                if bawidgets.dialog.result == "Open":
                                    print("ERROR: Cannot open since there is no dialog.last_clicked_key (this should never happen)")
                        else:
                            print("ERROR: unknown dialog command '"+str(bawidgets.dialog.key)+"' stored in dialog.key")
                        bawidgets.dismiss_dialog()
            #if self.mode == 'openimage':
            #    pass
            if this_frame_image is not None:
                screen.blit(this_frame_image,(0,0))
            
            bawidgets.program.trunk_widget.layout()
            bawidgets.draw()
            #clock.tick(60)
            show_status(screen)
            pygame.display.flip()
            
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        if bawidgets.dialog is None:
                            self.open_game_click()
                    elif event.key == pygame.K_ESCAPE:
                        if bawidgets.dialog is not None:
                            bawidgets.dismiss_dialog()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_in_string = "None"
                    clicked_widget = None
                    if bawidgets.dialog is not None:
                        clicked_in_string = "dialog"
                        #print("")
                        #print("dialog is present...")
                        clicked_widget = bawidgets.get_top_widget_at(bawidgets.dialog, pygame.mouse.get_pos())
                    else:
                        #print("")
                        #print("dialog is None...")
                        clicked_in_string = "trunk_widget"
                        clicked_widget = bawidgets.get_top_widget_at(self.trunk_widget, pygame.mouse.get_pos())
                    
                    if clicked_widget is not None:
                        if bawidgets.is_visual_debug:
                            clicked_widget_key = clicked_widget.key
                            if clicked_widget_key is None:
                                clicked_widget_key = clicked_widget.name
                            if clicked_widget_key is not None:
                                if clicked_widget.container is not None and clicked_widget.container.name is not None:
                                    clicked_widget_key = clicked_widget.container.name + "." + clicked_widget_key
                                set_status("clicked: "+clicked_widget_key+" in "+clicked_in_string)
                            else:
                                set_status("clicked a widget in "+clicked_in_string)
                        if (clicked_widget._enabled) and (clicked_widget.handler is not None):
                            clicked_widget.handler()
                    else:
                        if bawidgets.is_visual_debug:
                            set_status("clicked "+clicked_in_string)
    
    
def main():
    display_size = (800,600)
    this_program = BASpriteFramer(display_size)
    bawidgets.set_BAWidgetProgram(this_program)
    #global program
    if bawidgets.program is None:
        print("program is None")
    global screen
    screen = bawidgets.screen
    bawidgets.program.run()

if __name__ == "__main__":
    main()
