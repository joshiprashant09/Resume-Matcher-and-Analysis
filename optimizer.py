from keyword_extractor import (
    extract_keywords, 
    get_missing_keywords, 
    calculate_semantic_similarity,
    analyze_keyword_importance
)
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def generate_optimization_suggestions(resume_text, job_description_text):
    """
    Generate comprehensive suggestions to optimize resume based on job description
    """
    # Extract keywords and analyze
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description_text)
    
    # Get missing keywords and their importance
    missing_keywords = get_missing_keywords(resume_keywords, job_keywords) or {}
    keyword_importance = analyze_keyword_importance(job_keywords) or {}
    
    # Calculate semantic similarity
    semantic_score = calculate_semantic_similarity(resume_text, job_description_text)
    
    # Generate suggestions
    suggestions = []
    
    # Add missing keywords suggestions
    for category, keywords in missing_keywords.items():
        if keywords and isinstance(keywords, list):  # Ensure keywords is a list
            important_keywords = [
                kw for kw in keywords 
                if keyword_importance.get(category, {}).get(kw, 0) > 10
            ]
            if important_keywords:
                suggestions.append({
                    'type': f'missing_{category}',
                    'title': f'Add Important {category.replace("_", " ").title()}',
                    'description': f'Consider adding these important {category.replace("_", " ")}: {", ".join(important_keywords[:5])}',
                    'priority': 'high' if category == 'technical' else 'medium'
                })
    
    # Analyze and suggest improvements for each section
    skills_suggestions = analyze_skills_section(resume_text, job_description_text)
    if skills_suggestions:
        suggestions.extend(skills_suggestions)
    
    experience_suggestions = analyze_experience_section(resume_text, job_description_text)
    if experience_suggestions:
        suggestions.extend(experience_suggestions)
    
    education_suggestions = analyze_education_section(resume_text, job_description_text)
    if education_suggestions:
        suggestions.extend(education_suggestions)
    
    achievements_suggestions = analyze_achievements_section(resume_text, job_description_text)
    if achievements_suggestions:
        suggestions.extend(achievements_suggestions)
    
    # Add semantic similarity suggestion
    if semantic_score < 50:
        suggestions.append({
            'type': 'semantic_similarity',
            'title': 'Improve Content Relevance',
            'description': 'Your resume content could be more aligned with the job description. Consider restructuring your experience and skills to better match the role requirements.',
            'priority': 'high'
        })
    
    # Sort suggestions by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 2))
    
    return suggestions

def analyze_skills_section(resume_text, job_description_text):
    """
    Analyze skills section and provide detailed suggestions
    """
    suggestions = []
    
    try:
        # Process both texts
        resume_doc = nlp(resume_text.lower())
        job_doc = nlp(job_description_text.lower())
        
        # Look for skills section
        skills_section = None
        for sent in resume_doc.sents:
            if 'skills' in sent.text:
                skills_section = sent.text
                break
        
        if not skills_section:
            suggestions.append({
                'type': 'skills_section',
                'title': 'Add Skills Section',
                'description': 'Create a dedicated skills section highlighting your technical and professional skills. Group them by category (e.g., Technical Skills, Soft Skills, Tools & Technologies).',
                'priority': 'high'
            })
        else:
            # Analyze skills formatting
            if not re.search(r'[•\-\*]', skills_section):
                suggestions.append({
                    'type': 'skills_format',
                    'title': 'Improve Skills Presentation',
                    'description': 'Format your skills using bullet points for better readability. Group related skills together.',
                    'priority': 'medium'
                })
    except Exception as e:
        print(f"Error in analyze_skills_section: {str(e)}")
    
    return suggestions

def analyze_experience_section(resume_text, job_description_text):
    """
    Analyze experience section and provide detailed suggestions
    """
    suggestions = []
    
    try:
        # Process both texts
        resume_doc = nlp(resume_text.lower())
        job_doc = nlp(job_description_text.lower())
        
        # Look for experience section
        experience_section = None
        for sent in resume_doc.sents:
            if 'experience' in sent.text or 'work' in sent.text:
                experience_section = sent.text
                break
        
        if not experience_section:
            suggestions.append({
                'type': 'experience_section',
                'title': 'Add Experience Section',
                'description': 'Create a detailed experience section showcasing your relevant work history. Include specific achievements and responsibilities.',
                'priority': 'high'
            })
        else:
            # Analyze experience content
            if not re.search(r'\d+', experience_section):
                suggestions.append({
                    'type': 'experience_metrics',
                    'title': 'Add Quantifiable Achievements',
                    'description': 'Include specific metrics and numbers to quantify your achievements (e.g., "increased sales by 20%", "managed team of 5 people").',
                    'priority': 'medium'
                })
    except Exception as e:
        print(f"Error in analyze_experience_section: {str(e)}")
    
    return suggestions

def analyze_education_section(resume_text, job_description_text):
    """
    Analyze education section and provide suggestions
    """
    suggestions = []
    
    try:
        # Process both texts
        resume_doc = nlp(resume_text.lower())
        job_doc = nlp(job_description_text.lower())
        
        # Look for education section
        education_section = None
        for sent in resume_doc.sents:
            if any(edu in sent.text.lower() for edu in ['education', 'degree', 'university', 'college']):
                education_section = sent.text
                break
        
        if not education_section:
            suggestions.append({
                'type': 'education_section',
                'title': 'Add Education Section',
                'description': 'Include your educational background, relevant coursework, and academic achievements.',
                'priority': 'medium'
            })
    except Exception as e:
        print(f"Error in analyze_education_section: {str(e)}")
    
    return suggestions

def analyze_achievements_section(resume_text, job_description_text):
    """
    Analyze achievements section and provide suggestions
    """
    suggestions = []
    
    try:
        # Process both texts
        resume_doc = nlp(resume_text.lower())
        job_doc = nlp(job_description_text.lower())
        
        # Look for achievements section
        achievements_section = None
        for sent in resume_doc.sents:
            if any(ach in sent.text.lower() for ach in ['achievement', 'award', 'recognition', 'accomplishment']):
                achievements_section = sent.text
                break
        
        if not achievements_section:
            suggestions.append({
                'type': 'achievements_section',
                'title': 'Add Achievements Section',
                'description': 'Create a section highlighting your key achievements, awards, and recognitions. Focus on those most relevant to the target role.',
                'priority': 'medium'
            })
    except Exception as e:
        print(f"Error in analyze_achievements_section: {str(e)}")
    
    return suggestions 