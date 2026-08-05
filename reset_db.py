import os
import glob

project_root = os.path.dirname(__file__)
db_files = glob.glob(os.path.join(project_root, "**", "*.db"), recursive=True)

if not db_files:
    print("No existing database files found (*.db).")
else:
    for db_path in db_files:
        try:
            os.remove(db_path)
            print(f"Successfully deleted existing database at: {db_path}")
        except Exception as e:
            print(f"Failed to delete database at {db_path}: {e}")
