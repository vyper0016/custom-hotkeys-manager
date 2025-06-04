import json
from hotkey import Hotkey
import os

PROFILES_FOLDER = "profiles"
os.makedirs(PROFILES_FOLDER, exist_ok=True)

class Profile:
    def __init__(self, name:str):
        self.name = name
        self.hotkeys = []
        try:
            with open(f"{PROFILES_FOLDER}/{name}.json", "r") as file:
                data = json.load(file)
                hotkey_dicts = data.get("hotkeys", [])
                self.construct_hotkeys(hotkey_dicts)
        except FileNotFoundError:
            print(f"Profile '{name}' not found. Creating a new profile.")
            self.save()
            
    def construct_hotkeys(self, dict_list:list):
        for d in dict_list:
            hotkey = Hotkey(d["key_combination"], d["text"])
            self.hotkeys.append(hotkey)
            
            
    def get_hotkeys_as_dict(self):
        return [hotkey.as_dict() for hotkey in self.hotkeys]
        
    def save(self):
        with open(f"{PROFILES_FOLDER}/{self.name}.json", "w") as file:
            data = {"hotkeys": self.get_hotkeys_as_dict()}
            json.dump(data, file, indent=4)
    
    def hotkey_combination_exists(self, key_combination:str) -> bool:
        return any(hotkey.key_combination == key_combination for hotkey in self.hotkeys)    
    
    def add_hotkey_new(self, key_combination:str, text_to_paste:str) -> int:        
        return self.add_hotkey(Hotkey(key_combination, text_to_paste))
    
    def add_hotkey(self, hotkey: Hotkey) -> int:
        if self.hotkey_combination_exists(hotkey.key_combination):
            raise ValueError(f"Hotkey with key combination '{hotkey.key_combination}' already exists in profile '{self.name}'.")
        self.hotkeys.append(hotkey)
        hotkey.register_hotkey()
        self.save()
        
        #return the index of the newly added hotkey
        return len(self.hotkeys) - 1
        
    def remove_hotkey(self, index:int):
        hotkey = self.hotkeys.pop(index)
        hotkey.unregister_hotkey()
        self.save()
            
    def list_hotkeys(self):
        return self.hotkeys
    
    def delete(self):
        try:
            os.remove(f"{PROFILES_FOLDER}/{self.name}.json")
        except FileNotFoundError:
            pass
        self.hotkeys = []
    
    def edit_hotkey(self, index:int, new_text:str = None, new_key_combination:str = None):
        hotkey = self.hotkeys[index]
        if new_text is not None:
            hotkey.edit_text(new_text)
        if new_key_combination is not None:
            hotkey.edit_key_combination(new_key_combination)
        self.save()
    
    def __str__(self):
        s = f"Profile(name={self.name}, hotkeys=[\n"
        for c, hotkey in enumerate(self.hotkeys):
            s += str(hotkey) + '\n'
        s += "])"
        return s
            
    
if __name__ == "__main__":
    # Example usage
    profile = Profile("default")
    print(f"Loaded profile: {profile.name}")
    
    # Add a new hotkey
    new_hotkey = Hotkey("ctrl+alt+h", "Hello, world!")
    profile.add_hotkey(new_hotkey)
    print("Added new hotkey.")
    print(profile)
    print()

    # List all hotkeys
    print("Current hotkeys list:")
    for hk in profile.list_hotkeys():
        print(hk)

    # Edit the first hotkey
    profile.edit_hotkey(0, new_text="Updated text")
    print("Edited first hotkey.")
    print(profile)
    print()

    # Remove the first hotkey (if exists)
    profile.remove_hotkey(0)
    print("Removed first hotkey.")
    print(profile)
    print()
    # Save and print profile
    profile.save()
    
    