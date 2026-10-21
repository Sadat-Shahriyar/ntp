import os
import re


direcotry_to_check = "rts_papers_output/pdfs"

def find_duplicate_pdfs(directory):
    """Find PDF files ending with (1).pdf, (2).pdf, (3).pdf, etc."""
    pattern = re.compile(r".*\(\d+\)\.pdf$", re.IGNORECASE)
    duplicates = []

    for filename in sorted(os.listdir(directory)):
        if pattern.match(filename):
            duplicates.append(os.path.join(directory, filename))

    return duplicates


if __name__ == "__main__":
    directory = direcotry_to_check

    duplicates = find_duplicate_pdfs(directory)

    if not duplicates:
        print("No duplicate PDF files found.")
    else:
        print(f"Found {len(duplicates)} duplicate PDF file(s):\n")
        for f in duplicates:
            print(f"  {f}")

        answer = input("\nDelete all? [y/N]: ").strip().lower()
        if answer == "y":
            for f in duplicates:
                os.remove(f)
                print(f"  Deleted: {f}")
            print("Done.")
        else:
            print("No files deleted.")
