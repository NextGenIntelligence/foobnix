'''
Created on Mar 13, 2010

@author: ivan
'''
import gtk
from foobnix.util.configuration import VERSION, FConfiguration
from foobnix.base import BaseController
from foobnix.base import SIGNAL_RUN_FIRST, TYPE_NONE
from foobnix.util import const

class WindowController(BaseController):

    __gsignals__ = {
        'exit' : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
        'show_preferences' : (SIGNAL_RUN_FIRST, TYPE_NONE, ()),
    }

    def __init__(self, gx_main_window, gx_about):
        BaseController.__init__(self)
        
        self.decorate(gx_main_window)
        

        popup_signals = {
                "on_gtk-preferences_activate": lambda * a: self.emit('show_preferences'),
                "on_file_quit_activate": lambda * a: self.emit('exit'),
                "on_menu_about_activate": self.show_about_window
        }
        gx_main_window.signal_autoconnect(popup_signals)

        self.main_window = gx_main_window.get_widget("foobnixWindow")
        self.main_window.connect("delete-event", self.hide)
        self.main_window.set_title("Foobnix " + VERSION)
        self.main_window.connect("window-state-event", self.window_state_event_cb)
        self.main_window.connect("configure-event", self.on_configure_event)
        #self.main_window.maximize()

        self.about_window = gx_about.get_widget("aboutdialog")
        self.about_window.connect("delete-event", self.hide_about_window)
        
        self.tray_icon = None
        self.configure_state = None
        
    def on_load(self):
        cfg = FConfiguration().configure_state
        if cfg:
            print cfg
            self.main_window.move(cfg[0], cfg[1])
            self.main_window.set_default_size(cfg[2], cfg[3])
    
    def on_save(self):
        FConfiguration().configure_state = self.configure_state
    
    def on_configure_event(self, w, e):
        self.configure_state = [e.x, e.y, e.width, e.height]

    def on_song_started(self, sender, song):
        self.main_window.set_title(song.getTitleDescription())

    def show_about_window(self, *args):
        self.about_window.show()

    def hide_about_window(self, *args):
        self.about_window.hide()
        return True
    
    def destroy(self):
        self.main_window.hide()
        FConfiguration().save()        
        gtk.main_quit() 
        
    def maximize(self):
        self.main_window.maximize()

    def show(self):
        self.main_window.show()
        
    def window_state_event_cb(self, w, event):
        print event
        print event.new_window_state
        print event.changed_mask
      

    def hide(self, *args):
        
        if FConfiguration().on_close_window == const.ON_CLOSE_CLOSE:
            self.destroy()

        elif FConfiguration().on_close_window == const.ON_CLOSE_HIDE:
            self.main_window.hide()
            
        elif FConfiguration().on_close_window == const.ON_CLOSE_MINIMIZE:
            self.main_window.iconify()
        
        return True

    def toggle_visibility(self, *a):
        visible = self.main_window.get_property('visible')
        if visible:            
            self.main_window.hide()
        else:
            self.main_window.show()
            
        

    def decorate(self, gx):
        rc_st = '''
            style "menubar-style" { 
                GtkMenuBar::shadow_type = none
                GtkMenuBar::internal-padding = 0
                }
            class "GtkMenuBar" style "menubar-style"
        '''
        gtk.rc_parse_string(rc_st)

        style = gx.get_widget("label6").get_style()
        background_color = style.bg[gtk.STATE_NORMAL]
        text_color = style.fg[gtk.STATE_NORMAL]
        menu_bar = gx.get_widget("menubar3")
        menu_bar.modify_bg(gtk.STATE_NORMAL, background_color)

        # making main menu look a bit better
        for item in menu_bar.get_children():
            current = item.get_children()[0]
            current.modify_fg(gtk.STATE_NORMAL, text_color)