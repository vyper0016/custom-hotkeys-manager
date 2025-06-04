from hotkeys_profile import Profile
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import pyperclip

DEFAULT_TO_TEXT_FROM_CLIPBOARD = True

class Hotkey_GUI():
    def __init__(self, hotkey, row, frame):
        # two editable text fields for key combination and text to paste

        self.frame = frame
        self.row = row
        self.hotkey = hotkey
        self.index = row - 1

        # Make column 0 expandable
        self.frame.grid_columnconfigure(0, weight=1)

        text_entry = ctk.CTkEntry(self.frame, width=200)
        text_entry.insert(0, hotkey.text)
        text_entry.grid(row=row, column=0, padx=5, pady=5, sticky="ew")  # <-- sticky="ew"
        self.text_entry = text_entry

        key_combination_entry = ctk.CTkEntry(self.frame, width=80)
        key_combination_entry.insert(0, hotkey.key_combination)
        key_combination_entry.grid(row=row, column=1, padx=5, pady=5)
        self.key_combination_entry = key_combination_entry

        remove_button = ctk.CTkButton(self.frame, text="-", width=30)
        remove_button.grid(row=row, column=2, padx=5, pady=5)
        self.remove_button = remove_button
        

class Profile_GUI(Profile):
    def __init__(self, name: str, frame):
        super().__init__(name)
        self.frame = frame
        self.create_widgets()
        
    def create_widgets(self):
        self.hotkey_guis = []
        text_label = ctk.CTkLabel(self.frame, text="Text")
        text_label.grid(row=0, column=0, padx=5, pady=5)
        key_combination_label = ctk.CTkLabel(self.frame, text="Hotkey")
        key_combination_label.grid(row=0, column=1, padx=5, pady=5)
        for c, hotkey in enumerate(self.hotkeys):
            self.hotkey_guis.append(Hotkey_GUI(hotkey, c + 1, self.frame))
        
        self.add_hotkey_button = ctk.CTkButton(self.frame, text="+", command=self.add_hotkey_gui, width=300)
        self.add_hotkey_button.grid(row=len(self.hotkeys) + 1, column=0, padx=5, pady=5, columnspan=3)
        self.bind_changes()
        
    def add_hotkey_gui(self):
        try:
            key_combination = ctk.CTkInputDialog(title="Add Hotkey", text="Enter key combination (e.g., Ctrl+Shift+A):").get_input()
            if not key_combination:
                return
            
            text = ''
            if DEFAULT_TO_TEXT_FROM_CLIPBOARD:
                text = pyperclip.paste()
            self.add_hotkey_new(key_combination, text)
        except ValueError as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return
        
        self.update_frame()
    
    def edit_hotkey_gui(self, index, new_text=None, new_key_combination=None):
        try:
            self.edit_hotkey(index, new_text=new_text, new_key_combination=new_key_combination)
        except ValueError as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return
    
    def bind_changes(self):
        for gui in self.hotkey_guis:
            gui.text_entry.bind("<KeyRelease>", lambda e, g=gui: self.edit_hotkey_gui(g.index, new_text=g.text_entry.get()))
            gui.key_combination_entry.bind("<KeyRelease>", lambda e, g=gui: self.edit_hotkey_gui(g.index, new_key_combination=g.key_combination_entry.get()))
            def remove_hotkey(g):
                self.remove_hotkey(g.index)
                self.update_frame()
                
            gui.remove_button.configure(command=lambda g=gui: remove_hotkey(g))
        
    def update_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_widgets()