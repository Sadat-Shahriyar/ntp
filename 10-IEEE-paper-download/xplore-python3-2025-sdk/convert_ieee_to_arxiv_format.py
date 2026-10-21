import json
import os
from datetime import datetime


def extract_authors(authors_data):
    """Extract author names from IEEE format to simple list."""
    if not authors_data:
        return []
    authors_list = authors_data.get('authors', [])
    return [author.get('full_name', '') for author in authors_list if author.get('full_name')]


def extract_categories(index_terms):
    """Extract categories from IEEE index terms."""
    if not index_terms:
        return []

    categories = []

    # Get author terms (usually more specific/relevant)
    author_terms = index_terms.get('author_terms', {}).get('terms', [])
    categories.extend(author_terms)

    # Get IEEE terms
    ieee_terms = index_terms.get('ieee_terms', {}).get('terms', [])
    categories.extend(ieee_terms)

    return categories


def format_publication_date(paper):
    """Extract and format publication date."""
    # Try publication_year first
    year = paper.get('publication_year')
    if year:
        return str(year)

    # Try publication_date
    pub_date = paper.get('publication_date', '')
    if pub_date:
        return pub_date

    return None


def convert_ieee_to_arxiv_format(input_json_path, output_json_path=None, query_description=None):
    """
    Convert IEEE Xplore JSON format to arXiv-style format.
    Only includes papers where downloaded=True.
    """
    # Read input JSON
    with open(input_json_path, 'r', encoding='utf-8') as f:
        ieee_papers = json.load(f)

    # Filter for downloaded papers only
    downloaded_papers = [p for p in ieee_papers if p.get('downloaded', False)]

    # Convert each paper
    converted_papers = []
    for paper in downloaded_papers:
        converted = {
            'ieee_doi': paper.get('doi'),
            'article_number': paper.get('article_number'),
            'title': paper.get('title', ''),
            'authors': extract_authors(paper.get('authors')),
            'published': format_publication_date(paper),
            'summary': paper.get('abstract', ''),
            'categories': extract_categories(paper.get('index_terms')),
            'pdf_path': paper.get('pdf_path'),
            'pdf_url': paper.get('pdf_url'),
            'publication_title': paper.get('publication_title'),
            'publisher': paper.get('publisher', 'IEEE')
        }
        converted_papers.append(converted)

    # Build output structure
    output = {
        'metadata': {
            'converted_at': datetime.now().isoformat(),
            'source_file': os.path.basename(input_json_path),
            'query': query_description or 'IEEE Xplore search',
            'source_format': 'IEEE Xplore',
            'target_format': 'arXiv-style'
        },
        'papers': converted_papers,
        'total_downloaded': len(converted_papers)
    }

    # Generate output path if not provided
    if output_json_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.dirname(input_json_path)
        output_json_path = os.path.join(output_dir, f'papers_converted_{timestamp}.json')

    # Write output
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Total papers in source: {len(ieee_papers)}")
    print(f"Downloaded papers converted: {len(converted_papers)}")
    print(f"Output saved to: {output_json_path}")

    return output_json_path


if __name__ == '__main__':
    input_path = 'rts_papers_output/papers_raw_20260213_113432.json'
    query = '(all:"schedulability analysis" OR all:schedulability OR all:"response time analysis" OR all:"response-time analysis") AND (all:"real-time system" OR all:"real-time systems" OR all:"real-time task")'

    convert_ieee_to_arxiv_format(input_path, query_description=query)
