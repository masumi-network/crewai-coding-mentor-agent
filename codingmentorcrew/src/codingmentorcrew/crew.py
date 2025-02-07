from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Codingmentorcrew():
	"""Codingmentorcrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def mentor(self) -> Agent:
		return Agent(
			config=self.agents_config['mentor'],
			verbose=True
		)

	@agent
	def transcriber(self) -> Agent:
		return Agent(
			config=self.agents_config['transcriber'],
			verbose=True
		)
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def mentorship_task(self) -> Task:
		return Task(
			config=self.tasks_config['mentorship_task'],
		)

	@task
	def transcribe_task(self) -> Task:
		return Task(
			config=self.tasks_config['transcribe_task'],
		)
	
	def route_input(self, input_text) -> Agent:
		# Simple routing based on input
		if '1' in input_text:  
			print('routing to mentor')
			return [self.mentor(),self.mentorship_task()]
		else:# Otherwise, route to the text generation agent
			print('routing to other')
			return [self.transcriber(),self.transcribe_task()]

	@crew
	def crew(self) -> Crew:
		"""Creates the Codingmentorcrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge
		input_text = str(input("Enter your input: ")) 
		
		process = self.route_input(input_text)
		selected_agent = process[0]
		selected_task = process[1]

		return Crew(
			agents= [selected_agent], # Automatically created by the @agent decorator
			tasks= [selected_task], # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)


