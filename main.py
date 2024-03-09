import sys
from crewai import Crew, Process

from agents import YoutuberAssistant
from task import YoutuberTasks
from file_io import save_markdown

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


openAIGPT4 = ChatOpenAI(
    # model="gpt-3.5-turbo",
    model="gpt-4-turbo-preview",

)
agents = YoutuberAssistant()
tasks = YoutuberTasks()

theme = sys.argv[1]


# Agents
topic_generator = agents.topic_generator_agent()
topic_reviewer = agents.topic_reviewer_agent()
facts_collector = agents.facts_collector_agent()
yt_producer = agents.yt_producer_agent()
script_writer = agents.script_writer_agent()

# Tasks
generate_topics = tasks.generate_topics_task(topic_generator, theme)
review_topics = tasks.review_topics_task(topic_reviewer, [generate_topics])
search_for_interesting_facts = tasks.search_for_interesting_facts_task(facts_collector, [review_topics])
yt_initial_production = tasks.yt_production_task(yt_producer, [review_topics, search_for_interesting_facts])
yt_script_generator = tasks.yt_script_generator_task(agent=script_writer, context=[yt_initial_production, search_for_interesting_facts], callback_function=save_markdown)

# Tools




crew = Crew(
    agents=[topic_generator, topic_reviewer, facts_collector, yt_producer, script_writer],
    tasks=[generate_topics, review_topics, search_for_interesting_facts, yt_initial_production, yt_script_generator],
    process=Process.hierarchical,
    manager_llm=openAIGPT4
)


# Trigger

results = crew.kickoff()

print("Crew work results: ")
print(results)