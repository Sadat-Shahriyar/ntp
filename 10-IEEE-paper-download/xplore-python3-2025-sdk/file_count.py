import os
def count_papers_in_folder(folder_path):
    """Count the number of papers in the folder file."""
    total_papers = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            total_papers += 1
    print(f"Total papers in folder: {total_papers}")
    return total_papers

if __name__ == "__main__":
    json_path = '/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/10-IEEE-paper-download/xplore-python3-2025-sdk/rts_papers_output/pdfs'  # Update this path if needed
    count_papers_in_folder(json_path)