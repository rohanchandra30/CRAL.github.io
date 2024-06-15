import bibtexparser
import pyperclip

def reformat_authors(authors_str):
    authors = authors_str.split(" and ")
    formatted_authors = []
    for author in authors:
        parts = author.split(", ")
        if len(parts) > 1:
            formatted_name = f"{parts[1]} {parts[0]}"
        else:
            formatted_name = parts[0]  # Handle cases with no comma
        formatted_authors.append(formatted_name)
    return ", ".join(formatted_authors)

def parse_bibtex_file(filename):
    with open(filename, 'r') as bibtex_file:
        bibtex_str = bibtex_file.read()
    
    bib_database = bibtexparser.loads(bibtex_str)
    publications = []  # Use a list to store entries for sorting
    print(len(bib_database.entries))
    for entry in bib_database.entries:
        try:
            title = entry.get('title', 'No title available')
            raw_authors = entry.get('author', 'No authors listed')
            authors = reformat_authors(raw_authors)
            # Check for 'journal' or 'booktitle', whichever is available
            if 'journal' in entry:
                venue = entry['journal']
            elif 'booktitle' in entry:
                venue = entry['booktitle']
            else:
                venue = 'No venue available'
            year = entry.get('year', 'No year available')
            
            # Only add entries with a valid year
            if year and year.isdigit() and venue != 'No venue available':
                publications.append({
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'year': year
                })
        except Exception as e:
            print(f"Failed to process one entry: {e}")
    
    # Sort publications by year
    publications.sort(key=lambda x: x['year'], reverse=True)
    # Format sorted publications for output
    all_publications_info = ""
    last_year = None  # Track the last year for heading insertion
    for pub in publications:
        if pub['year'] != last_year:
            if last_year is not None:  # Add spacing between different years, if not the first
                all_publications_info += "\n"
            all_publications_info += f"<h4>{pub['year']}</h4>\n"
            last_year = pub['year']
        publication_info = f"_{pub['title']}_<br>\n{pub['authors']}<br>\n{pub['venue']}, {pub['year']}<br>\n [PDF]()\n" + "\n"
        all_publications_info += publication_info

    # Copy all publications info to clipboard
    pyperclip.copy(all_publications_info)
    print("Copied to clipboard")
    return all_publications_info

# Example usage:
filename = "bibtex.bib"
publications_info = parse_bibtex_file(filename)
# print(publications_info)  # Optional: print to console as well
