import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from models import Resume, JobDescription, MatchedSkills, EducationScore, CertificationScore

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)

def evaluate_experience(resume_experience: int, job_experience: int) -> int:
    if job_experience <= 0:
        return 0

    experience_ratio = resume_experience / job_experience

    if experience_ratio >= 1:
        return 20
    elif experience_ratio >= 0.75:
        return 15
    elif experience_ratio >= 0.5:
        return 10
    elif experience_ratio >= 0.25:
        return 5
    else:
        return 0

def find_education_certification_match(parsed_resume_education, job_education, parsed_resume_certifications, job_certifications):
    score = 0
    
    if len(job_education) == 0:
        score += 15
    else:
        education_match = find_education_match(parsed_resume_education, job_education)
        if education_match.education_match:
            if education_match.education_match_level == 'equal':
                score += 10
            elif education_match.education_match_level == 'higher':
                score += 15
            elif education_match.education_match_level == 'lower':
                score += 5

    if len(job_certifications) == 0:
        score += 5
    else:
        certification_match = find_certification_match(parsed_resume_certifications, job_certifications)
        certification_match_ratio = len(certification_match.certification_match_list) / len(job_certifications) if job_certifications else 0
        
        if certification_match_ratio >= 0.75:
            score += 5
        elif certification_match_ratio >= 0.5:
            score += 3
        elif certification_match_ratio >= 0.25:
            score += 1
            
    return score

def map_skills_to_resume(job_description: str, resumes: dict) -> dict:
    logging.info("Mapping skills to resumes.")
    parsed_job_description = extract_details_from_job_description(job_description)
    
    skill_mapping = {}
    
    for resume_name, resume in resumes.items():
        logging.info("Processing resume: %s", resume_name)
        parsed_resume = extract_details_from_resume(resume['page_content'])
        
        matched_skills = find_matched_skills(resume['page_content'], parsed_job_description.skills)
        gaps = [skill for skill in parsed_job_description.skills if skill not in matched_skills]
        suitability_score = len(matched_skills) * 40 / len(parsed_job_description.skills) if parsed_job_description.skills else 40

        experience_match = evaluate_experience(parsed_resume.years_of_experience, parsed_job_description.years_of_experience)

        education_certification_score = find_education_certification_match(
            parsed_resume.education,
            parsed_job_description.education,
            parsed_resume.certifications,
            parsed_job_description.certifications
        )

        other_factors_score = 0
        if parsed_resume.location == parsed_job_description.location:
            other_factors_score += 5
            
        if len(parsed_job_description.spoken_languages) == 0 and 'english' in parsed_resume.spoken_languages:
            other_factors_score += 5
        else:
            matched_languages = set(parsed_resume.spoken_languages).intersection(set(parsed_job_description.spoken_languages))
            if len(parsed_job_description.spoken_languages) > 0:
                match_language_ration = len(matched_languages) / len(parsed_job_description.spoken_languages)
                if match_language_ration >= 0.75:
                    other_factors_score += 5
                elif match_language_ration >= 0.5:
                    other_factors_score += 3
                elif match_language_ration >= 0.25:
                    other_factors_score += 1
            else:
                logging.info("No spoken languages in job description.")

        skill_mapping[resume_name] = {
            'resume_details': parsed_resume,
            'job_details': parsed_job_description,
            'matched_skills': matched_skills,
            'gaps': gaps,
            'experience_match': experience_match,
            'education_certification_score': education_certification_score,
            'other_factors_score': other_factors_score, 
            'suitability_score': suitability_score,
            'total_score': experience_match + education_certification_score + other_factors_score + suitability_score,
            'task_recommendations': [f"Consider taking a course on {', '.join(gaps)}."] if gaps else []
        }
        
    return skill_mapping

def extract_details_from_job_description(job_description):
    logging.info("Calling LLM to extract skills from job description.")
    prompt_template = ChatPromptTemplate.from_template(
        "Extract the details from the following job description: {job_description}"
    )
    job_description_llm = llm.with_structured_output(JobDescription,method="function_calling")
    chain = prompt_template | job_description_llm
    
    try:
        response = chain.invoke(input=job_description)
        logging.info("LLM response: %s", response)
        return response
    except Exception as e:
        logging.error("Error calling LLM: %s", e)
        return []

def extract_details_from_resume(resume_content):
    logging.info("Extracting details from resume content.")
    reusme_llm = llm.with_structured_output(Resume,method="function_calling")
    prompt_template = ChatPromptTemplate.from_template(
        "Extract the details from the following resume content: {resume_content}"
    )

    chain = prompt_template | reusme_llm

    response = chain.invoke(input=resume_content)
    logging.info("LLM response for resume: %s", response)
    return response

def find_matched_skills(page_content, job_skills):
    logging.info("Finding matched skills between:")
    prompt_template = ChatPromptTemplate.from_template(
        "Think carefully and pick one skill from {job_skills} at a time and check if it is present in {page_content} recursively do it for all skills in {job_skills} and return the list of matched skills."
    )
    matched_skills_llm = llm.with_structured_output(MatchedSkills, method="function_calling")
    chain = prompt_template | matched_skills_llm
    response = chain.invoke(input={"page_content": page_content, "job_skills": job_skills})
    logging.info("LLM response for matched skills: %s", response.matched_skills)
    return response.matched_skills

def find_education_match(parsed_resume_education, job_education):
    logging.info("Finding education match between:")
    prompt_template = ChatPromptTemplate.from_template(
        "Eduction degree required for Job are '{job_education}', and candidate's education is '{parsed_resume_education}'. Please return if we have a match and the level of education match."
    )
    education_llm = llm.with_structured_output(EducationScore, method="function_calling")
    chain = prompt_template | education_llm
    response = chain.invoke(input={"parsed_resume_education": parsed_resume_education, "job_education": job_education})
    logging.info("LLM response for education match: %s", response)
    return response

def find_certification_match(parsed_resume_certifications, job_certifications):
    logging.info("Finding certification match between:")
    prompt_template = ChatPromptTemplate.from_template(
        "Certification required for Job are '{job_certifications}', and candidate's certifications are '{parsed_resume_certifications}'. Please return the list of matched certifications with job certifications."
    )
    certification_llm = llm.with_structured_output(CertificationScore, method="function_calling")
    chain = prompt_template | certification_llm
    response = chain.invoke(input={"parsed_resume_certifications": parsed_resume_certifications, "job_certifications": job_certifications})
    logging.info("LLM response for certification match: %s", response)
    return response

