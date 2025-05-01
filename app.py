from flask import Flask, render_template, request, jsonify
from document_parser import parse_resume, parse_job_description
from keyword_extractor import (
    extract_keywords, 
    calculate_match_score, 
    calculate_semantic_similarity
)
from optimizer import generate_optimization_suggestions
import os
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'resume' not in request.files or 'job_description' not in request.files:
            return jsonify({'error': 'Both resume and job description files are required'}), 400
        
        resume_file = request.files['resume']
        job_description_file = request.files['job_description']
        
        logger.debug("Files received successfully")
        
        # Parse documents
        try:
            resume_text = parse_resume(resume_file)
            job_description_text = parse_job_description(job_description_file)
            logger.debug("Documents parsed successfully")
        except Exception as e:
            logger.error(f"Error parsing documents: {str(e)}")
            return jsonify({'error': f'Error parsing documents: {str(e)}'}), 400
        
        # Extract keywords and calculate match score
        try:
            resume_keywords = extract_keywords(resume_text)
            job_keywords = extract_keywords(job_description_text)
            logger.debug("Keywords extracted successfully")
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return jsonify({'error': f'Error extracting keywords: {str(e)}'}), 500
        
        try:
            match_scores = calculate_match_score(resume_keywords, job_keywords)
            logger.debug("Match scores calculated successfully")
        except Exception as e:
            logger.error(f"Error calculating match scores: {str(e)}")
            return jsonify({'error': f'Error calculating match scores: {str(e)}'}), 500
        
        # Calculate semantic similarity
        try:
            semantic_score = calculate_semantic_similarity(resume_text, job_description_text)
            logger.debug("Semantic similarity calculated successfully")
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {str(e)}")
            return jsonify({'error': f'Error calculating semantic similarity: {str(e)}'}), 500
        
        # Generate optimization suggestions
        try:
            suggestions = generate_optimization_suggestions(resume_text, job_description_text)
            logger.debug("Suggestions generated successfully")
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            return jsonify({'error': f'Error generating suggestions: {str(e)}'}), 500
        
        # Prepare detailed analysis results
        analysis_results = {
            'overall_score': match_scores['overall_score'],
            'category_scores': match_scores['category_scores'],
            'semantic_score': semantic_score,
            'resume_keywords': resume_keywords,
            'job_keywords': job_keywords,
            'suggestions': suggestions
        }
        
        logger.debug("Analysis completed successfully")
        return jsonify(analysis_results)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred during analysis'}), 500

if __name__ == '__main__':
    app.run(debug=True) 