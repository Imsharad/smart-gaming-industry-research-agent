
import os

# Define the root directory
ROOT_DIR = "/Users/sharad/Projects/udacity-reviews-hq/projects"
OUTPUT_FILE = os.path.join(ROOT_DIR, "master_of_master_context.md")

# List of files to concatenate
# Using relative paths for clarity, joining with ROOT_DIR
FILES_TO_APPEND = [
    # building-agents
    "building-agents/my_submission/master_context.md",
    
    # energy-advisor
    "energy-advisor/my_submission/master_context.md",
    
    # finance-agent-fintool
    "finance-agent-fintool/master_context.md",
    
    # knowledge-agents
    "knowledge-agents/my_submission/master_context.md",
    
    # swift-agent (including both found locations for completeness, or just the one in root if they are duplicates)
    # Checking file list, one is in root, one in my_submission. Usually my_submission is the generated one. 
    # Let's use the one in my_submission as primary if it exists.
    "swift-agent/my_submission/master_context.md",
    
    # travel-agent (Text file content provided by user, assuming it's saved or accessible. 
    # Since I cannot 'read' the user's previous message directly in this script without it being a file,
    # I will assume the user wants me to concatenate existing files. 
    # Wait, the user provided the CONTENT of travel-agent/my_submission/master_context.txt in the chat.
    # I should probably write that content to a temporary file or just include the path if it actually exists on disk.
    # The glob search didn't find it as a .md file. It might be a .txt or just missing.
    # Let's check if the file exists. If not, I'll note it.)
    "travel-agent/my_submission/master_context.txt",

    # udaci-model-optimization
    "udaci-model-optimization/project_instructions.md",
    "udaci-model-optimization/README.md",
    # Notebooks are complex to just "append" as raw JSON. 
    # Ideally they should be converted to Markdown or just referenced.
    # For this script, we will simply append their raw content as requested.
    "udaci-model-optimization/project/my_submission/final_notebooks/01_baseline_colab_pro.ipynb",
    "udaci-model-optimization/project/my_submission/final_notebooks/02_Compression_Colab_Pro.ipynb",
    "udaci-model-optimization/project/my_submission/final_notebooks/03_Pipeline_Final.ipynb",
    "udaci-model-optimization/project/my_submission/final_notebooks/04_Deployment_Complete_Colab_Pro.ipynb",

    # betty-bird-boutique
    "betty-bird-boutique/README.md"
]

def create_master_context():
    print(f"Creating master context file at: {OUTPUT_FILE}")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # Add a header
        outfile.write("# Master of Master Context\n\n")
        outfile.write("This file contains concatenated context from all Udacity projects.\n\n")
        
        for relative_path in FILES_TO_APPEND:
            full_path = os.path.join(ROOT_DIR, relative_path)
            
            print(f"Processing: {relative_path}")
            
            if os.path.exists(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as infile:
                        content = infile.read()
                        
                        # Add a separator and file title
                        outfile.write(f"\n\n{'='*80}\n")
                        outfile.write(f"START OF FILE: {relative_path}\n")
                        outfile.write(f"{ '='*80}\n\n")
                        
                        outfile.write(content)
                        
                        outfile.write(f"\n\n{'='*80}\n")
                        outfile.write(f"END OF FILE: {relative_path}\n")
                        outfile.write(f"{ '='*80}\n\n")
                        
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")
                    outfile.write(f"\n\n[ERROR READING FILE {relative_path}: {e}]\n\n")
            else:
                print(f"Warning: File not found: {full_path}")
                outfile.write(f"\n\n[FILE NOT FOUND: {relative_path}]\n\n")

    print("Done.")

if __name__ == "__main__":
    create_master_context()
