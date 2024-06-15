import requests
from bs4 import BeautifulSoup
import pyperclip


def fetch_additional_details(link, headers):
    try:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Assuming 'gsc_oci_title_ggi' contains the PDF link
            pdf_link_element = soup.find("div", class_="gsc_oci_title_ggi").find("a")
            if pdf_link_element and 'href' in pdf_link_element.attrs:
                return pdf_link_element['href']
        return "No PDF link found"
    except Exception as e:
        print(f"Failed to fetch details from {link}: {e}")
        return "Failed to fetch PDF link"

def scrape_scholar(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    publications = []
    
    for row in soup.find_all("tr", class_="gsc_a_tr"):
        try:
            title = row.find("a", class_="gsc_a_at").text
            authors = row.find("div", class_="gs_gray").text
            venue_year = row.find_all("div", class_="gs_gray")[1].text
            year = venue_year.split(',')[-1].strip()
            venue = venue_year.rsplit(',', 1)[0].strip() if ',' in venue_year else venue_year
            link_page = "https://scholar.google.com" + row.find("a", class_="gsc_a_at")['href']
            
            # Fetch additional details from the link page
            pdf_link = fetch_additional_details(link_page, headers)
            
            # Format the publication info
            publication_info = f"_{title}_<br> \n {authors}<br>\n{venue}, {year}<br>\n"
            if pdf_link != "PDF link not found":
                publication_info += f"[PDF]({pdf_link})<a href='{pdf_link}'>PDF</a>\n"
            else:
                publication_info += "PDF link not found"

            publications.append(publication_info)
        except Exception as e:
            print(f"Failed to process one entry: {e}")
    # Copy all publications info to clipboard
    # pyperclip.copy(publications)
    # print("Copied to clipboard")
    return publications


# Example usage:
url = "https://scholar.google.com/citations?user=uOIgTt8AAAAJ&hl=en"
publications = scrape_scholar(url)
for pub in publications:
    print(pub)
