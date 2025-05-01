# Resume Matcher

A sophisticated resume analysis tool that helps job seekers optimize their resumes for specific job descriptions. The application provides detailed matching analysis, keyword suggestions, and optimization recommendations.

## Features

- Resume and job description parsing (PDF and DOCX formats)
- Keyword extraction and matching
- Semantic similarity analysis
- Category-wise matching scores
- Detailed optimization suggestions
- Modern and responsive UI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/joshiprashant09/Resume-Matcher-and-Analysis.git
cd Resume-Matcher-and-Analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload your resume and job description files (PDF or DOCX format)

4. View the analysis results and optimization suggestions

## Project Structure

```
resume-matcher/
├── app.py                  # Main Flask application
├── document_parser.py      # Document parsing utilities
├── keyword_extractor.py    # Keyword extraction and matching logic
├── optimizer.py            # Resume optimization suggestions
├── requirements.txt        # Project dependencies
├── templates/              # HTML templates
│   └── index.html          # Main UI template
└── venv/                   # Virtual environment
```

## Dependencies

- Flask: Web framework
- spaCy: Natural language processing
- scikit-learn: Machine learning utilities
- PyPDF2: PDF parsing
- python-docx: DOCX parsing
- Bootstrap: Frontend framework
- Chart.js: Data visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 