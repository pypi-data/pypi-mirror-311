import os
import requests
from datetime import datetime
from .simfetcher import fetch_content  # Use relative import
from .processor import process_content  # Use relative import
from .archiver import save_as_markdown  # Use relative import
import yaml
from .imp_clip import update_sources_from_clipboard, is_clipboard_content_valid  # Use relative import

def init_config():
    config = {
        'BASE_PATH': input("Enter the base path for saving content: "),
        'SOURCES': []
    }
    while True:
        url = input("Enter source URL (or 'done' to finish): ")
        if url.lower() == 'done':
            break
        filename = input("Enter filename for this source: ")
        config['SOURCES'].append({'url': url, 'filename': filename})
    
    with open('simexp.yaml', 'w') as config_file:
        yaml.safe_dump(config, config_file)
    print("Configuration saved to simexp.yaml")

def main():
    # Update sources from clipboard
    update_sources_from_clipboard()

    # Load configuration from YAML file
    config_path = 'simexp.yaml'
    if not os.path.exists(config_path):
        print(f"Configuration file '{config_path}' not found. Please run 'simexp init' to create it.")
        return

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Check if clipboard content is valid
    if not is_clipboard_content_valid():
        print("Invalid clipboard content. Proceeding with existing websites from configuration.")
        sources = config['SOURCES']
    else:
        sources = config['CLIPBOARD_SOURCES']

    base_path = config['BASE_PATH']

    # Create a folder for the current date
    current_date = datetime.now().strftime('%Y%m%d')
    daily_folder = os.path.join(base_path, current_date)
    os.makedirs(daily_folder, exist_ok=True)

    # Fetch, process, and save content for each source
    for source in sources:
        url = source['url']
        filename = source['filename']
        raw_content = fetch_content(url)
        title, cleaned_content = process_content(raw_content)
        save_as_markdown(title, cleaned_content, filename)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init_config()
    else:
        main()