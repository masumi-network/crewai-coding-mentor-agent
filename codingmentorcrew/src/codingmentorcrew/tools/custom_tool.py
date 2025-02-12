from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup

class WebScraperInput(BaseModel):
    """Input schema for Web scraper."""
    website_url: str = Field(..., description="URL of the website to be scraped.")

class WebScraperTool(BaseTool):
    name: str = "Web Scraper Tool"
    description: str = (
        "Scrapes website content to return HTML text."
    )
    args_schema: Type[BaseModel] = WebScraperInput

    def _run(self, website_url: str) -> str:

        website_url = website_url.strip('"')
        
        contenta = requests.get(website_url)

        soup = BeautifulSoup(contents.content, 'html5lib')

        return soup.prettify()
