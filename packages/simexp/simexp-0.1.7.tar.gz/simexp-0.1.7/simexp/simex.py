import os
import requests
from datetime import datetime
from simexp.simfetcher import fetch_content
from .processor import process_content  # Use relative import
from .archiver import save_as_markdown  # Use relative import
import yaml
from .imp_clip import update_sources_from_clipboard, is_clipboard_content_valid  # Use relative import

def main():
    # Update sources from clipboard
    update_sources_from_clipboard()

    # Load configuration from YAML file
    with open('config.yaml', 'r') as config_file:
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
    main()