"""
Modern Web Interface for Semantic Data Integration Framework
A futuristic UI for querying and exploring integrated RDF data
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# Fuseki SPARQL endpoint (adjust if needed)
# Can be set via environment variable for deployment
FUSEKI_ENDPOINT = os.getenv('FUSEKI_ENDPOINT', 'http://localhost:3030/university/query')

@app.route('/')
def index():
    """Main page with futuristic interface"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def execute_query():
    """Execute SPARQL query via Fuseki endpoint"""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Send query to Fuseki
        response = requests.post(
            FUSEKI_ENDPOINT,
            data={'query': query},
            headers={'Accept': 'application/sparql-results+json'},
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            return jsonify({
                'success': True,
                'data': results,
                'results': format_sparql_results(results)
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Fuseki error: {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': f'Cannot connect to Fuseki at {FUSEKI_ENDPOINT}. Please ensure Fuseki is running and accessible. For deployment, set the FUSEKI_ENDPOINT environment variable to your Fuseki service URL.',
            'help': 'To set up Fuseki: 1) Deploy Fuseki as a separate service on Render, 2) Set FUSEKI_ENDPOINT environment variable to your Fuseki URL, or 3) Use a public SPARQL endpoint.'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if Fuseki endpoint is accessible"""
    try:
        # Simple query to test connection
        response = requests.get(
            FUSEKI_ENDPOINT.replace('/query', ''),
            timeout=5
        )
        return jsonify({
            'status': 'connected' if response.status_code < 500 else 'error',
            'endpoint': FUSEKI_ENDPOINT
        })
    except:
        return jsonify({
            'status': 'disconnected',
            'endpoint': FUSEKI_ENDPOINT,
            'message': 'Fuseki endpoint is not accessible'
        }), 503

def format_sparql_results(sparql_json):
    """Format SPARQL JSON results for display"""
    if 'results' not in sparql_json:
        return []
    
    bindings = sparql_json['results'].get('bindings', [])
    if not bindings:
        return []
    
    # Get variable names from first binding
    variables = list(bindings[0].keys()) if bindings else []
    
    # Format results
    formatted = []
    for binding in bindings:
        row = {}
        for var in variables:
            if var in binding:
                value = binding[var]
                row[var] = value.get('value', '')
                if value.get('type') == 'uri':
                    # Extract local name from URI
                    uri = row[var]
                    if '#' in uri:
                        row[var] = uri.split('#')[-1]
                    elif '/' in uri:
                        row[var] = uri.split('/')[-1]
        formatted.append(row)
    
    return {
        'variables': variables,
        'rows': formatted,
        'count': len(formatted)
    }

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Return example SPARQL queries"""
    examples = [
        {
            'name': 'Student Enrollments',
            'description': 'Get all student enrollments with course details',
            'query': '''PREFIX uni: <http://example.org/university#>
SELECT ?student ?courseTitle ?semester ?year
WHERE {
  ?student uni:hasEnrollment ?enrollment .
  ?enrollment uni:enrolledInCourse ?course ;
              uni:semester ?semester ;
              uni:year ?year .
  ?course uni:courseTitle ?courseTitle .
}'''
        },
        {
            'name': 'Students with Contact Info',
            'description': 'Retrieve student information from SQLite and CSV',
            'query': '''PREFIX uni: <http://example.org/university#>
SELECT ?student ?firstName ?lastName ?email ?phone ?major
WHERE {
  ?student uni:firstName ?firstName ;
           uni:lastName ?lastName ;
           uni:email ?email ;
           uni:phone ?phone ;
           uni:major ?major .
}'''
        },
        {
            'name': 'Courses by Department',
            'description': 'Get courses organized by department from XML',
            'query': '''PREFIX uni: <http://example.org/university#>
SELECT ?courseCode ?courseTitle ?deptName ?credits
WHERE {
  ?course uni:courseCode ?courseCode ;
          uni:courseTitle ?courseTitle ;
          uni:credits ?credits ;
          uni:offeredByDepartment ?dept .
  ?dept uni:departmentName ?deptName .
}
ORDER BY ?deptName ?courseCode'''
        },
        {
            'name': 'Cross-Source Integration',
            'description': 'Unified query across all three sources',
            'query': '''PREFIX uni: <http://example.org/university#>
SELECT ?studentName ?email ?courseTitle ?deptName ?semester ?year
WHERE {
  ?student uni:firstName ?first ;
           uni:lastName ?last ;
           uni:email ?email .
  BIND(CONCAT(?first, " ", ?last) AS ?studentName)
  ?student uni:hasEnrollment ?enrollment .
  ?enrollment uni:enrolledInCourse ?course ;
              uni:semester ?semester ;
              uni:year ?year .
  ?course uni:courseTitle ?courseTitle ;
          uni:offeredByDepartment ?dept .
  ?dept uni:departmentName ?deptName .
}
ORDER BY ?studentName ?semester'''
        }
    ]
    return jsonify(examples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

