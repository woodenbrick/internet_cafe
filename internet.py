#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import gtk.glade
import hashlib
import time
import gobject
import pango
PRICE = 0.04 #price in pounds
PER = 1 #for this many minutes

class InternetTimer():
    def __init__(self):
        self.wTree = gtk.glade.XML("internet.glade")
        self.wTree.signal_autoconnect(self)
        self.wTree.get_widget("main_window").move(gtk.gdk.screen_width() - 50, gtk.gdk.screen_height() - 50)
        self.wTree.get_widget("main_window").set_keep_above(True)
        self.wTree.get_widget("main_window").modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("green"))
        self.wTree.get_widget("main_window").set_tooltip_text("£" + str(PRICE) + " for " + str(PER) + " minute")
        self.start_timer()
    
    def start_timer(self):
        try:
            gobject.source_remove(self.timer)
        except AttributeError:
            pass
        self.start_time = time.time()
        self.update_time()
        self.timer = gobject.timeout_add(1000, self.update_time)
        
    def on_password_insert(self, *args):
        if hashlib.sha1(self.wTree.get_widget("password").get_text()).hexdigest() == 'b1b3773a05c0ed0176787a4f1574ff0075f7521e':
            admin = True
        else:
            admin = False   
        self.wTree.get_widget("reset").set_sensitive(admin)
        self.wTree.get_widget("quit").set_sensitive(admin)
            
    def on_reset_clicked(self, *args):
        self.wTree.get_widget("password").set_text("")
        self.wTree.get_widget("reset").set_sensitive(False)
        self.wTree.get_widget("quit").set_sensitive(False)
        self.start_timer()
        self.wTree.get_widget("admin").hide()

    def update_time(self):
        time_since = time.time() - self.start_time
        time_split = [int(time_since / 60), int(time_since % 60)]
        self.update_cost(time_split[0])
        for i in range(0, 2):
            if time_split[i] == 0:
                time_split[i] = str("00")
            elif time_split[i] <= 9:
                time_split[i] = str("0" + str(time_split[i]))
            else:
                time_split[i] = str(time_split[i])
        self.wTree.get_widget("timer").set_text(":".join(time_split))
        return True
    
    def update_cost(self, mins):
        cost = "£" + str(round(mins / PER * PRICE + PRICE, 2))
        if cost[-2] == ".":
            cost += "0"
        self.wTree.get_widget("money").set_text(cost)
        
    def open_admin(self, *args):
        self.wTree.get_widget("admin").show()
        
    def on_cancel_clicked(self, *args):
        self.wTree.get_widget("admin").hide()
    
    def on_quit_clicked(self, *args):
        gtk.main_quit()

InternetTimer()
gtk.main()