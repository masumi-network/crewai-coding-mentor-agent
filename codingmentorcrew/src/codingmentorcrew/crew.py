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
	n_results=5
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
	def mentor(self) -> Agent:
		return Agent(
			config=self.agents_config['mentor'],
			tools=[ScrapeWebsiteTool()],
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
			output_key="retrieved_urls"
		)
	
	@task
	def mentor_task(self) -> Task:
		return Task(
			config=self.tasks_config['mentor_task'],
			output_file = 'data.txt',
			agent=self.mentor(),
			depends_on=[self.retriever_task()],
			inputs={"website_url": "{{retriever_task.retrieved_urls}}"},
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ReferenceCrew crew"""	
		return Crew(
			agents=self.agents,  # Automatically created by the @agent decorator
			tasks=[self.retriever_task(),self.mentor_task()],  # Automatically created by the @task decorator
			##manager_llm=ChatOpenAI(temperature=0, model="gpt-4o"),
			process=Process.sequential,
			verbose=True,
			#manager_agent=None,
		)
	