import requests
import xml.etree.ElementTree as ET
from pymongo import MongoClient

def fetch_arxiv_papers(query, max_results=5, start_int = 0):
    # arXiv API endpoint
    url = 'http://export.arxiv.org/api/query'
    
    # Parameters for the search query
    params = {
        'search_query': query,
        'start': start_int,  # start from the first result
        'max_results': max_results,
        'sortBy': 'submittedDate',  # Sort by submission date
        'sortOrder': 'descending'   # Sort in descending order
    }
    
    # Make the request to the arXiv API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Error fetching data from arXiv!")
        return
    
    # Parse the XML response
    root = ET.fromstring(response.content)
    
    # Extracting paper details from the XML
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper = {}
        
        #Extring paper id
        id = entry.find('{http://www.w3.org/2005/Atom}id').text
        paper['id'] = id.split('/')[-1]
        
        # Extracting paper category
        category = entry.find('{http://www.w3.org/2005/Atom}category').attrib['term']
        paper['category'] = category
        
        # Extracting paper abstract
        abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text
        paper['abstract'] = abstract.strip()
        
        # Extracting paper links
        links = []
        for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
            links.append(link.attrib['href'])
        paper['links'] = links
        
        # Extracting paper version
        # Extracting paper title
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        paper['title'] = title.strip()
        
        # Extracting paper authors
        authors = []
        for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
            name = author.find('{http://www.w3.org/2005/Atom}name').text
            authors.append(name)
        paper['authors'] = authors
        
        # Extracting paper summary
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        paper['summary'] = summary.strip()
        
        # Extracting publication date
        published = entry.find('{http://www.w3.org/2005/Atom}published').text
        paper['published'] = published
        
        # Extracting the URL to the paper
        link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
        paper['link'] = link
        
        papers.append(paper)
    
    return papers

# Example usage
mongo_uri = "mongodb://datasci:scopus888@datascidb.kanakornmek.dev:27017/?authSource=admin"
client = MongoClient(mongo_uri)
db = client["datasci"]
collection = db["papers"]
"""subject_map = {
    "Agricultural": "AGRI" , "Arts": "ARTS", "Biochemistry": "BIOC",
    "Business": "BUSI", "Chemical Engineering": "CENG",
    "Chemistry": "CHEM", "Computer": "COMP", "Decision": "DECI", "Dentist": "DENT",
    "Planetary": "EART", "Economic": "ECON", "Energy": "ENER",
    "Engineering": "ENGI", "Environment": "ENVI", "Health": "HEAL",
    "Immunology": "IMMU", "Material science": "MATE", "Math": "MATH",
    "Medicine": "MEDI", "Neuroscience": "NEUR", "Nursing": "NURS",
    "Pharma": "PHAR", "Physic": "PHYS", "Psychology": "PSYC",
    "Social": "SOCI", "Veterinary": "VETE", "Multidisciplinary": "MULT"
}"""
"""queries = [
    "Agricultural", "Arts", "Biochemistry", "Business", "Chemical Engineering", "Chemistry", "Computer", 
    "Decision", "Dentist", "Planetary", "Economic",
    "Energy", "Engineering", "Environment", "Health", "Immunology",
    "Material science", "Math", "Medicine", "Neuroscience", "Nursing", "Pharma",
    "Physic", "Psychology", "Social", "Veterinary", "Multidisciplinary"
]"""


subject_map = {
    #"Agricultural": "AGRI" , "Biochemistry": "BIOC", "Business": "BUSI", 
    "Chemical Engineering": "CENG",
    "Chemistry": "CHEM", "Computer": "COMP", "Dentist": "DENT",
    "Planetary": "EART", "Energy": "ENER",
    "Engineering": "ENGI", "Environment": "ENVI",
    "Immunology": "IMMU", "Material science": "MATE", "Math": "MATH",
    "Neuroscience": "NEUR", 
    "Pharma": "PHAR", "Physic": "PHYS",
    "Social": "SOCI", "Veterinary": "VETE", "Multidisciplinary": "MULT"
}


queries = [
    #"Agricultural", "Biochemistry", "Business", 
    "Chemical Engineering", "Chemistry", "Computer", 
    "Dentist", "Planetary", 
    "Energy", "Engineering", "Environment", "Immunology",
    "Material science", "Math", "Neuroscience",  "Pharma",
    "Physic",  "Social", "Veterinary", "Multidisciplinary"
]

for query in queries:
    print(f"Processing {query}...")
    for i in range(40):
        print(f"Cycle {i+1}")
        papers = fetch_arxiv_papers(query, max_results=25, start_int=i*25)

        new_data = []
        if papers:
            for i, paper in enumerate(papers):
                data = {
                    'item': {'ait:process-info': {'ait:date-delivered': {'@timestamp': paper['published']}}},
                    'coredata': {'dc:description': paper['summary'], 'dc:title': paper['title'], 'dc:identifier': paper['id']},
                    'subject-areas': {'subject-area': [subject_map[query]]},
                    'authors': [author for author in paper['authors']],
                    'batches': 2
                }
                new_data.append(data)
            try:
                collection.insert_many(new_data, ordered=False)
            except Exception as e:
                print(f"Error inserting data into MongoDB")
        else:
            print(f"No papers found for {query}")

