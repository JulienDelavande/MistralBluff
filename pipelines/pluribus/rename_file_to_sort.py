import os

def rename_file_to_sort(pluribus_folder):
    for folder in os.listdir(pluribus_folder):
        file_names = [int(file.split('.')[0]) for file in os.listdir(pluribus_folder / folder)]
        size = len(str(max(file_names)))
        for file in os.listdir(pluribus_folder / folder):
            name = str(int(file.split('.')[0]))
            extension = file.split('.')[1]
            name = "0" * (size - len(name)) + name
            os.rename(pluribus_folder / folder / file, pluribus_folder / folder / f"{name}.{extension}")