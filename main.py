import os
import sys
import json
import openai
import PyPDF2
import argparse
import logging
from openai import OpenAI

# Initialize the OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_pdf(file_path):
    logger.info(f"Reading PDF file: {file_path}")
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        logger.error(f"Error reading PDF file {file_path}: {e}")
        raise

def get_prompt(job_rec, current_resume, detailed_job_history):
    return f"""
    Job Description:
    {job_rec}

    Old Resume:
    {current_resume}

    Detailed Job History:
    {detailed_job_history}
    
    Please generate a resume and cover letter tailored to the provided job description. The resume should:

    1. Highlight relevant leadership experience, technical expertise, and significant projects related to the job description.
    2. Include a strong professional summary that emphasizes leadership skills, technical expertise, and significant achievements.
    3. Extract and prioritize the most relevant experiences and skills from the detailed job history and current resume to match the job requirements.
    4. Highlight key achievements for each relevant role using quantifiable metrics to demonstrate impact.
    5. Use strong action verbs to begin bullet points and convey contributions and impact.
    6. Showcase leadership and teamwork experience, including mentorship or coaching roles.
    7. Detail technical skills and provide context by describing their use in work.
    8. Include relevant projects with details about role, technologies used, and outcomes.
    9. List relevant certifications, courses, or professional development activities.
    10. Ensure the resume is free of typos and grammatical errors
    11. Ensure the resume will not be too long, and only includes RECENT important experience and education.
    12. Remove any special characters in the resume like bullets.

    Focus on aligning the candidate's experience with the job requirements provided in the job description.

    For the cover letter, ensure it:

    1. Starts with a brief introduction and expresses interest in the specific position.
    2. Emphasizes the candidate’s most recent and relevant experiences first, followed by past roles.
    3. Highlights unique aspects of the candidate’s background that align with the job description.
    4. Avoids directly repeating content from the resume.
    5. Includes quantifiable achievements and specific projects relevant to the job.
    6. Maintains a professional and engaging tone throughout.
    7. Clearly explains why the candidate is a good fit for the role based on their experiences and skills.
    8. Concludes by expressing enthusiasm for the position and willingness to discuss further.

    Format the response in the following JSON structure:

    {{
        "cover_letter": "Your cover letter content here",
        "resume": {{
            "contact_information": {{
                "name": "Full Name",
                "email": "Email Address",
                "phone": "Phone Number"
            }},
            "summary": "Brief summary or objective statement emphasizing leadership and technical skills",
            "work_experience": [
                {{
                    "company": "Company Name",
                    "location": "Location",
                    "roles": [
                        {{
                            "job_title": "Job Title",
                            "start_date": "Start Date",
                            "end_date": "End Date",
                            "responsibilities": "Description of responsibilities, key projects, and achievements, focusing on leadership and technical impact"
                        }}
                        // Add more roles as needed
                    ]
                }}
                // Add more work experience entries as needed
            ],
            "education": [
                {{
                    "degree": "Degree",
                    "institution": "Institution Name",
                    "location": "Location",
                    "graduation_year": "Graduation Year",
                    "details": "Relevant coursework, projects, and honors"
                }}
                // Add more education entries as needed
            ],
            "skills": [
                {{
                    "skill_name": "Skill Name",
                    "proficiency_level": "Proficiency Level",
                    "experience": "Description of relevant projects, experiences, and achievements demonstrating this skill"
                }}
                // Add more skills as needed
            ],
            "certifications": [
                {{
                    "certification_name": "Certification Name",
                    "issuing_organization": "Issuing Organization",
                    "issue_date": "Issue Date",
                    "details": "Details of the certification and relevance to the role"
                }}
                // Add more certifications as needed
            ],
            "publications": [
                {{
                    "title": "Publication Title",
                    "publication_date": "Publication Date",
                    "publication_link": "Link to the publication",
                    "summary": "Summary of the publication and its impact"
                }}
                // Add more publications as needed
            ],
            "projects": [
                {{
                    "project_name": "Project Name",
                    "description": "Description of the project, your role, technologies used, and the impact or results of the project"
                }}
                // Add more projects as needed
            ],
            "awards_and_honors": [
                {{
                    "award_name": "Award Name",
                    "issuing_organization": "Issuing Organization",
                    "issue_date": "Issue Date",
                    "details": "Details of the award and its relevance to the role"
                }}
                // Add more awards as needed
            ],
            "professional_affiliations": [
                {{
                    "organization_name": "Organization Name",
                    "role": "Your Role"
                }}
                // Add more affiliations as needed
            ]
        }}
    }}
    """


def generate_content(job_rec, current_resume, detailed_job_history):
    prompt = get_prompt(job_rec, current_resume, detailed_job_history)
    
    logger.info("Generating content with OpenAI GPT-4")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional tech recruiter, an expert in the current tech recruiting trends and approaches. You generate professional resumes and cover letters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating content with OpenAI GPT-4: {e}")
        raise

def main(args):
    try:
        job_rec = read_pdf(args.job_rec) if args.job_rec.endswith('.pdf') else open(args.job_rec).read()
        current_resume = read_pdf(args.current_resume) if args.current_resume.endswith('.pdf') else open(args.current_resume).read()
        detailed_job_history = open(args.detailed_job_history).read()

        logger.info("Generating resume and cover letter")
        generated_content = generate_content(job_rec, current_resume, detailed_job_history)
        generated_content = generated_content.replace("```json","")
        generated_content = generated_content.replace("```","")
        logger.info(generated_content)
        # Parse the JSON response
        content_json = json.loads(generated_content)
        
        with open("cover_letter.json", "w") as cover_letter_file:
            json.dump({"cover_letter": content_json["cover_letter"]}, cover_letter_file)
            logger.info("Cover letter saved to cover_letter.json")
        
        with open("resume.json", "w") as resume_file:
            json.dump({"resume": content_json["resume"]}, resume_file)
            logger.info("Resume saved to resume.json")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a tailored resume and cover letter using OpenAI GPT-4.')
    parser.add_argument('--job-desc', type=str, required=True, help='Path to the job description file (txt or pdf).')
    parser.add_argument('--current-resume', type=str, required=True, help='Path to the current resume file (txt or pdf).')
    parser.add_argument('--detailed-job-history', type=str, required=True, help='Path to the detailed job history file (txt).')
    
    args = parser.parse_args()
    main(args)