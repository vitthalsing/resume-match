from langgraph.graph import StateGraph, START, END
from resume_agent.llms import get_llm
from resume_agent.models import JobDescription, Resume, ResumeAnalysis, GraphState
from trustcall import create_extractor

llm = get_llm()

# Define extraction functions
def extract_job_description_function(state: GraphState) -> JobDescription:
    job_description_text = state.job_description_text
    try:
        bound = create_extractor(
            llm,
            tools=[JobDescription],
            tool_choice="JobDescription",
        )

        result = bound.invoke(
            f"""Extract the details from the following job description content:
        <convo>
        {job_description_text}
        </convo>
        
        Instructions:
        <ins>
        {state.follow_up_question}
        </ins>"""
        )
        
        state.job_description = result["responses"][0]
        print("Job description extracted successfully")
        
        return state
    except Exception as e:
        print(f"Error during job description extraction: {e}")
        return None

def extract_resume_function(state: GraphState) -> Resume:
    resume_text = state.resume_text
    try:
        bound = create_extractor(
            llm,
            tools=[Resume],
            tool_choice="Resume",
        )
        result = bound.invoke(
            f"""Extract the details from the following resume content:
        <convo>
        {resume_text}
        </convo>
        
        Instructions:
        <ins>
        {state.follow_up_question}
        </ins>"""
        )
        
        state.resume = result["responses"][0]
        print("Resume extracted successfully")
        return state
    except Exception as e:
        print(f"Error during resume extraction: {e}")
        return None

def extract_resume_analysis_function(state: GraphState) -> ResumeAnalysis:
    try:
        bound = create_extractor(
            llm,
            tools=[ResumeAnalysis],
            tool_choice="ResumeAnalysis",
        )
        result = bound.invoke(
            f"""Extract the details from the following context:
            <convo>
            {state}
            </convo>
            
            Instructions:
            <ins>
            {state.follow_up_question}
            </ins>"""
        )
        state.resume_analysis = result["responses"][0]
        print("Resume Analysis extracted successfully")
        return state
    except Exception as e:
        print(f"Error during resume analysis extraction: {e}")
        return None

def generate_final_report_function(state: GraphState) -> GraphState:
    try:
        prompt = f"""
        Generate a detailed, professional textual report based on the following resume analysis:

        Resume and Job Description Details: {state}

        The report should:
        To evaluate the resumes against the Job Description, use the following scoring guidelines:
        - Match on Skills: (Matched skills/Job Description skills). Assign 40% weightage to how well the candidate's skills align with the JD.
        - Match on Experience: 30 for Above, 20 for equal, 10 from below else 0. Assign 30% weightage to the relevance and duration of the candidate's experience.
        - Match on Certifications and Education: Assign 20% weightage to certifications, degrees, or other qualifications.
        - Other Factors: Assign 10% weightage to additional relevant elements, such as soft skills, location, or languages.
 
        Each resume should receive a total score out of 100, based on these criteria. Provide a
        breakdown of scores for candidate, along with a brief explanation of how the scores
        were derived.
        """

        final_report = llm.invoke(prompt)
        
        state.final_textual_report = final_report.content
        print("Final textual report generated successfully")

        return state
    except Exception as e:
        print(f"Error during final report generation: {e}")
        return None

def handle_follow_up_question_function(state: GraphState) -> GraphState:
    try:
        prompt = f"""
        You have previously generated a report analyzing a resume against a job description. 
        A new follow-up question has been asked: {state.follow_up_question}

        Previous Report and Context:
        {state}

        Please provide a detailed response to the follow-up question, 
        drawing from the previous analysis and adding any new insights 
        or clarifications that are relevant to the question.

        Guidelines:
        - Directly address the specific question asked
        - Refer back to the original resume and job description analysis
        - Provide a clear, concise, and professional response
        - If the question requires additional context, explain why

        Remember
        To evaluate the resumes against the Job Description, use the following scoring guidelines:
        - Match on Skills: (Matched skills/Job Description skills). Assign 40% weightage to how well the candidate's skills align with the JD.
        - Match on Experience: 30 for Above, 20 for equal, 10 from below else 0. Assign 30% weightage to the relevance and duration of the candidate's experience.
        - Match on Certifications and Education: Assign 20% weightage to certifications, degrees, or other qualifications.
        - Other Factors: Assign 10% weightage to additional relevant elements, such as soft skills, location, or languages.

        Each resume should receive a total score out of 100, based on these criteria. Provide a
        breakdown of scores for candidate, along with a brief explanation of how the scores
        were derived.
        """

        follow_up_response = llm.invoke(prompt)
        
        state.follow_up_report = follow_up_response.content
        print("Follow-up report generated successfully")

        return state
    except Exception as e:
        print(f"Error during follow-up question handling: {e}")
        return None

def check_follow_up(state: GraphState) -> str:
    state.next_node = "handle_follow_up" if state.follow_up_question else "generate_final_report"
    return state

workflow = StateGraph(state_schema=GraphState)

workflow.add_node("extract_job_description", extract_job_description_function)
workflow.add_node("extract_resume", extract_resume_function)
workflow.add_node("generate_final_report", generate_final_report_function)
workflow.add_node("handle_follow_up", handle_follow_up_question_function)
workflow.add_node("check_follow_up", check_follow_up)


workflow.add_conditional_edges("check_follow_up", lambda state: state.next_node, {
    "handle_follow_up": "handle_follow_up",
    "generate_final_report": "generate_final_report"
})

workflow.add_edge(START, "extract_job_description")
workflow.add_edge("extract_job_description", "extract_resume")
workflow.add_edge("extract_resume", "check_follow_up")
workflow.add_edge("generate_final_report", END)
workflow.add_edge("handle_follow_up", END)

graph = workflow.compile()
