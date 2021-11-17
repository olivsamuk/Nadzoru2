import sys
import gi
import os
from gi.repository import Gdk, Gio, Gtk

from machine.automaton import Automaton
from gui.automaton_editor import AutomatonEditor
from gui.automaton_simulator import AutomatonSimulator
from gui.main_window import MainWindow

class MouseButtons:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.nadzoru2.application", **kwargs)
        self.elements = list()

    def create_action(self, action_name, callback):
        action = Gio.SimpleAction.new(action_name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.window = MainWindow(application=self, title="Nadzoru 2")

        self.create_action('new-automaton', self.on_new_automaton)
        self.create_action('load-automaton', self.on_load_automaton)
        self.create_action('save-automaton', self.on_save_automaton)
        self.create_action('save_as-automaton', self.on_save_as_automaton)
        self.create_action('edit-automaton', self.on_edit_automaton)
        self.create_action('simulate-automaton', self.on_simulate_automaton)
        self.create_action('import-ides', self.on_import_ides)
        self.create_action('close-tab', self.on_close_tab)
        self.create_action('quit', self.on_quit)
        self.create_action('export-ides', self.on_export_ides)

        self.window.toolpallet.add_button('file', label="Save", icon_name='gtk-floppy', callback=self.on_save_automaton)

        builder = Gtk.Builder()
        builder.add_from_file("gui/ui/menubar.ui")
        self.menubar = builder.get_object("menubar")
        self.set_menubar(self.menubar)

    def do_activate(self):
        self.window.show_all()
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()

        self.activate()
        return

    def validade_quit(self):
        # TODO: For each file not save ask: cancel, discard, save. If no file just quit!
        dialog = Gtk.Dialog("Nazoru2", self.window)
        dialog.modify_style
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_DISCARD, Gtk.ResponseType.YES, Gtk.STOCK_SAVE, Gtk.ResponseType.APPLY)
        dialog.set_default_size(150, 100)

        label = Gtk.Label()
        #label.set_text("File {} not saved!")
        label.set_text("Do you really want to exit? All work will be lost")
        label.set_justify(Gtk.Justification.LEFT)

        box_dialog = dialog.get_content_area()
        box_dialog.add(label)
        box_dialog.show_all()

        result = dialog.run()
        dialog.destroy()

        if result == Gtk.ResponseType.YES or result == Gtk.ResponseType.APPLY:
            self.quit()

    def on_new_automaton(self, action, param):
        automaton = Automaton()
        self.elements.append(automaton)
        editor = AutomatonEditor(automaton, self)
        self.window.add_tab(editor, editor.automaton.get_file_name())
        editor.connect('nadzoru-editor-change', self.on_editor_change)

    def on_load_automaton(self, action, param):
        dialog = Gtk.FileChooserDialog("Choose file", self.window, Gtk.FileChooserAction.OPEN,
            ("_Cancel", Gtk.ResponseType.CANCEL, "_Open", Gtk.ResponseType.ACCEPT, "_Edit", Gtk.ResponseType.OK))
        dialog.set_property('select-multiple', True)
        result = dialog.run()
        if result in [Gtk.ResponseType.ACCEPT, Gtk.ResponseType.OK]:
            for file_path_name in dialog.get_filenames():
                file_name = os.path.basename(file_path_name)
                automaton = Automaton()
                try:
                    automaton.load(file_path_name)
                except:
                    dialog.destroy()
                    return
                self.elements.append(automaton)
                if result == Gtk.ResponseType.OK:
                    editor = AutomatonEditor(automaton, self)
                    editor.connect('nadzoru-editor-change', self.on_editor_change)
                    self.window.add_tab(editor, file_name)
        dialog.destroy()

    def on_save_automaton(self, action, param=None):
        widget = self.window.get_current_tab_widget()
        if (widget is None) or type(widget) != AutomatonEditor:
            return
        automata = widget.automaton

        file_path_name = automata.get_file_path_name()
        if file_path_name == None:
            self._save_dialog(automata)
            self.window.set_tab_page_title(widget, automata.get_file_name())
        else:
            automata.save(file_path_name)
        self.window.set_tab_label_color(widget, '#000')

    def on_save_as_automaton(self, action, param=None):
        widget = self.window.get_current_tab_widget()
        if (widget is None) or type(widget) != AutomatonEditor:
            return
        automata = widget.automaton
        self._save_dialog(automata)
        self.window.set_tab_page_title(widget, automata.get_file_name())
        self.window.set_tab_label_color(widget, '#000')

    def _save_dialog(self, automata):
        dialog = Gtk.FileChooserDialog("Choose file", self.window, Gtk.FileChooserAction.SAVE,
            ("_Cancel", Gtk.ResponseType.CANCEL, "_Save", Gtk.ResponseType.OK))
        result = dialog.run()
        if result ==  Gtk.ResponseType.OK:
            file_path = (dialog.get_filename())
            if not(file_path.lower().endswith('.xml')):
                file_path = f'{file_path}.xml'
            automata.save(file_path)
        dialog.destroy()

    def on_edit_automaton(self, action, param):
        print("You opened in editor automata")

    def on_simulate_automaton(self, action, param):
        # TODO: open dialog to select from self.elements
        from test_automata import automata_01  # For testing
        automaton = Automaton()
        automata_01(automaton)  # For testing
        simulator = AutomatonSimulator(automaton)
        self.window.add_tab(simulator, "Simulator")

    def on_close_tab(self, action, param):
        self.window.remove_tab(self.window.note.get_current_page())

    def on_editor_change(self, editor, *args):
        self.window.set_tab_label_color(editor, '#F00')



    def on_import_ides(self, action, param):
        dialog = Gtk.FileChooserDialog("Choose file", self.window, Gtk.FileChooserAction.OPEN,
            ("_Cancel", Gtk.ResponseType.CANCEL, "_Open", Gtk.ResponseType.ACCEPT, "_Edit", Gtk.ResponseType.OK))
        dialog.set_property('select-multiple', True)
        result = dialog.run()
        if result in [Gtk.ResponseType.ACCEPT, Gtk.ResponseType.OK]:
            for full_path_name in dialog.get_filenames():
                file_name = os.path.basename(full_path_name)
                automaton = Automaton()
                automaton.ides_import(full_path_name)
                self.elements.append(automaton)
                if result == Gtk.ResponseType.OK:
                    editor = AutomatonEditor(automaton, self)
                    editor.connect('nadzoru-editor-change', self.on_editor_change)
                    self.window.add_tab(editor, "{} *".format(file_name))
        dialog.destroy()

    def on_export_ides(self, action, param):
        dialog = Gtk.FileChooserDialog("Choose File", self.window, Gtk.FileChooserAction.SAVE,
            ("_Cancel", Gtk.ResponseType.CANCEL, "_Export", Gtk.ResponseType.OK))
        result = dialog.run()
        if result == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            file_path = f'{file_path}.xmd'
            widget = self.window.get_current_tab_widget()
            if type(widget) == AutomatonEditor:
                automata = widget.automaton
                automata.ides_export(file_path)
        dialog.destroy()

    def on_quit(self, action, param):
        self.validade_quit()



