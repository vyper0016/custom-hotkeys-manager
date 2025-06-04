import customtkinter as ctk
import os
from hotkeys_profile import PROFILES_FOLDER
from CTkMessagebox import CTkMessagebox
from profile_gui import Profile_GUI
 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotkey Manager")
        self.geometry("450x400")

        # Make column 0, 1, 2 expand horizontally as needed
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        # Make row 1 (the profile_frame row) expand vertically
        self.grid_rowconfigure(1, weight=1)

        self.profiles = []
        self.profile_gui = None
        self.create_widgets()
        self.load_profiles()
        
    def add_profile(self):
        profile_name = ctk.CTkInputDialog(title="New Profile", text="Enter profile name:").get_input()
        
        if not profile_name:
            CTkMessagebox(title="Error", message="Profile name cannot be empty.", icon="cancel", master=self)
            return
        
        if profile_name in self.profiles:
            CTkMessagebox(title="Error", message=f"Profile '{profile_name}' already exists.", icon="cancel", master=self)
            return
        
        try:
            self.on_profile_selected(profile_name)
            self.profiles.append(profile_name)
            self.update_profiles_menu()
            self.set_last_profile()
            print(f"Profile '{profile_name}' created and loaded.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to create profile: {str(e)}", icon="cancel")
            print(f"Error creating profile '{profile_name}': {e}")
        return True

    def update_profiles_menu(self):
        self.profiles_menu.configure(values=self.profiles)
        
    def load_profiles(self):
        for filename in os.listdir(PROFILES_FOLDER):
            if filename.endswith(".json"):
                profile_name = filename[:-5]
                self.profiles.append(profile_name)
                print(f"Loaded profile: {profile_name}")
        self.handle_empty_list()
        self.update_profiles_menu()
        self.set_last_profile()
    
    def on_profile_selected(self, profile_name):
        print(f"Profile selected: {profile_name}")
        # remove all hotkeys from previous profile
        if self.profile_gui is not None:
            self.profile_gui.unhook_all()
        self.reset_profile_frame()
        self.profile_gui = Profile_GUI(profile_name, self.profile_frame)
        
        def delete_profile():
            self.profile_gui.delete()
            self.profiles.remove(self.profile_gui.name)
            self.load_profiles()
                            
        self.delete_profile_button.configure(command=delete_profile)
        
    def set_last_profile(self):
        if self.profiles:
            self.profiles_menu.set(self.profiles[-1])
            self.on_profile_selected(self.profiles[-1])
    
    def create_widgets(self):        
        self.profiles_menu = ctk.CTkOptionMenu(
            self,
            values=[],
            command=self.on_profile_selected, 
            width=200,
        )            
        self.profiles_menu.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.add_profile_button = ctk.CTkButton(
            self,
            text="+",
            command=lambda: self.add_profile(),\
            width=30
        )
        self.add_profile_button.grid(row=0, column=1, padx=1, pady=10, sticky="ew")
            
        self.delete_profile_button = ctk.CTkButton(
            self,
            text="-",
            width=30,
        )
        self.delete_profile_button.grid(row=0, column=2, padx=1, pady=10, sticky="ew")    

    def reset_profile_frame(self):
        self.profile_frame = ctk.CTkScrollableFrame(
            self,
            width=400,
            height=300
        )
        self.profile_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
    def handle_empty_list(self):
        if self.profiles:
            return
        new = self.add_profile()
        while not new:
            new = self.add_profile()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()