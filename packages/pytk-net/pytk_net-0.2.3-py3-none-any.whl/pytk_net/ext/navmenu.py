from tkinter import Label, X, LEFT, TOP
from typing import List

from ttkbootstrap import Frame, DARK, SECONDARY, WARNING

from pytk_net.ext.icon import Icon
from pytk_net.utils import get_color


class NavMenuItem:
    def __init__(self, icon, text, side=TOP):
        self.side = side
        self.icon = icon
        self.text = text


class NavMenu(Frame):
    def __init__(self, parent, menus: List[NavMenuItem], default_color=DARK, hover_color=SECONDARY,
                 selected_color=WARNING, icon_txt_color="#FFF", **kwargs):
        self.default_color = default_color
        self.hover_color = hover_color
        self.selected_color = selected_color
        self.icon_txt_color = icon_txt_color
        self.selected_menu = None

        super(NavMenu, self).__init__(parent, bootstyle=self.default_color, **kwargs)
        self.pack_propagate(False)
        for menu in menus:
            self.create_menu(menu)

    def create_menu(self, menu: NavMenuItem):
        nav_menu = Frame(self, height=50, bootstyle=self.default_color, padding=(12, 0, 0, 0))
        icon = Icon(nav_menu, icon_name=menu.icon, size=30, color=self.icon_txt_color, name="icon")
        label = Label(nav_menu, text=menu.text, font=("", 12), name="label")

        nav_menu.pack_propagate(False)
        nav_menu.pack(fill=X, ipadx=10, ipady=10, side=menu.side)
        nav_menu.bind("<Enter>", lambda e: self.enter(e, nav_menu, icon, label))
        nav_menu.bind("<Leave>", lambda e: self.leave(e, nav_menu, icon, label))
        nav_menu.bind("<Button-1>", lambda e: self.click(e, nav_menu, icon, label))
        icon.bind("<Button-1>", lambda e: self.click(e, nav_menu, icon, label))
        label.bind("<Button-1>", lambda e: self.click(e, nav_menu, icon, label))

        icon.configure(background=get_color(self.default_color))
        icon.pack(side=LEFT, padx=(0, 12))

        label.pack(side=LEFT)
        label.configure(background=get_color(self.default_color), fg=self.icon_txt_color)

    def enter(self, _, menu, icon, label):
        if menu == self.selected_menu:
            return
        menu.configure(bootstyle=self.hover_color)
        icon.configure(background=get_color(self.hover_color))
        label.configure(background=get_color(self.hover_color))

    def leave(self, _, menu, icon, label):
        if menu == self.selected_menu:
            return
        menu.configure(bootstyle=self.default_color)
        icon.configure(background=get_color(self.default_color))
        label.configure(background=get_color(self.default_color))

    def click(self, _, menu, icon, label):
        if self.selected_menu is not None:
            _icon = self.selected_menu.children.get("icon")
            _label = self.selected_menu.children.get("label")
            tmp = self.selected_menu
            self.selected_menu = menu
            self.leave(None, tmp, _icon, _label)
        else:
            self.selected_menu = menu

        menu.configure(bootstyle=self.selected_color)
        icon.configure(background=get_color(self.selected_color))
        label.configure(background=get_color(self.selected_color))
