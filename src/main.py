from resume_agent.graph import graph
from resume_agent.tools import get_resume_content, get_job_description
from resume_agent.models import GraphState

job_description_text = get_job_description()
resume_text = get_resume_content()

initial_inputs = {
    "job_description_text": job_description_text,
    "resume_text": resume_text
}

initial_state = GraphState(**initial_inputs)

initial_report = graph.invoke(input=initial_state)

if initial_report is None:
    print("Failed to generate report due to extraction errors.")
else:
    print("Initial Report Generated:")
    print(initial_report["final_textual_report"])

while True:
    user_question = input("Ask a follow-up question (or type 'exit' to quit): ")
    if user_question.lower() == 'exit':
        break
    
    initial_state.follow_up_question = user_question
    
    updated_state = graph.invoke(input=initial_state)
    
    if updated_state is None:
        print("Failed to generate follow-up report due to errors.")
    else:
        print("Updated Report:")
        print(updated_state["follow_up_report"])