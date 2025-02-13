from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()
Model = 'gpt-4'
api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model = Model,api_key=api_key)


site = 'https://www.geeksforgeeks.org/merge-sort/'
tool = ScrapeWebsiteTool(website_url=site)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ReferenceCrew():
	"""ReferenceCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['scraper'],
			tools=[tool],
			verbose=True,
			llm = llm
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def scraper_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape_task'],
			output_file = 'data.txt'
		)
		
	@crew
	def crew(self) -> Crew:
		"""Creates the ReferenceCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents,  # Automatically created by the @agent decorator
			tasks=self.tasks,  # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical,  # Alternative process mode
		)

