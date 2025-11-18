"""
Utility functions for the application
"""

import os
import shutil

def clear_directory(directory):
    """Clear all files in a directory"""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def ensure_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def get_file_count(directory, extensions=('.jpg', '.jpeg', '.png')):
    """Count files with specific extensions in a directory"""
    if not os.path.exists(directory):
        return 0
    
    count = 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(extensions):
            count += 1
    return count

