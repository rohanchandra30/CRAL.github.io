import bibtexparser

def parse_bibtex_file(filename):
    with open(filename, 'r') as bibtex_file:
        bibtex_str = bibtex_file.read()
    print('hi')
    bib_database = bibtexparser.loads(bibtex_str)
    publications = []
    
    for entry in bib_database.entries:
        try:
            title = entry.get('title', 'No title available')
            authors = entry.get('author', 'No authors listed').replace(" and ", ", ")
            venue = entry.get('journal', 'No venue available')
            year = entry.get('year', 'No year available')
            
            # Formatting the output
            publication_info = f"{title}\n{authors}\n{venue}, {year}"
            publications.append(publication_info)
        except Exception as e:
            print(f"Failed to process one entry: {e}")
    
    return publications

# Example usage:
filename = "bibtex.bib"
publications = parse_bibtex_file(filename)
print(len(publications))
for pub in publications:
    print(pub)
