#~ import os
import sys
import gi
from gi.repository import GLib, Gio, Gtk

from renderer import AutomatonRenderer


class FileIconMixin:
    def __init__(self, *args, icon_file_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        if icon_file_name is not None:
            image_widget = Gtk.Image()
            image_widget.set_from_file(icon_file_name)
            self.set_icon_widget(image_widget)


class FileIconToolButton(FileIconMixin, Gtk.ToolButton):
    pass


class FileIconToggleToolButton(FileIconMixin, Gtk.ToggleToolButton):
    def __init__(self, *args, tool_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool_id = tool_id


class AutomatonEditorToolPalette(Gtk.ToolPalette):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tool = None
        self.groups = {}

        self.add_group('file', "File")
        self.add_group('edit', "Edit")
        self.add_group('view', "view")

        #~ self.add_button('file', label="Save", icon_name='gtk-floppy', callback=self.on_click_test)
        self.add_toggle_button('edit', tool_id='state_add', label="Add State", icon_file_name='./res/icons/state_add.png')
        self.add_toggle_button('edit', tool_id='state_initial', label="Make Initial State", icon_file_name='./res/icons/state_initial.png')
        self.add_toggle_button('edit', tool_id='state_marked', label="Mark State", icon_file_name='./res/icons/state_marked.png')
        self.add_toggle_button('edit', tool_id='transition_add', label="Add Transition", icon_file_name='./res/icons/transition_add.png')

    def add_group(self, name, label):
        assert name not in self.groups, "group '{}' already exists".format(name)
        self.groups[name] = Gtk.ToolItemGroup.new(label)
        self.add(self.groups[name])

    def add_button(self, group_name, *args, position=-1, callback=None, **kwargs):
        btn = FileIconToolButton(*args, **kwargs)
        self.groups[group_name].insert(btn, position)
        if callback is not None:
            btn.connect('clicked', callback)

    def add_toggle_button(self, group_name, *args, position=-1, **kwargs):
        btn = FileIconToggleToolButton(*args, **kwargs)
        self.groups[group_name].insert(btn, position)
        btn.connect('toggled', self.on_toggled)

    def get_selected_tool(self):
        if self.tool is None:
            return ''
        return self.tool.tool_id

    def clear_selection(self):
        if not self.tool is None:
            self.tool.set_active(False)
            self.tool = None

    def on_toggled(self, btn):
        if btn.get_active() and self.tool != btn:
            if self.tool is not None:
                self.tool.set_active(False)
            self.tool = btn
        else:
            self.tool = None

    #~ def on_click_test(self, *args):
        #~ print(self.get_selected_tool())

class AutomatonEditor(Gtk.Box):
    def __init__(self, automaton, *args, **kwargs):
        if 'spacing' not in kwargs:
            kwargs['spacing'] = 2
        super().__init__(*args, **kwargs)

        self.automaton = automaton
        self.ar = AutomatonRenderer(self.automaton)
        self.selected_state = None
        self._build()

    def _build(self):
        self.paned = Gtk.Paned()
        self.scrolled = Gtk.ScrolledWindow.new()
        self.drawing_area = Gtk.DrawingArea.new()
        # self.listbox = Gtk.ListBox()

        self.pack_start(self.paned, True, True, 0)
        self.paned.pack1(self.scrolled, True, True)
        self.scrolled.add(self.drawing_area)


        self.drawing_area.connect("draw", self.on_draw)

    def on_draw(self, wid, cr):
        pass
        # self.ar.draw(cr, self.automaton)


