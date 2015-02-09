# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import time
import logging

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from ava.shell.base import ShellBase
from ava.shell import resource_path

logger = logging.getLogger(__name__)


class StatusIcon(object):
    def __init__(self, shell):
        self.shell = shell
        self.ind = appindicator.Indicator.new("EAvatar-indicator",
                                           resource_path("home/static/images/eavatar.png"),
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_icon_theme_path(resource_path('home/static/images'))

        #self.ind = appindicator.Indicator.new_with_path ("EAvatar-indicator", "eavatar.png",
        #        appindicator.IndicatorCategory.APPLICATION_STATUS,
        #        resource_path('res'))
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon("eavatar.png")

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = Gtk.Menu()

        self.open_item = Gtk.MenuItem.new_with_label(u"Open...")
        self.open_item.connect("activate", self.on_open_frame)
        self.open_item.show()

        self.restart_item = Gtk.MenuItem.new_with_label(u"Restart")
        self.restart_item.connect("activate", self.on_restart)
        self.restart_item.show()

        self.quit_item = Gtk.MenuItem.new_with_label(u"Exit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()

        self.menu.append(self.open_item)
        self.menu.append(self.restart_item)
        self.menu.append(Gtk.SeparatorMenuItem.new())
        self.menu.append(self.quit_item)

    def on_open_frame(self, sender):
        self.shell.open_main_ui()

    def on_restart(self, sender):
        logger.debug("Restarting agent...")
        self.shell.stop_server()

        self.shell.start_server()

    def quit(self, widget):
        self.ind.set_status(appindicator.IndicatorStatus.PASSIVE)
        Gtk.main_quit()


def yieldToOthers():
    time.sleep(0.1)
    #GLib.timeout_add(200, yieldToOthers)
    return True


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()
        self.statusIcon = StatusIcon(self)

    def run(self):
        #gtk.timeout_add(200, self._on_idle)
        #GLib.timeout_add(200, yieldToOthers, priority=GLib.PRIORITY_DEFAULT)
        #GObject.idle_add(self._on_idle)
        Gtk.main()


if __name__ == '__main__':
    shell = Shell()
    shell.run()

