import customtkinter as ctk
import os
from hotkeys_profile import Profile, PROFILES_FOLDER
from CTkMessagebox import CTkMessagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotkey Manager")
        self.geometry("400x300")
        
        self.profiles = []
        self.create_widgets()
        self.load_profiles()
        
    def add_profile(self, profile_name):
        if not profile_name:
            CTkMessagebox(title="Error", message="Profile name cannot be empty.", icon="cancel")
            return
        
        if any(profile.name == profile_name for profile in self.profiles):
            CTkMessagebox(title="Error", message=f"Profile '{profile_name}' already exists.", icon="cancel")
            return
        
        try:
            new_profile = Profile(profile_name)
            self.profiles.append(new_profile)
            self.profiles_menu.configure(values=[profile.name for profile in self.profiles] + ["Create New Profile"])
            self.profiles_menu.set(profile_name)
            print(f"Profile '{profile_name}' created and loaded.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to create profile: {str(e)}", icon="cancel")
            print(f"Error creating profile '{profile_name}': {e}")
        
    def load_profiles(self):
        for filename in os.listdir(PROFILES_FOLDER):
            if filename.endswith(".json"):
                profile_name = filename[:-5]
                profile = Profile(profile_name)
                self.profiles.append(profile)
                print(f"Loaded profile: {profile_name}")
        self.profiles_menu.configure(values=[profile.name for profile in self.profiles] + ["Create New Profile"])
        # select the first profile by default
        if self.profiles:
            self.profiles_menu.set(self.profiles[0].name)
            self.on_profile_selected(self.profiles[0].name)
    
    def on_profile_selected(self, profile_name):
        if profile_name == "Create New Profile":
            new_profile_name = ctk.CTkInputDialog(text="Enter new profile name:").get_input()
            self.add_profile(new_profile_name)
        else:
            print(f"Selected profile: {profile_name}")
    
    def create_widgets(self):
        
        self.profiles_menu = ctk.CTkOptionMenu(
            self,
            values=[],
            command=self.on_profile_selected
        )
        self.profiles_menu.pack(pady=10)
        
            
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()