# Deployment Guide

## GitHub Setup

### 1. Initialize Git Repository (if not already done)

```bash
git init
```

### 2. Add Files to Git

Only key source files will be committed (excluded files are in `.gitignore`):

```bash
git add .gitignore
git add README.md
git add requirements.txt
git add app.py
git add university.owl
git add sqlite_to_rdf.py
git add csv_to_rdf.py
git add xml_to_rdf.py
git add setup_university.sql
git add student_contacts.csv
git add course_catalog.xml
git add source_to_ontology_mapping.md
git add templates/
git add static/
git add render.yaml
git add Procfile
```

### 3. Commit and Push

```bash
git commit -m "Initial commit: Semantic Data Integration Framework"
git branch -M main
git remote add origin https://github.com/EvansOdhams/Semantic-Data-Integration-Framework-for-Multi-Source-Data.git
git push -u origin main
```

## Render Deployment

### Prerequisites

1. GitHub repository pushed (see above)
2. Render account (sign up at https://render.com)

### Steps

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Connect your GitHub account
   - Select repository: `Semantic-Data-Integration-Framework-for-Multi-Source-Data`

3. **Configure Service**
   - **Name**: `semantic-integration-framework`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free tier is fine for demo

4. **Environment Variables** (Optional)
   - `FUSEKI_ENDPOINT`: Your Fuseki endpoint (if using external Fuseki)
   - Note: For local Fuseki, you'll need to deploy Fuseki separately or use a cloud SPARQL endpoint

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your app will be available at: `https://semantic-integration-framework.onrender.com`

### Important Notes

- **Fuseki Dependency**: The web app requires Fuseki to be running. Options:
  1. Deploy Fuseki separately on Render (as another service)
  2. Use a cloud SPARQL endpoint (e.g., GraphDB Cloud, Stardog Cloud)
  3. Modify `app.py` to use a different SPARQL endpoint

- **Free Tier Limitations**: 
  - Services spin down after 15 minutes of inactivity
  - First request after spin-down may take 30-60 seconds

- **Database**: The SQLite database (`university.db`) is not included in the repo (it's in `.gitignore`). You'll need to regenerate it or use a persistent database service.

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit http://localhost:5000
```

Make sure Fuseki is running on `localhost:3030` for the app to work properly.

