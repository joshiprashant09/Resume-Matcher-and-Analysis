import spacy
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load English language model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    """
    Extract important keywords from text using spaCy with enhanced analysis
    """
    # Process the text
    doc = nlp(text.lower())
    
    # Extract different types of keywords
    keywords = {
        'technical': [],
        'soft_skills': [],
        'experience': [],
        'education': [],
        'certifications': []
    }
    
    # Technical skills and tools
    tech_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes', 
                    'machine learning', 'ai', 'data analysis', 'cloud', 'devops', 'agile']
    
    # Soft skills
    soft_skills = ['leadership', 'communication', 'teamwork', 'problem-solving', 'time management',
                  'adaptability', 'creativity', 'critical thinking']
    
    # Extract keywords based on context
    for token in doc:
        if not token.is_stop and len(token.text) > 2:
            # Technical skills
            if any(tech in token.text.lower() for tech in tech_keywords):
                keywords['technical'].append(token.text)
            # Soft skills
            elif any(skill in token.text.lower() for skill in soft_skills):
                keywords['soft_skills'].append(token.text)
            # Experience indicators
            elif token.pos_ in ['NOUN', 'PROPN'] and any(exp in token.text.lower() for exp in ['year', 'experience', 'project']):
                keywords['experience'].append(token.text)
            # Education indicators
            elif any(edu in token.text.lower() for edu in ['degree', 'bachelor', 'master', 'phd', 'university']):
                keywords['education'].append(token.text)
            # Certification indicators
            elif any(cert in token.text.lower() for cert in ['certified', 'certification', 'license']):
                keywords['certifications'].append(token.text)
    
    # Count frequencies for each category
    for category in keywords:
        keywords[category] = dict(Counter(keywords[category]).most_common(10))
    
    return keywords

def calculate_match_score(resume_keywords, job_keywords):
    """
    Calculate comprehensive match score between resume and job description
    """
    scores = {}
    
    # Calculate category-wise scores
    for category in resume_keywords:
        if category in job_keywords:
            resume_set = set(resume_keywords[category].keys())
            job_set = set(job_keywords[category].keys())
            
            if job_set:
                matching_keywords = resume_set.intersection(job_set)
                category_score = (len(matching_keywords) / len(job_set)) * 100
                scores[category] = round(category_score, 2)
    
    # Calculate overall score with weighted categories
    weights = {
        'technical': 0.4,
        'soft_skills': 0.2,
        'experience': 0.2,
        'education': 0.1,
        'certifications': 0.1
    }
    
    overall_score = sum(scores.get(category, 0) * weights.get(category, 0) 
                       for category in weights)
    
    return {
        'overall_score': round(overall_score, 2),
        'category_scores': scores
    }

def get_missing_keywords(resume_keywords, job_keywords):
    """
    Get missing keywords from job description categorized by type
    """
    missing = {}
    
    for category in job_keywords:
        resume_set = set(resume_keywords.get(category, {}).keys())
        job_set = set(job_keywords[category].keys())
        
        missing[category] = list(job_set - resume_set)
    
    return missing

def calculate_semantic_similarity(resume_text, job_description_text):
    """
    Calculate semantic similarity between resume and job description using TF-IDF and cosine similarity
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)

def analyze_keyword_importance(job_keywords):
    """
    Analyze the importance of keywords in the job description
    """
    importance_scores = {}
    
    for category, keywords in job_keywords.items():
        total_freq = sum(keywords.values())
        importance_scores[category] = {
            keyword: (freq / total_freq) * 100 
            for keyword, freq in keywords.items()
        }
    
    return importance_scores 