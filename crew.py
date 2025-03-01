from crewai import Crew, Process, Agent, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool,SerperDevTool,FileWriterTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()


Model = 'gpt-4o'
api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model = Model,api_key=api_key)

crawlTool = SerperDevTool(
	n_results=5
)
file_writer = FileWriterTool()


@CrewBase
class Codingmentorcrew():
	"""Coding Mentor Crew"""

	tasks_config = 'config/tasks.yaml'

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
			agents=self.agents, 
			tasks=[self.retriever_task(),self.mentor_task()], 
			process=Process.sequential,
			verbose=True,
		)