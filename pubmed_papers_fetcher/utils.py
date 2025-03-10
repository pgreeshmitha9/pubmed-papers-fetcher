import re

def extract_company_names(affiliation):
    """
    Extract company names from author affiliations.
    Example: "Pfizer Inc, New York, USA" -> "Pfizer Inc"
    """
    company_keywords = [
        'Inc', 'Ltd', 'LLC', 'Corporation', 'Pharma', 'Biotech', 'Company'
    ]

    for keyword in company_keywords:
        if keyword.lower() in affiliation.lower():
            # Extract the part before the comma or full affiliation if no comma
            return affiliation.split(',')[0]
    return None


def extract_corresponding_author_email(article):
    """
    Extract the corresponding author's email from the article.
    """
    if 'elocationid' in article and 'email' in article['elocationid']:
        return article['elocationid']['email']

    # Alternatively, scan the entire text body for email patterns
    text_body = article.get('abstract', '')
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text_body)

    return emails[0] if emails else 'Not Available'
