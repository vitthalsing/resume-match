from pydantic import BaseModel, Field
from typing import Literal

class TechnicalSkill(BaseModel):
    skill: str = Field(description="A technical skill in lower case")

class MatchedTechnicalSkills(BaseModel):
    matched_skills: list[TechnicalSkill] = Field(description="A list of matched technical skills in lower case")

class SoftSkill(BaseModel):
    skill: str = Field(description="A soft skill in lower case")

class MatchedSoftSkills(BaseModel):
    matched_skills: list[SoftSkill] = Field(description="A list of matched soft skills in lower case")

class Education(BaseModel):
    degree: str = Field(description="Degree in lower case")
    institution: str = Field(description="Institution in lower case")
    year: int = Field(description="Year of graduation in lower case")

class Certification(BaseModel):
    title: str = Field(description="Title of the certification in lower case")
    institution: str = Field(description="Institution in lower case")
    year: int = Field(description="Year of certification in lower case")

class SpokenLanguage(BaseModel):
    language: str = Field(description="Human language in lower case")
    proficiency: Literal['Native', 'Fluent', 'Intermediate', 'Basic'] = Field(description="Proficiency in the language")

class MatchedSpokenLanguages(BaseModel):
    matched_languages: list[SpokenLanguage] = Field(description="A list of matched spoken languages in lower case")

class Location(BaseModel):
    city: str = Field(description="City in lower case")
    country: str = Field(description="Country in lower case")

class Resume(BaseModel):
    name: str = Field(description="Name of the person in the resume")
    skills: list[TechnicalSkill] = Field(description="A list of technical skills in the resume in lower case")
    years_of_experience: int = Field(description="Total Years of experience in the resume content")
    education: list[Education] = Field(description="A list of education in the resume content in lower case")
    certifications: list[Certification] = Field(description="A list of certifications in the resume content in lower case")
    soft_skills: list[SoftSkill] = Field(description="A list of soft skills in the resume content in lower case")
    spoken_languages: list[SpokenLanguage] = Field(description="A list of spoken languages in the resume content in lower case")
    location: Location = Field(description="Location of city and country in the resume content in lower case")

class JobDescription(BaseModel):
    title: str = Field(description="Title of the job description")
    skills: list[TechnicalSkill] = Field(description="A list of technical skills in the job description in lower case")
    years_of_experience: int = Field(description="Years of experience in the job description")
    education: list[Education] = Field(description="A list of education in the job description in lower case")
    certifications: list[Certification] = Field(description="A list of certifications in the job description in lower case")
    soft_skills: list[SoftSkill] = Field(description="A list of soft skills in the job description in lower case")
    spoken_languages: list[SpokenLanguage] = Field(description="A list of spoken languages in the job description in lower case")
    location: Location = Field(description="Location of city and country in the job description in lower case")

class ResumeAnalysis(BaseModel):
    resume: Resume = Field(description="Analyzed resume")
    job_description: JobDescription = Field(description="Analyzed job description")
    key_matches: MatchedTechnicalSkills = Field(description="Key matches found between resume and job description")
    education_match: Literal['Above', 'Equal', 'Below'] = Field(description="Education match score between resume and job description based on highest education required as per job description and highest education in resume")
    experience_match: Literal['Above', 'Equal', 'Below'] = Field(description="Experience match score between resume and job description based on total years of experience required as per job description and total years of experience in resume")
    certifications_match: Literal['Above', 'Equal', 'Below'] = Field(description="Certifications match score between resume and job description based on highest certifications required as per job description and highest certifications in resume")
    soft_skills_match: MatchedSoftSkills = Field(description="Soft skills match score between resume and job description")
    spoken_languages_match: MatchedSpokenLanguages = Field(description="Spoken languages match score between resume and job description")
    location_match: bool = Field(description="Location match score between resume and job description")
    gaps: list[str] = Field(description="Gaps or missing requirements in the resume")
    task_recommendations: dict[str, list[str]] = Field(description="Actionable tasks for each candidate to address identified gaps")

class GraphState(BaseModel):
    job_description_text: str = None
    resume_text: str = None
    job_description: JobDescription = None
    resume: Resume = None
    resume_analysis: ResumeAnalysis = None
    final_textual_report: str = None
    follow_up_question: str = None
    follow_up_report: str = None
    next_node: str = None

