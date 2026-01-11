import os

OUTPUT_FILE = "master_context.md"

def is_text_file(filepath):
    # Extensions to explicitly include
    valid_exts = ['.md', '.py', '.txt', '.ipynb', '.json', '.yaml', '.yml', '.html', '.css', '.js', '.sh', '.csv']
    ext = os.path.splitext(filepath)[1].lower()
    return ext in valid_exts or os.path.basename(filepath) in ['Dockerfile', 'Makefile']

def scaffold_directory(root_dir):
    print(f"Generating {OUTPUT_FILE} from contents of {os.path.abspath(root_dir)}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# Master Context for {os.path.basename(os.path.abspath(os.path.join(root_dir, '..')))}\n")
        outfile.write(f"Generated on {os.popen('date').read().strip()}\n\n")

        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude unwanted directories
            dirs_to_skip = ['.ipynb_checkpoints', '__pycache__', '.git', '.claude', 'node_modules', 'venv', 'env', 'site-packages']
            
            # Modify dirnames in-place to skip recursion
            dirnames[:] = [d for d in dirnames if d not in dirs_to_skip]
            
            for f in sorted(filenames):
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, root_dir)
                
                # Skip output file and hidden files/scripts
                if f == OUTPUT_FILE or f == "scaffold_context.py" or f.startswith('.'):
                    continue
                
                if f == "master_context.txt": # Skip the travel-agent style legacy file if present
                    continue

                # Check if text file
                if not is_text_file(full_path):
                    # print(f"Skipping non-text file: {rel_path}")
                    continue

                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        # Use XML-style tags for clear file delimitation, which works well for LLMs
                        outfile.write(f"\n<file_content path=\"{rel_path}\">\n")
                        outfile.write(content)
                        if not content.endswith('\n'):
                            outfile.write('\n')
                        outfile.write(f"</file_content>\n")
                        print(f"Added {rel_path}")
                except Exception as e:
                    print(f"Error reading {rel_path}: {e}")

    print(f"Done. Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    scaffold_directory(".")
