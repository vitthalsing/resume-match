from input_handler import load_job_description, load_resumes
from analysis import map_skills_to_resume

def print_resume_report(resume_name, skill_mapping):
    resume_details = skill_mapping[resume_name]['resume_details']
    job_details = skill_mapping[resume_name]['job_details']
    matched_skills = skill_mapping[resume_name]['matched_skills']
    gaps = skill_mapping[resume_name]['gaps']
    
    # Format and print the report
    print(f"\n--- Report for {resume_name} ---")
    print(f"Name: {resume_details.name}")
    print(f"Location: {resume_details.location}")
    print(f"Years of Experience: {resume_details.years_of_experience}")
    print(f"Education: {', '.join(resume_details.education)}")
    print(f"Matched Skills: {', '.join(matched_skills)}")
    print(f"Gaps: {', '.join(gaps)}")
    print(f"Job Title: {job_details.title}")
    print(f"Job Required Skills: {', '.join(job_details.skills)}")
    print(f"Suitability Score for Skills: {skill_mapping[resume_name]['suitability_score']:.2f}")
    print(f"Experience Match: {skill_mapping[resume_name]['experience_match']}")
    print(f"Education and Certification Score: {skill_mapping[resume_name]['education_certification_score']}")
    print(f"Other Factors Score like location, languages, soft skills: {skill_mapping[resume_name]['other_factors_score']}")
    print(f"Total Score: {skill_mapping[resume_name]['total_score']:.2f}")
    print(f"Task Recommendations: {', '.join(skill_mapping[resume_name]['task_recommendations'])}")
    print("-----------------------------------")

def main():
    job_description = load_job_description('data/job_description.txt')
    resumes = load_resumes('data/resumes/')
    
    skill_mapping = map_skills_to_resume(job_description, resumes)
    
    # Output results
    for resume_name in resumes.keys():
        print_resume_report(resume_name, skill_mapping)
if __name__ == "__main__":
    main()