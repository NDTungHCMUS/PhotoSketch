import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from synthesis.split_data import split_data
from synthesis.download_images import download_images_for_item
from synthesis.title_extractor import extract_titles_from_items, save_category_titles

OUTPUT_DIR = 'amazon'
TITLE_JSON_FILE = 'title.json'
title_data = {}  # Lưu trữ dữ liệu để ghi ra file JSON

def process_category(category_file):
    category = category_file.split('.')[0]
    print(f'Processing category: {category}')

    file_path = os.path.join('amazon', category_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    if not items:
        raise ValueError(f"No items found in the file: {category_file}")
    
    # Chia thành 2 tập train và test
    train_items, test_items = split_data(items)
    
    # Tải ảnh tập train
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(download_images_for_item, item, category, "train") for item in train_items]
        for future in futures:
            future.result()

    # Tải ảnh tập test
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(download_images_for_item, item, category, "test") for item in test_items]
        for future in futures:
            future.result()
    
    # Extract titles for train and test sets
    # extract_titles_from_items(train_items, category, title_data)
    # extract_titles_from_items(test_items, category, title_data)
    save_category_titles("train_mapping_title", category, train_items)
    save_category_titles("test_mapping_title", category, test_items)


# category_files = ["applicance.json", "camera.json", "clothes.json", "computers.json", "cpu.json"]
# category_files = ["desk.json", "drone.json", "fan.json", "fitness_trackers.json", "game_controller.json"]
# category_files = ["headphones.json", "keyboards.json", "photo_printer.json", "shoes.json", "smartphone.json"]
category_files = ["smartwatches.json", "soundbar.json", "tablet.json", "toys.json", "tripod.json", "usb_driver.json", "vr_gaming.json"]
if __name__ == '__main__':
    # for category_file in os.listdir('amazon'):
    #     if category_file.endswith('.json'):
    #         process_category(category_file)

    for category_file in category_files:
        process_category(category_file)
    # Ghi ra tệp title.json ở ngoài cùng cấp với folder train và data
    # with open(TITLE_JSON_FILE, 'w', encoding='utf-8') as f:
    #     json.dump(title_data, f, indent=4, ensure_ascii=False)
    # print(f'Title JSON file saved as {TITLE_JSON_FILE}')
