import os

OUTPUT_FILE = "master_context.md"

# Specific paths to include
TARGET_PATHS = [
    "src/project",
    "Udaplay_01_solution_project.ipynb",
    "Udaplay_02_solution_project.ipynb"
]

def is_text_file(filepath):
    # Extensions to explicitly include
    valid_exts = ['.md', '.py', '.txt', '.ipynb', '.json', '.yaml', '.yml', '.html', '.css', '.js', '.sh', '.csv']
    ext = os.path.splitext(filepath)[1].lower()
    return ext in valid_exts or os.path.basename(filepath) in ['Dockerfile', 'Makefile']

def process_file(outfile, full_path, root_dir):
    rel_path = os.path.relpath(full_path, root_dir)
    
    if os.path.basename(full_path) == OUTPUT_FILE or os.path.basename(full_path).startswith('.') or os.path.basename(full_path) == "generate_custom_context.py":
        return

    if not is_text_file(full_path):
        return

    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as infile:
            content = infile.read()
            outfile.write(f"\n<file_content path=\"{rel_path}\">\n")
            outfile.write(content)
            if not content.endswith('\n'):
                outfile.write('\n')
            outfile.write(f"</file_content>\n")
            print(f"Added {rel_path}")
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")

def main():
    root_dir = os.path.abspath(".")
    print(f"Generating {OUTPUT_FILE} from specific targets in {root_dir}...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# Master Context for specific files in {os.path.basename(root_dir)}\n")
        outfile.write(f"Generated on {os.popen('date').read().strip()}\n\n")

        for target in TARGET_PATHS:
            abs_target = os.path.abspath(target)
            
            if not os.path.exists(abs_target):
                print(f"Warning: {target} does not exist. Skipping.")
                continue

            if os.path.isfile(abs_target):
                process_file(outfile, abs_target, root_dir)
            elif os.path.isdir(abs_target):
                for dirpath, dirnames, filenames in os.walk(abs_target):
                    # Exclude unwanted directories
                    dirs_to_skip = ['.ipynb_checkpoints', '__pycache__', '.git', '.claude', 'node_modules', 'venv', 'env', 'site-packages']
                    dirnames[:] = [d for d in dirnames if d not in dirs_to_skip]
                    
                    for f in sorted(filenames):
                        process_file(outfile, os.path.join(dirpath, f), root_dir)

    print(f"Done. Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
