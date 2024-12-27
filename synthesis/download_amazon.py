import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor

DATA_DIR = 'amazon'

def extract_image_file(image_link):
    """
    Extracts the file name from an image URL.
    """
    return image_link.split('/')[-1]

def download_images_for_item(item, category_dir):
    """
    Downloads all images for a given item and saves them in a directory.
    """
    asin = item['asin']
    item_dir = os.path.join(category_dir, asin)
    os.makedirs(item_dir, exist_ok=True)
    img_links = item['highResolutionImages']
    
    for img_link in img_links:
        try:
            response = requests.get(img_link, timeout=10)
            if response.status_code == 200:
                image_file = extract_image_file(img_link)
                image_path = os.path.join(item_dir, image_file)
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                break # take the 1st image only
            else:
                print(f"Failed to download {img_link}: Status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Error downloading {img_link}: {e}")

def process_category(category_file):
    """
    Processes a category JSON file to download all images for items in the category.
    """
    category = category_file.split('.')[0]
    print(f'Processing category: {category}')
    category_dir = os.path.join(DATA_DIR, category)
    os.makedirs(category_dir, exist_ok=True)

    file_path = os.path.join(DATA_DIR, category_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    if not items:
        raise ValueError(f"No items found in the file: {category_file}")
    
    # Use ThreadPoolExecutor to process items concurrently
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(download_images_for_item, item, category_dir) for item in items]
        for future in futures:
            future.result()

if __name__ == '__main__':
    for category_file in os.listdir(DATA_DIR):
        if category_file.endswith('.json'):
            process_category(category_file)
