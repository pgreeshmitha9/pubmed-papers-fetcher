import argparse
from pubmed_papers_fetcher.fetcher import PaperFetcher


def main():
    parser = argparse.ArgumentParser(description='Fetch PubMed papers based on a query.')
    parser.add_argument('--query', '-q', required=True, help='Search query for PubMed')
    parser.add_argument('--file', '-f', required=True, help='Output CSV file')
    parser.add_argument('--email', '-e', required=True, help='Your email address (required by PubMed API)')
    parser.add_argument('--api-key', '-k', required=True, help='Your PubMed API key')

    args = parser.parse_args()

    # Initialize PaperFetcher
    fetcher = PaperFetcher(query=args.query, email=args.email, api_key=args.api_key)

    # Fetch papers and save to CSV
    try:
        papers = fetcher.fetch_papers()
        fetcher.save_to_csv(papers, args.file)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()