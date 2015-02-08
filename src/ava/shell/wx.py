# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import wx
from ava.shell import resource_path
from ava.shell.base import ShellBase


class StatusIcon(wx.TaskBarIcon):
    TBMENU_RESTORE = wx.NewId()
    TBMENU_CLOSE   = wx.NewId()
    TBMENU_NOTIFY  = wx.NewId()
    TBMENU_REMOVE  = wx.NewId()

    def __init__(self, shell):
        wx.TaskBarIcon.__init__(self)
        self._shell = shell

        self.SetIcon(self._shell.app.icon, "EAvatar")
        self.imgidx = 1

        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarNotify, id=self.TBMENU_NOTIFY)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

        wx.GetApp().Bind(wx.EVT_MENU_CLOSE, self.OnClose)
        #app.Bind(wx.EVT_MENU_CLOSE, self.OnClose)

    def CreatePopupMenu(self):
        #print("Context menu opened.")
        self.menu = wx.Menu()
        #self.menu.SetTitle("ContextMenu :)")
        self.menu.Append(self.TBMENU_RESTORE, u"開啟主視窗...")
        self.menu.Append(self.TBMENU_NOTIFY, u"通知訊息")
        self.menu.Append(wx.ID_EXIT,   u"結束影化身")
        return self.menu

    def OnClose(self, evt):
        print("Context menu closed.")
        print(evt.GetMenu().GetTitle())

    def OnTaskBarActivate(self, evt):
        self._shell.on_open_ui()

    def OnTaskBarNotify(self, evt):
        msg = wx.NotificationMessage()
        msg.SetParent(self._shell.frame)
        msg.SetTitle(u"Message")
        msg.SetMessage("Hello from EAvatar")
        msg.Show()

    def OnTaskBarClose(self, evt):
        self._shell.on_destroy()


class MyFrame(wx.Frame):
    def __init__(self, _shell):
        wx.Frame.__init__(self, None, style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)
        self._shell = _shell
        self.SetIcon(self._shell.app.icon)


class MyApp(wx.App):
    def __init__(self):
        super(MyApp, self).__init__(redirect=False)
        self.icon = wx.Icon(resource_path('res/eavatar.ico'), wx.BITMAP_TYPE_ICO)


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()

        self.app = MyApp()
        self.frame = MyFrame(self)
        self.status_icon = StatusIcon(self)

    def on_open_ui(self):
        self.open_main_ui()

    def on_destroy(self):
        self.stop_server()

        self.status_icon.RemoveIcon()
        self.status_icon.Destroy()
        self.app.Destroy()
        sys.exit(0)

    def run(self):
        self.app.MainLoop()