import requests
import csv
import time
from pubmed_papers_fetcher.utils import extract_company_names, extract_corresponding_author_email

class PaperFetcher:
    def __init__(self, query, email, api_key):
        self.query = query
        self.email = email
        self.api_key = api_key
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def fetch_papers(self):
        # Step 1: Search for papers
        search_url = f"{self.base_url}esearch.fcgi?db=pubmed&term={self.query}&retmax=100&usehistory=y&email={self.email}&api_key={self.api_key}&retmode=json"
        response = requests.get(search_url)
        response.raise_for_status()

        # Extract WebEnv and QueryKey
        data = response.json()
        pmids = data['esearchresult']['idlist']

        print(f"✅ Found {len(pmids)} papers... Fetching details now...")

        # Step 2: Fetch paper details in JSON
        papers = []
        for pmid in pmids:
            fetch_url = f"{self.base_url}esummary.fcgi?db=pubmed&id={pmid}&retmode=json&email={self.email}&api_key={self.api_key}"
            response = requests.get(fetch_url)
            response.raise_for_status()

            try:
                article = response.json()['result'][pmid]
                title = article.get('title', 'N/A')
                pub_date = article.get('pubdate', 'N/A')
                authors = article.get('authors', [])

                non_academic_authors = []
                company_affiliations = []

                # Extract author details
                for author in authors:
                    affiliation = author.get('affiliationinfo', [{}])[0].get('affiliation', '')
                    company_name = extract_company_names(affiliation)

                    # ✅ New logic: Capture ALL authors (even if no company affiliation)
                    non_academic_authors.append(author['name'])
                    if company_name:
                        company_affiliations.append(company_name)

                corresponding_email = extract_corresponding_author_email(article)

                # ✅ Always save the paper (even if no company affiliation)
                papers.append([
                    pmid,
                    title,
                    pub_date,
                    ", ".join(non_academic_authors) if non_academic_authors else "Not Available",
                    ", ".join(company_affiliations) if company_affiliations else "Not Available",
                    corresponding_email or "Not Available"
                ])
            except Exception as e:
                print(f"❌ Failed to fetch paper {pmid}: {e}")
                continue

            # Avoid rate-limiting
            time.sleep(0.3)

        print(f"✅ Successfully fetched {len(papers)} papers.")
        return papers

    def save_to_csv(self, papers, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['PubmedID', 'Title', 'Publication Date', 'Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'])
            writer
