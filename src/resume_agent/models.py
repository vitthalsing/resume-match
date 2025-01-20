from pydantic import BaseModel, Field
from typing import Literal

class Resume(BaseModel):
    name: str = Field(description="Name of the person in the resume")
    skills: list[str] = Field(description="A list of skills in the resume in lower case")
    years_of_experience: int = Field(description="Total Years of experience in the resume content")
    education: list[str] = Field(description="A list of education in the resume content in lower case")
    certifications: list[str] = Field(description="A list of certifications in the resume content in lower case")
    soft_skills: list[str] = Field(description="A list of soft skills in the resume content in lower case")
    spoken_languages: list[str] = Field(description="A list of spoken languages in the resume content in lower case")
    location: str = Field(description="Location of city and country in the resume content in lower case")

class JobDescription(BaseModel):
    title: str = Field(description="Title of the job description")
    skills: list[str] = Field(description="A list of skills in the job description in lower case")
    years_of_experience: int = Field(description="Years of experience in the job description")
    education: list[str] = Field(description="A list of education in the job description in lower case")
    certifications: list[str] = Field(description="A list of certifications in the job description in lower case")
    soft_skills: list[str] = Field(description="A list of soft skills in the job description in lower case")
    spoken_languages: list[str] = Field(description="A list of spoken languages in the job description in lower case")
    location: str = Field(description="Location of city and country in the job description in lower case")

class Similarity(BaseModel):
    is_similar: bool = Field(description="Whether the skills are similar")

class MatchedSkills(BaseModel):
    matched_skills: list[str] = Field(description="A list of matched skills")

class EducationScore(BaseModel):
    education_match: bool = Field(description="Whether the education is matched")
    education_match_level: Literal['equal', 'lower', 'higher'] = Field(description="The level of education match")

class CertificationScore(BaseModel):
    certification_match_list: list[str] = Field(description="List of matched certifications")







