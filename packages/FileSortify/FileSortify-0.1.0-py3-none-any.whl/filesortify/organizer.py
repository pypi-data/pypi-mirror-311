import os
import shutil

def organize_files_by_extension(directory, nested=False):
    # Define file categories based on extension
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
        'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm'],
        'Text Files': ['.txt', '.md', '.pdf', '.docx', '.xlsx', '.pptx'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
        'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
        'Others': []
    }

    # Create subdirectories for each file category
    for category in file_types:
        category_path = os.path.join(directory, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

    # Loop through files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Get the file extension
        file_extension = os.path.splitext(filename)[1].lower()

        # Find the appropriate category for the file
        moved = False
        for category, extensions in file_types.items():
            if file_extension in extensions:
                if nested:
                    # Create a nested folder for each file type
                    type_folder = os.path.join(directory, category, file_extension.lstrip('.').upper())
                    if not os.path.exists(type_folder):
                        os.makedirs(type_folder)
                    shutil.move(file_path, os.path.join(type_folder, filename))
                else:
                    # Move file to the corresponding folder in single-level organization
                    shutil.move(file_path, os.path.join(directory, category, filename))
                moved = True
                break
        
        # If no category matches, move the file to 'Others'
        if not moved:
            if nested:
                # Create a nested folder for 'Others'
                others_folder = os.path.join(directory, 'Others', 'Others')
                if not os.path.exists(others_folder):
                    os.makedirs(others_folder)
                shutil.move(file_path, os.path.join(others_folder, filename))
            else:
                shutil.move(file_path, os.path.join(directory, 'Others', filename))
    
    print(f"Files have been organized in {directory}.")
