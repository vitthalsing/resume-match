import os
from langchain_community.document_loaders import PyPDFLoader

def load_job_description(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def load_resumes(resumes_dir):
    resumes = {}
    for filename in os.listdir(resumes_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(resumes_dir, filename)
            try:
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                resumes[filename] = {
                    'page_content': ' '.join([page.page_content for page in pages])
                }
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return resumes