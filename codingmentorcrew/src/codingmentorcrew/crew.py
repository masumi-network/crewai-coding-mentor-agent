from crewai import Crew, Process, Agent, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai_tools import FileWriterTool
import os
from crewai_tools import FileWriterTool

load_dotenv()
Model = 'gpt-4o'
api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model = Model,api_key=api_key)

crawlTool = SerperDevTool(
	n_results=2
)

file_writer = FileWriterTool()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Codingmentorcrew():
	"""ReferenceCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def retriever(self) -> Agent:
		return Agent(
			config=self.agents_config['retriever'],
			verbose=True,
			llm = llm
		)
	@agent
	def scraper(self) -> Agent:
		return Agent(
			config=self.agents_config['scraper'],
			tools=[ScrapeWebsiteTool()],
			verbose=True,
			llm = llm
		)
	@agent
	def scraper2(self) -> Agent:
		return Agent(
			config=self.agents_config['scraper2'],
			tools=[ScrapeWebsiteTool()],
			verbose=True,
			llm = llm
		)

	@agent
	def scraper3(self) -> Agent:
		return Agent(
			config=self.agents_config['scraper3'],
			tools=[ScrapeWebsiteTool()],
			verbose=True,
			llm = llm
		)

	@agent
	def scraper4(self) -> Agent:
		return Agent(
			config=self.agents_config['scraper4'],
			tools=[ScrapeWebsiteTool()],
			verbose=True,
			llm = llm
		)

	@agent
	def scraper5(self) -> Agent:
		return Agent(
			config=self.agents_config['scraper5'],
			tools=[ScrapeWebsiteTool()],
			verbose=True,
			llm = llm
		)
	@agent
	def mentor(self) -> Agent:
		return Agent(
			config=self.agents_config['mentor'],
			verbose = True,
			llm = llm
		)
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	@task
	def retriever_task(self) -> Task:
		return Task(
			config=self.tasks_config['retriever_task'],
			agent = self.retriever(),
			output_key="retrieved_url"
		)
	
	@task
	def scraper_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape_task'],
			output_file = 'data.txt',
			agent=self.scraper(),
			depends_on=[self.retriever_task()],
			inputs={"website_url": "{{retriever_task.retrieved_url}}"},
			output_key="scraped_data_1"
		)

	@task
	def scraper2_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape2_task'],
			output_file = 'data.txt',
			agent=self.scraper2(),
			depends_on=[self.retriever_task()],
			inputs={"website_url": "{{retriever_task.retrieved_url}}"},
			output_key="scraped_data_2"
		)

	@task
	def scraper3_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape3_task'],
			output_file = 'data.txt',
			agent=self.scraper3(),
			depends_on=[self.retriever_task()],
			inputs={"website_url": "{{retriever_task.retrieved_url}}"},
			output_key="scraped_data_3"
		)

	@task
	def scraper4_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape4_task'],
			output_file = 'data.txt',
			agent=self.scraper4(),
			depends_on=[self.retriever_task()],
			inputs={"website_url": "{{retriever_task.retrieved_url}}"},
			output_key="scraped_data_4"
		)

	@task
	def scraper5_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrape5_task'],
			output_file = 'data.txt',
			agent=self.scraper5(),
			depends_on=[self.retriever_task()],
			inputs={"website_url": "{{retriever_task.retrieved_url}}"},
			output_key="scraped_data_5"
		)

	@task 
	def mentor_task(self) -> Task:
		return Task(
			config=self.tasks_config['mentor_task'],
			output_file = 'data.txt',
			agent=self.mentor(),
			depends_on=[self.scraper_task(),self.scraper2_task(),self.scraper3_task(),self.scraper4_task(),self.scraper5_task()],
			inputs={
            "source1": "{{scraper_task.scraped_data_1}}",  
            "source2": "{{scraper2_task.scraped_data_2}}",
            "source3": "{{scraper3_task.scraped_data_3}}",
            "source4": "{{scraper4_task.scraped_data_4}}",
            "source5": "{{scraper5_task.scraped_data_5}}"
        } 
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ReferenceCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge
		
		return Crew(
			agents=self.agents,  # Automatically created by the @agent decorator
			tasks=[self.retriever_task(),self.scraper_task(),self.scraper2_task(),self.scraper3_task(),self.scraper4_task(),self.scraper5_task(),self.mentor_task()],  # Automatically created by the @task decorator
			##manager_llm=ChatOpenAI(temperature=0, model="gpt-4o"),
			process=Process.sequential,
			verbose=True,
			#manager_agent=None,
		)
	