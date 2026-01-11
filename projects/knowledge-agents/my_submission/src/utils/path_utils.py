"""
Path utilities for robust database path resolution
"""
import os


def find_project_root():
    """Find the project root directory by looking for key files"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for data directory and key project files
    while current_dir != '/':
        if (os.path.exists(os.path.join(current_dir, 'data', 'core', 'udahub.db')) and 
            os.path.exists(os.path.join(current_dir, 'data', 'external', 'cultpass.db'))):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # Fallback to relative path from current file location
    return os.path.dirname(__file__)


def get_core_db_path():
    """Get the absolute path to the core database"""
    project_root = find_project_root()
    return os.path.abspath(os.path.join(project_root, 'data', 'core', 'udahub.db'))


def get_external_db_path():
    """Get the absolute path to the external database"""
    project_root = find_project_root()
    return os.path.abspath(os.path.join(project_root, 'data', 'external', 'cultpass.db'))