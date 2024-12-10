import os

main_folder_path = "../data"

for subfolder in os.listdir(main_folder_path):
    subfolder_path = os.path.join(main_folder_path, subfolder)
    if os.path.isdir(subfolder_path):
        for filename in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, filename)

            if os.path.isfile(file_path) and not filename.endswith(".json"):
                new_file_path = f"{file_path}.json"
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_path} -> {new_file_path}")