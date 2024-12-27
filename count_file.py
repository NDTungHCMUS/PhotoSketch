import os
def count_files_and_folders(root_folder):
    total_files = 0
    total_folders = 0

    # Duyệt qua lớp đầu tiên trong root_folder
    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)

        if os.path.isdir(item_path):
            total_folders += 1
            file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
            
            # In ra thư mục có 0 file
            if file_count == 0:
                print(f'Folder: {item} - No files found')
            

        elif os.path.isfile(item_path):
            total_files += 1  # Đếm file trong thư mục gốc

    # In kết quả tổng
    print("\nSummary:")
    print(f"Total folders in '{root_folder}': {total_folders}")
    print(f"Total files in '{root_folder}': {total_files}")

# Đường dẫn thư mục gốc
root_folder = 'train/photo_printer'
count_files_and_folders(root_folder)