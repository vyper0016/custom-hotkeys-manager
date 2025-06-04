import keyboard
import pyperclip

COPY_SNIPPET_ON_HOTKEY = True

class Hotkey:
    def __init__(self, key_combination, text_to_paste):
        self.key_combination = key_combination
        self.text = text_to_paste
        self._hotkey_handler = None
        self.register_hotkey()

    def register_hotkey(self):
        if not self.text:
            self.unregister_hotkey()
            return
        self.unregister_hotkey()  # Ensure no duplicate registration
        print(f"Registering hotkey: {self.key_combination} to paste text: '{self.text}'")
        
        def on_hotkey():
            if COPY_SNIPPET_ON_HOTKEY:
                pyperclip.copy(self.text)                
            keyboard.write(self.text)
            
        self._hotkey_handler = keyboard.add_hotkey(self.key_combination, on_hotkey, timeout=2)

    def unregister_hotkey(self):
        if self._hotkey_handler is not None:
            print(f"Unregistering hotkey: {self.key_combination}")
            keyboard.remove_hotkey(self._hotkey_handler)
            self._hotkey_handler = None
        
    def edit_text(self, new_text):
        self.text = new_text
        self.register_hotkey()
        
    def edit_key_combination(self, new_key_combination):
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