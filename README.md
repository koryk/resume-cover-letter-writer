**Disclaimer:** This project is provided "as is" without any warranties or guarantees. The author makes no claims regarding the accuracy, relevance, or completeness of the generated content. Users are advised to review and edit the generated documents to ensure they meet their specific requirements and standards. The author assumes no liability for any errors or omissions in the content provided by this project.

**Disclaimer:** This project utilizes OpenAI's GPT-4 for generating resume and cover letter content. The accuracy and relevance of the generated content depend on the input data provided. Please review and edit the generated documents to ensure they meet your requirements and standards.

# LLM-Driven Resume Writer

This project generates a tailored resume and cover letter using OpenAI's GPT-4. The script processes a job description, current resume, and detailed job history to produce HTML and PDF files for the resume and a JSON file for the cover letter.

## Requirements

- Python 3.9.7 or later
- `pip` (Python package installer)

## Setup

1. **Create and activate a virtual environment:**

    ```bash
    python -m venv llm-resume-env
    source llm-resume-env/bin/activate  # On Windows use `llm-resume-env\Scripts\activate`
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set your OpenAI API key:**

    ```bash
    export OPENAI_API_KEY='your_openai_api_key'  # On Windows use `set OPENAI_API_KEY=your_openai_api_key`
    ```

## Usage

1. **Run the main script to generate the JSON files:**

    ```bash
    python main.py --job-desc rec.pdf --current-resume resume.pdf --detailed-job-history other.txt
    ```

    This will generate `cover_letter.json` and `resume.json`.

2. **Run the script to generate the HTML and PDF resume:**

    ```bash
    python generate_resume.py
    ```

    This will generate `resume.html` and `generated_resume.pdf`.

## Notes

- Ensure the input files (`rec.pdf`, `resume.pdf`, and `other.txt`) are in the correct format and contain relevant information.
- The OpenAI API key must be set in your environment for the scripts to function correctly.