import json
import os
from datetime import datetime


def get_pdf_filename(title):
    """Create PDF filename from paper title: strip colons, replace spaces with underscores."""
    return title.replace(':', '').replace(',','').replace('/','_').replace(' ', '_').replace('"', '').replace("(", "").replace(")", "").replace("'", "").replace("?", "").replace("[", "").replace("]", "").replace("^","")   + '.pdf'


def check_downloaded_papers(json_path, pdf_dir):
    """Check if papers marked as downloaded actually exist in the pdf folder."""
    # Read the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    # Get list of existing PDFs in the folder
    existing_pdfs = set(os.listdir(pdf_dir)) if os.path.exists(pdf_dir) else set()

    updated_count = 0

    for paper in papers:
        title = paper.get('title', '')
        expected_filename = get_pdf_filename(title)

        if paper.get('downloaded', False):
            # Check if file exists
            if expected_filename in existing_pdfs:
                # Add the absolute PDF path
                paper['pdf_path'] = os.path.abspath(os.path.join(pdf_dir, expected_filename))
            else:
                paper['downloaded'] = False
                paper['pdf_path'] = None
                updated_count += 1
                print(f"Missing: {expected_filename}")
        else:
            # For non-downloaded papers, check if file happens to exist
            if expected_filename in existing_pdfs:
                paper['pdf_path'] = os.path.abspath(os.path.join(pdf_dir, expected_filename))
            else:
                paper['pdf_path'] = None

    # Generate new filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.dirname(json_path)
    output_filename = f"papers_raw_{timestamp}.json"
    output_path = os.path.join(output_dir, output_filename)

    # Save the updated JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=4, ensure_ascii=False)

    print(f"\nTotal papers in JSON: {len(papers)}")
    print(f"Total PDFs in folder: {len(existing_pdfs)}")
    print(f"Updated (set downloaded=False): {updated_count}")
    print(f"Saved to: {output_path}")

    return output_path


if __name__ == '__main__':
    json_path = 'rts_papers_output/papers_raw_20260212_132745.json'
    pdf_dir = 'rts_papers_output/pdfs'

    check_downloaded_papers(json_path, pdf_dir)
