from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()
# Initialize the tool for internet searching capabilities

webCrawler = SerperDevTool(
	n_results=5
)

def search_websites(query: str):
    links = []
    
    results = webCrawler.run(search_query= query)
    

    for item in results['organic']:
            links.append(item['link'])

    return links


