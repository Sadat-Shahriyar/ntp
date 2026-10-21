#!/usr/bin/env python3
"""
Download real-time systems schedulability analysis papers from IEEE Xplore.
Conferences: RTSS, RTAS, ECRTS, EMSOFT, and related venues.
"""

import sys
import os
import json
import time
import csv
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the xploreapi module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'xploreapi'))
from xploreapi import XPLORE

# ============== CONFIGURATION ==============
API_KEY = os.getenv("IEEE_API_KEY")  # Loaded from .env file
AUTH_TOKEN = os.getenv("IEEE_AUTH_TOKEN")  # Institutional auth token for full text access

# Output directory for results
OUTPUT_DIR = "rts_papers_output"

# Schedulability analysis search query (adapted from your arXiv query)
SEARCH_QUERY = (
    '("schedulability analysis" OR "schedulability" OR '
    '"response time analysis" OR "response-time analysis") '
    'AND ("real-time system" OR "real-time systems" OR "real-time task" OR '
    '"real-time scheduling" OR "worst-case execution time")'
)

# Real-time systems conferences to search
# Format: (search_term, friendly_name)
CONFERENCES = [
    ("Real-Time Systems Symposium", "RTSS"),
    ("Real-Time and Embedded Technology and Applications Symposium", "RTAS"),
    ("Euromicro Conference on Real-Time Systems", "ECRTS"),
    ("Embedded Software", "EMSOFT"),  # EMSOFT often appears this way
    ("Real-Time Computing Systems and Applications", "RTCSA"),
    ("Real-Time Networks and Systems", "RTNS"),
    ("Robotics: Science and Systems", "RSS"),
    ("Intelligent Robots and Systems", "IROS"),
    # ("Design Automation Conference", "DAC"),
    # ("Design, Automation and Test in Europe", "DATE"),
]

# Rate limiting: seconds between API calls
RATE_LIMIT_DELAY = 1.0

# Maximum results per API call (IEEE limit is 25)
MAX_RESULTS_PER_CALL = 25

# Maximum API calls per day (IEEE limit is 200)
MAX_API_CALLS_PER_DAY = 200

# Enable PDF downloads (set to True to download PDFs)
DOWNLOAD_PDFS = True

# PDF output directory
PDF_DIR = "rts_papers_output/pdfs"

# Global counter for API calls
api_call_count = 0

# ============================================


def create_xplore_instance():
    """Create a fresh XPLORE instance."""
    api = XPLORE(API_KEY)
    api.dataFormat('object')  # Return as Python dict
    api.dataType('json')
    return api


def check_api_limit():
    """Check if we've hit the daily API call limit."""
    global api_call_count
    if api_call_count >= MAX_API_CALLS_PER_DAY:
        print(f"\n  WARNING: Reached daily API limit ({MAX_API_CALLS_PER_DAY} calls)")
        print("  Results so far will be saved. Run again tomorrow for more.")
        return False
    return True


def increment_api_count():
    """Increment and display API call counter."""
    global api_call_count
    api_call_count += 1
    remaining = MAX_API_CALLS_PER_DAY - api_call_count
    if api_call_count % 10 == 0:  # Show every 10 calls
        print(f"  [API calls used: {api_call_count}/{MAX_API_CALLS_PER_DAY}, remaining: {remaining}]")


def search_conference(conference_title, conference_name, search_query):
    """
    Search for papers in a specific conference matching the query.
    Handles pagination to get all results.
    """
    all_papers = []
    start_record = 1
    total_records = None

    print(f"\n{'='*60}")
    print(f"Searching: {conference_name} ({conference_title})")
    print(f"{'='*60}")

    while True:
        # Check API limit before making call
        if not check_api_limit():
            break

        # Create fresh instance for each request (API state resets)
        api = create_xplore_instance()

        # Set search parameters
        api.maximumResults(MAX_RESULTS_PER_CALL)
        api.startingResult(start_record)
        api.resultsSorting('publication_year', 'desc')

        # Build the combined query: conference + schedulability terms
        combined_query = f'("{conference_title}") AND {search_query}'
        api.booleanText(combined_query)

        # Execute query
        try:
            result = api.callAPI()
            increment_api_count()
        except Exception as e:
            print(f"  Error querying API: {e}")
            break

        # Check for errors
        if isinstance(result, str):
            print(f"  API returned string (possible error): {result[:200]}")
            break

        if 'error' in result:
            print(f"  API Error: {result.get('error')}")
            break

        # Get total records on first call
        if total_records is None:
            total_records = result.get('total_records', 0)
            print(f"  Total papers found: {total_records}")

        # Extract articles
        articles = result.get('articles', [])
        if not articles:
            break

        all_papers.extend(articles)
        print(f"  Fetched {len(all_papers)}/{total_records} papers...")

        # Check if we have all records
        if len(all_papers) >= total_records:
            break

        # Move to next page
        start_record += MAX_RESULTS_PER_CALL

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    return all_papers


def search_general_query(search_query):
    """
    Search for papers matching the query without conference filter.
    This catches papers from other venues.
    """
    all_papers = []
    start_record = 1
    total_records = None

    print(f"\n{'='*60}")
    print(f"Searching: General Real-Time Systems (no conference filter)")
    print(f"{'='*60}")

    while True:
        # Check API limit before making call
        if not check_api_limit():
            break

        api = create_xplore_instance()
        api.maximumResults(MAX_RESULTS_PER_CALL)
        api.startingResult(start_record)
        api.resultsSorting('publication_year', 'desc')

        # Filter to conference papers only
        api.resultsFilter('content_type', 'Conferences')
        api.booleanText(search_query)

        try:
            result = api.callAPI()
            increment_api_count()
        except Exception as e:
            print(f"  Error querying API: {e}")
            break

        if isinstance(result, str):
            print(f"  API returned string: {result[:200]}")
            break

        if 'error' in result:
            print(f"  API Error: {result.get('error')}")
            break

        if total_records is None:
            total_records = result.get('total_records', 0)
            print(f"  Total papers found: {total_records}")

        articles = result.get('articles', [])
        if not articles:
            break

        all_papers.extend(articles)
        print(f"  Fetched {len(all_papers)}/{total_records} papers...")

        if len(all_papers) >= total_records:
            break

        start_record += MAX_RESULTS_PER_CALL
        time.sleep(RATE_LIMIT_DELAY)

        # Safety limit: stop after 2000 papers for general search
        if len(all_papers) >= 2000:
            print("  Reached 2000 paper limit for general search")
            break

    return all_papers


def extract_paper_info(paper):
    """Extract relevant fields from a paper record."""
    authors = paper.get('authors', {}).get('authors', [])
    author_names = [a.get('full_name', '') for a in authors]

    return {
        'title': paper.get('title', ''),
        'authors': '; '.join(author_names),
        'abstract': paper.get('abstract', ''),
        'publication_title': paper.get('publication_title', ''),
        'publication_year': paper.get('publication_year', ''),
        'article_number': paper.get('article_number', ''),
        'doi': paper.get('doi', ''),
        'pdf_url': paper.get('pdf_url', ''),
        'html_url': paper.get('html_url', ''),
        'start_page': paper.get('start_page', ''),
        'end_page': paper.get('end_page', ''),
        'citing_paper_count': paper.get('citing_paper_count', 0),
        'is_open_access': paper.get('is_open_access', False),
        'index_terms': json.dumps(paper.get('index_terms', {})),
    }


def save_results(papers, output_dir):
    """Save papers to JSON and CSV files."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save raw JSON
    json_path = os.path.join(output_dir, f'papers_raw_{timestamp}.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    print(f"\nSaved raw JSON: {json_path}")

    # Extract and save as CSV
    extracted = [extract_paper_info(p) for p in papers]
    csv_path = os.path.join(output_dir, f'papers_{timestamp}.csv')

    if extracted:
        fieldnames = extracted[0].keys()
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(extracted)
        print(f"Saved CSV: {csv_path}")

    # Save summary
    summary_path = os.path.join(output_dir, f'summary_{timestamp}.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"IEEE Xplore Paper Download Summary\n")
        f.write(f"{'='*50}\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        f.write(f"Total papers: {len(papers)}\n")
        f.write(f"Search query: {SEARCH_QUERY}\n\n")

        # Count by publication
        pub_counts = {}
        for p in papers:
            pub = p.get('publication_title', 'Unknown')
            pub_counts[pub] = pub_counts.get(pub, 0) + 1

        f.write("Papers by publication:\n")
        for pub, count in sorted(pub_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {count:4d} - {pub}\n")

    print(f"Saved summary: {summary_path}")

    return json_path, csv_path


def deduplicate_papers(papers):
    """Remove duplicate papers based on article_number or DOI."""
    seen = set()
    unique = []

    for paper in papers:
        # Use article_number as primary key, DOI as fallback
        key = paper.get('article_number') or paper.get('doi') or paper.get('title')
        if key and key not in seen:
            seen.add(key)
            unique.append(paper)

    return unique


def sanitize_filename(title):
    """Create a safe filename from paper title."""
    # Remove special characters, keep alphanumeric and spaces
    safe = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    safe = re.sub(r'\s+', '_', safe)
    # Truncate to reasonable length
    return safe[:100]


def download_open_access_pdf(article_number, output_path):
    """
    Download PDF using IEEE Open Access API endpoint.
    Returns True if successful, False otherwise.
    """
    global api_call_count

    if not check_api_limit():
        return False

    try:
        api = create_xplore_instance()
        api.openAccess(str(article_number))
        result = api.callAPI()
        increment_api_count()

        # Check if we got actual content
        if isinstance(result, dict):
            # API returns metadata, not the PDF directly
            # Check for full text content
            if 'full_text' in result or 'content' in result:
                content = result.get('full_text') or result.get('content', '')
                if content:
                    with open(output_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True
        return False
    except Exception as e:
        print(f"    Open access download failed: {e}")
        return False


def download_with_institutional_access(article_number, output_path):
    """
    Download full text using institutional auth token.
    Returns True if successful, False otherwise.
    """
    global api_call_count

    if not AUTH_TOKEN:
        return False

    if not check_api_limit():
        return False

    try:
        api = create_xplore_instance()
        api.setAuthToken(AUTH_TOKEN)
        api.fullTextRequest(str(article_number))
        result = api.callAPI()
        increment_api_count()

        # Check if we got actual content
        if isinstance(result, dict):
            # Check for error response
            if 'error' in result:
                print(f"    Institutional access error: {result.get('error')}")
                return False

            # Check for full text content
            content = None
            if 'full_text' in result:
                content = result.get('full_text')
            elif 'content' in result:
                content = result.get('content')
            elif 'xml_content' in result:
                content = result.get('xml_content')

            if content:
                # Save as text file (API returns text/XML, not PDF)
                txt_path = output_path.replace('.pdf', '.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    if isinstance(content, dict):
                        f.write(json.dumps(content, indent=2))
                    else:
                        f.write(str(content))
                return True

        # If result is a string (raw response), save it
        elif isinstance(result, str) and len(result) > 100:
            txt_path = output_path.replace('.pdf', '.txt')
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(result)
            return True

        return False
    except Exception as e:
        print(f"    Institutional download failed: {e}")
        return False


def download_pdf_direct(pdf_url, output_path):
    """
    Try to download PDF directly from URL.
    This may work for truly open access papers.
    Returns True if successful, False otherwise.
    """
    if not pdf_url:
        return False

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(pdf_url, headers=headers, timeout=30, stream=True)

        # Check if we got a PDF
        content_type = response.headers.get('content-type', '')
        if response.status_code == 200 and 'pdf' in content_type.lower():
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"    Direct download failed: {e}")
        return False


def download_papers(papers, pdf_dir):
    """
    Download PDFs for all papers.
    Tries open access API first, then direct download.
    """
    os.makedirs(pdf_dir, exist_ok=True)

    total = len(papers)
    downloaded = 0
    failed = 0
    skipped = 0

    print(f"\n{'='*60}")
    print(f"Downloading PDFs for {total} papers...")
    print(f"{'='*60}")

    download_log = []

    for i, paper in enumerate(papers, 1):
        article_number = paper.get('article_number', '')
        title = paper.get('title', f'paper_{article_number}')
        pdf_url = paper.get('pdf_url', '')
        is_open_access = paper.get('is_open_access', False)
        year = paper.get('publication_year', 'unknown')

        # Create filename
        safe_title = sanitize_filename(title)
        filename = f"{year}_{article_number}_{safe_title}.pdf"
        output_path = os.path.join(pdf_dir, filename)

        # Skip if already downloaded (check both .pdf and .txt)
        txt_path = output_path.replace('.pdf', '.txt')
        if os.path.exists(output_path) or os.path.exists(txt_path):
            print(f"  [{i}/{total}] Skipped (exists): {title[:50]}...")
            skipped += 1
            download_log.append({
                'article_number': article_number,
                'title': title,
                'status': 'skipped',
                'file': filename
            })
            continue

        print(f"  [{i}/{total}] Downloading: {title[:50]}...")

        success = False
        download_method = None

        # Try open access API first for open access papers
        if is_open_access and article_number:
            success = download_open_access_pdf(article_number, output_path)
            if success:
                download_method = 'open_access_api'
                print(f"    Downloaded via Open Access API")

        # Try institutional access if auth token is available
        if not success and AUTH_TOKEN and article_number:
            success = download_with_institutional_access(article_number, output_path)
            if success:
                download_method = 'institutional_access'
                print(f"    Downloaded via Institutional Access")

        # Try direct PDF download
        if not success and pdf_url:
            success = download_pdf_direct(pdf_url, output_path)
            if success:
                download_method = 'direct_url'
                print(f"    Downloaded via direct URL")

        if success:
            downloaded += 1
            download_log.append({
                'article_number': article_number,
                'title': title,
                'status': 'downloaded',
                'method': download_method,
                'file': filename
            })
        else:
            failed += 1
            download_log.append({
                'article_number': article_number,
                'title': title,
                'status': 'failed',
                'pdf_url': pdf_url,
                'is_open_access': is_open_access
            })
            print(f"    Failed - URL: {pdf_url or 'N/A'}")

        # Rate limiting between downloads
        time.sleep(0.5)

    # Save download log
    log_path = os.path.join(pdf_dir, 'download_log.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(download_log, f, indent=2)

    print(f"\nDownload Summary:")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped (already exists): {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Log saved to: {log_path}")

    return downloaded, skipped, failed


def main():
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Please set your IEEE API key in the .env file!")
        print("Edit the .env file and set: IEEE_API_KEY=your_actual_key")
        print("Get your API key from: https://developer.ieee.org/")
        sys.exit(1)

    print("="*60)
    print("IEEE Xplore Real-Time Systems Paper Downloader")
    print("="*60)
    print(f"API limits: {MAX_API_CALLS_PER_DAY} calls/day, {MAX_RESULTS_PER_CALL} records/call")
    print(f"Institutional access: {'Enabled' if AUTH_TOKEN else 'Disabled (no auth token)'}")
    print(f"Search query: {SEARCH_QUERY[:80]}...")
    print(f"Conferences: {', '.join([c[1] for c in CONFERENCES])}")

    all_papers = []

    # Search each conference
    for conf_title, conf_name in CONFERENCES:
        if not check_api_limit():
            break
        papers = search_conference(conf_title, conf_name, SEARCH_QUERY)
        all_papers.extend(papers)
        time.sleep(RATE_LIMIT_DELAY)

    # Also do a general search to catch papers from other venues
    if check_api_limit():
        general_papers = search_general_query(SEARCH_QUERY)
        all_papers.extend(general_papers)

    # Deduplicate
    print(f"\n{'='*60}")
    print(f"Total papers before deduplication: {len(all_papers)}")
    unique_papers = deduplicate_papers(all_papers)
    print(f"Total papers after deduplication: {len(unique_papers)}")

    # Save results
    if unique_papers:
        save_results(unique_papers, OUTPUT_DIR)

        # Print some statistics
        years = [p.get('publication_year') for p in unique_papers if p.get('publication_year')]
        if years:
            print(f"\nYear range: {min(years)} - {max(years)}")

        open_access = sum(1 for p in unique_papers if p.get('is_open_access'))
        print(f"Open access papers: {open_access}/{len(unique_papers)}")

        # Download PDFs if enabled
        if DOWNLOAD_PDFS:
            download_papers(unique_papers, PDF_DIR)
    else:
        print("\nNo papers found!")

    # API usage summary
    print(f"\nAPI calls used: {api_call_count}/{MAX_API_CALLS_PER_DAY}")
    print(f"Remaining calls today: {MAX_API_CALLS_PER_DAY - api_call_count}")
    print("\nDone!")


if __name__ == "__main__":
    main()
