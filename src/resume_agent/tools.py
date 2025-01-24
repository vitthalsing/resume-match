import os
from langchain_community.document_loaders import PyPDFLoader

def get_resume_content() -> str:
    """Get the resume content from the resume file"""
    file_path = os.path.join(os.path.dirname(__file__), os.getenv("RESUME_FILE_PATH"))
    if file_path.endswith('.pdf'):
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            page_content = ' '.join([page.page_content for page in pages])
            
        except Exception as e:
            print(f"Error loading {os.getenv("RESUME_FILE_PATH")}: {e}")
    print("Extracting resume content...")
    return page_content

def get_job_description() -> str:
    """Get the job description from the job description file"""
    with open(os.path.join(os.path.dirname(__file__), os.getenv("JOB_DESCRIPTION_FILE_PATH")), 'r') as file:
        print("Loading job description...")
        job_description = file.read()
    return job_description
