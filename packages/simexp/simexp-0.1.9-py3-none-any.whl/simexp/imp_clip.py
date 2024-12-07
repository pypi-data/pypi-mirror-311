import yaml
import os
import pyperclip

CONFIG_FILE = 'simexp.yaml'
MAX_SOURCES = 3

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return yaml.safe_load(file)

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        yaml.safe_dump(config, file)

def is_clipboard_content_valid():
    clipboard_content = pyperclip.paste().strip()
    return clipboard_content.startswith('http://') or clipboard_content.startswith('https://')

def update_sources_from_clipboard():
    # Get the current clipboard content
    clipboard_content = pyperclip.paste().strip()
    
    # Check if the clipboard content is a valid URL
    if is_clipboard_content_valid():
        config = load_config()
        
        # Create a new source entry
        new_source = {
            'url': clipboard_content,
            'filename': os.path.basename(clipboard_content).split('.')[0] + '.md'
        }
        
        # Update the configuration with the new source
        if 'CLIPBOARD_SOURCES' not in config:
            config['CLIPBOARD_SOURCES'] = []
        
        config['CLIPBOARD_SOURCES'].append(new_source)
        
        # Ensure we do not exceed the maximum number of sources
        if len(config['CLIPBOARD_SOURCES']) > MAX_SOURCES:
            config['CLIPBOARD_SOURCES'] = config['CLIPBOARD_SOURCES'][-MAX_SOURCES:]
        
        save_config(config)
    else:
        print("Invalid clipboard content. No changes made to the configuration.")

if __name__ == "__main__":
    update_sources_from_clipboard()