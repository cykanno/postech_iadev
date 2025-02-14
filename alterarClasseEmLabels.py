import os

def modify_txt_files(directory):
    """
    Lists .txt files in a directory, changes the first value in each file to 0,
    and saves the modified content with the same filename.

    Args:
        directory (str): The path to the directory containing the .txt files.
    """

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r") as file:
                    lines = file.readlines()

                modified_lines = []
                for line in lines:
                    parts = line.split()
                    if parts:
                        parts[0] = "0"
                        modified_lines.append(" ".join(parts) + "\n")
                    else:
                        modified_lines.append("\n")

                with open(filepath, "w") as file:
                    file.writelines(modified_lines)

                print(f"Modified: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


# Example usage:
current_directory = os.getcwd()

directory_path = current_directory + "/Fase_V/kaggle/Weapon_Detection_YOLOv8/imagens/val/labels"  # Replace with the actual path to your directory
modify_txt_files(directory_path)

directory_path = current_directory + "/Fase_V/kaggle/Weapon_Detection_YOLOv8/imagens/test/labels"  # Replace with the actual path to your directory
modify_txt_files(directory_path)

directory_path = current_directory + "/Fase_V/kaggle/Weapon_Detection_YOLOv8/imagens/train/labels"  # Replace with the actual path to your directory
modify_txt_files(directory_path)
