import keyboard

class Hotkey:
    def __init__(self, key_combination, text_to_paste):
        self.key_combination = key_combination
        self.text = text_to_paste
        self.callback = lambda: keyboard.write(text_to_paste)
        self.register_hotkey()

    def register_hotkey(self):
        keyboard.add_hotkey(self.key_combination, self.callback)

    def unregister_hotkey(self):
        keyboard.remove_hotkey(self.key_combination)
        
    def edit_text(self, new_text):
        self.callback = lambda: keyboard.write(new_text)
        self.text = new_text
        self.unregister_hotkey()
        self.register_hotkey()
        
    def edit_key_combination(self, new_key_combination):
        self.unregister_hotkey()
        self.key_combination = new_key_combination
        self.register_hotkey()
        
    def as_dict(self):
        return {
            "key_combination": self.key_combination,
            "text": self.text
        }
        
    def __str__(self):
        return f"Hotkey(key_combination={self.key_combination}, text_to_paste={self.text})"

if __name__ == "__main__":
    # Example usage
    hotkey = Hotkey('ctrl+1', 'Hello, this is a test paste!')
    print(f"Hotkey '{hotkey.key_combination}' registered to paste text.")
    print(hotkey)
    print(hotkey.as_dict())
    
    #edit the hotkey text
    hotkey.edit_text('This is the updated text to paste!')
    print(f"Hotkey text updated")
    print(hotkey)
    
    # Keep the script running to listen for the hotkey
    keyboard.wait('esc')  # Press 'esc' to exit the script
    hotkey.unregister_hotkey()
    print("Hotkey unregistered.")