import os
import requests


def extract_image_file(image_link):
    return image_link.split('/')[-1]


def download_images_for_item(item, category, output_dir):
    asin = item.get('asin')

    # Bỏ qua nếu không có ASIN
    if not asin:
        print(f"Skipping item with no ASIN in category: {category}")
        return

    img_links = item.get('highResolutionImages') or item.get('galleryThumbnails', [])

    item_dir = os.path.join(output_dir, category, asin)
    os.makedirs(item_dir, exist_ok=True)

    # Tải ảnh
    for img_link in img_links:
        try:
            response = requests.get(img_link, timeout=10)
            if response.status_code == 200:
                image_file = extract_image_file(img_link)
                image_path = os.path.join(item_dir, image_file)
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {image_file} to {item_dir}")
                break  # Dừng sau khi tải xong ảnh đầu tiên
            else:
                print(f"Failed to download {img_link}: Status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Error downloading {img_link}: {e}")
