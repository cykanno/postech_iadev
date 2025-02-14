import os
import re

def delete_files_without_strings(directory, strings_to_keep):
    """
    Deletes files in a directory that do not contain any of the specified strings in their names.

    Args:
        directory (str): The path to the directory.
        strings_to_keep (list): A list of strings. Files containing any of these strings will be kept.
    """

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Create a regex pattern that matches if ANY of the strings_to_keep are present
            pattern = re.compile("|".join(strings_to_keep))  # Join strings with OR operator

            if not pattern.search(filename): # if the filename does NOT contain any of the strings to keep
                os.remove(file_path)
                print(f"Deleted: {filename}")


# Example usage:
current_directory = os.getcwd()

directory_to_clean = current_directory + "/Fase_V/kaggle/Weapon_Detection_YOLOv8/imagens/val/labels" 

strings_to_keep = ["knife", "KravMaga", "HBmframe"]
delete_files_without_strings(directory_to_clean, strings_to_keep)

directory_to_clean = current_directory + "/Fase_V/kaggle/Weapon_Detection_YOLOv8/imagens/val/images" # Replace with the actual path to your directory
delete_files_without_strings(directory_to_clean, strings_to_keep)
