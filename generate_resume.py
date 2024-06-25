import json
import pdfkit

def generate_resume_html(resume_data):
    contact_info = resume_data['contact_information']
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            .section-title {{
                font-size: 24px;
                font-weight: bold;
                border-bottom: 2px solid #000;
                padding-bottom: 5px;
                margin-bottom: 10px;
            }}
            .item-title {{
                font-size: 18px;
                font-weight: bold;
            }}
            .item-subtitle {{
                font-size: 16px;
                font-style: italic;
            }}
            .item-description {{
                margin-left: 20px;
            }}
            .contact-info {{
                margin-bottom: 20px;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="contact-info">
            <h1>{contact_info.get('name', '')}</h1>
    """
    if 'email' in contact_info:
        html_content += f"<p>Email: {contact_info['email']}</p>"
    if 'phone' in contact_info:
        html_content += f"<p>Phone: {contact_info['phone']}</p>"

    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Professional Summary</div>
            <p>{summary}</p>
        </div>
        <div class="section">
            <div class="section-title">Work Experience</div>
    """.format(summary=resume_data.get('summary', ''))

    for experience in resume_data['work_experience']:
        html_content += f"""
            <div class="item">
                <div class="item-title">{experience['company']}</div>
                <div class="item-subtitle">{experience['location']}</div>
                <div class="item-description">
        """
        for role in experience['roles']:
            responsibilities = role['responsibilities'].split(' • ')
            html_content += f"""
                <p><strong>{role['job_title']}</strong> ({role['start_date']} - {role['end_date']})</p>
                <ul>
            """
            for responsibility in responsibilities:
                html_content += f"<li>{responsibility.strip()}</li>"
            html_content += """
                </ul>
            """
        html_content += """
                </div>
            </div>
        """
    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Education</div>
    """
    for education in resume_data.get('education', []):
        html_content += f"""
            <div class="item">
                <div class="item-title">{education['degree']}</div>
                <div class="item-subtitle">{education['institution']} - {education['location']}</div>
                <div class="item-description">
                    <p>Graduation Year: {education['graduation_year']}</p>
                    <p>{education['details']}</p>
                </div>
            </div>
        """
    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Skills</div>
    """
    for skill in resume_data.get('skills', []):
        html_content += f"""
            <div class="item">
                <div class="item-title">{skill['skill_name']}</div>
                <div class="item-description">
                    <p>Proficiency Level: {skill['proficiency_level']}</p>
                    <p>{skill['experience']}</p>
                </div>
            </div>
        """
    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Certifications</div>
    """
    for certification in resume_data.get('certifications', []):
        html_content += f"""
            <div class="item">
                <div class="item-title">{certification['certification_name']}</div>
                <div class="item-subtitle">{certification['issuing_organization']} - {certification['issue_date']}</div>
                <div class="item-description">
                    <p>{certification['details']}</p>
                </div>
            </div>
        """
    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Publications</div>
    """
    for publication in resume_data.get('publications', []):
        html_content += f"""
            <div class="item">
                <div class="item-title">{publication['title']}</div>
                <div class="item-subtitle">{publication['publication_date']}</div>
                <div class="item-description">
                    <p><a href="{publication['publication_link']}">{publication['publication_link']}</a></p>
                    <p>{publication['summary']}</p>
                </div>
            </div>
        """
    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Projects</div>
    """
    for project in resume_data.get('projects', []):
        html_content += f"""
            <div class="item">
                <div class="item-title">{project['project_name']}</div>
                <div class="item-description">
                    <p>{project['description']}</p>
                </div>
            </div>
        """
    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Awards and Honors</div>
    """
    for award in resume_data.get('awards_and_honors', []):
        html_content += f"""
            <div class="item">
                <div class="item-title">{award['award_name']}</div>
                <div class="item-subtitle">{award['issuing_organization']} - {award['issue_date']}</div>
                <div class="item-description">
                    <p>{award['details']}</p>
                </div>
            </div>
        """
    html_content += """
        </div>
        <div class="section">
            <div class="section-title">Professional Affiliations</div>
    """
    for affiliation in resume_data.get('professional_affiliations', []):
        html_content += f"""
            <div class="item">
                <div class="item-title">{affiliation['organization_name']}</div>
                <div class="item-description">
                    <p>{affiliation['role']}</p>
                </div>
            </div>
        """
    html_content += """
        </div>
    </body>
    </html>
    """
    return html_content

def generate_resume():
    with open("resume.json", "r") as file:
        resume_data = json.load(file)
    
    html_content = generate_resume_html(resume_data['resume'])
    
    with open("resume.html", "w") as html_file:
        html_file.write(html_content)
    
    pdfkit.from_file("resume.html", "resume_new.pdf")

if __name__ == "__main__":
    generate_resume()
