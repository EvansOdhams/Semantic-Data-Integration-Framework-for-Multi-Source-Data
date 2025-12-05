# Semantic Data Integration Framework for Multi-Source Data

A semantic integration solution that unifies data from multiple heterogeneous sources (SQLite database, CSV file, and XML file) into a unified RDF knowledge graph, enabling seamless cross-source querying through SPARQL.

## 🚀 Features

- **Multi-Source Integration**: Unifies data from SQLite, CSV, and XML formats
- **Semantic Ontology**: Domain ontology designed in Protégé (OWL)
- **RDF Conversion**: Automated Python scripts for transforming source data to RDF/Turtle
- **SPARQL Querying**: Query integrated data through Apache Jena Fuseki
- **Modern Web Interface**: Interactive web UI for exploring and querying the integrated data

## 📁 Project Structure

```
├── university.owl              # Domain ontology (OWL)
├── sqlite_to_rdf.py           # SQLite → RDF converter
├── csv_to_rdf.py              # CSV → RDF converter
├── xml_to_rdf.py              # XML → RDF converter
├── setup_university.sql        # SQLite database schema and sample data
├── student_contacts.csv        # CSV source file
├── course_catalog.xml         # XML source file
├── source_to_ontology_mapping.md  # Mapping documentation
├── app.py                      # Web application (Flask)
├── templates/                  # Web UI templates
├── static/                     # CSS, JS, assets
└── requirements.txt           # Python dependencies
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Apache Jena Fuseki (for SPARQL endpoint)
- SQLite3

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/EvansOdhams/Semantic-Data-Integration-Framework-for-Multi-Source-Data.git
   cd Semantic-Data-Integration-Framework-for-Multi-Source-Data
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create the SQLite database**
   ```bash
   sqlite3 university.db < setup_university.sql
   ```

4. **Generate RDF files**
   ```bash
   python sqlite_to_rdf.py --db university.db --output data/sqlite_dump.ttl
   python csv_to_rdf.py --csv student_contacts.csv --output data/csv_dump.ttl
   python xml_to_rdf.py --xml course_catalog.xml --output data/xml_dump.ttl
   ```

5. **Start Apache Jena Fuseki** (in a separate terminal)
   ```bash
   cd /path/to/apache-jena-fuseki
   ./fuseki-server
   ```
   Then upload the three `.ttl` files to a dataset named `university` via the web UI at `http://localhost:3030`

6. **Run the web application**
   ```bash
   python app.py
   ```
   Access the interface at `http://localhost:5000`

## 📊 Data Sources

### 1. SQLite Database (`university.db`)
- **Tables**: Students, Courses, Enrollments
- **Schema**: Normalized relational structure with foreign keys
- **Sample Data**: 3 students, 3 courses, 5 enrollments

### 2. CSV File (`student_contacts.csv`)
- **Columns**: student_id, full_name, email, phone, country
- **Purpose**: Student contact information (partially overlaps with SQLite)

### 3. XML File (`course_catalog.xml`)
- **Structure**: Hierarchical course catalog with departments and courses
- **Purpose**: Rich course metadata with department information

## 🎯 Ontology

The domain ontology (`university.owl`) includes:

- **Classes**: Student, Course, Department, Enrollment
- **Object Properties**: hasEnrollment, enrolledInCourse, offeredByDepartment
- **Data Properties**: firstName, lastName, email, phone, courseCode, courseTitle, credits, etc.

## 🔍 Usage

### Command Line

Convert individual sources:
```bash
python sqlite_to_rdf.py --db university.db --output data/sqlite_dump.ttl
python csv_to_rdf.py --csv student_contacts.csv --output data/csv_dump.ttl
python xml_to_rdf.py --xml course_catalog.xml --output data/xml_dump.ttl
```

### Web Interface

1. Start the Flask app: `python app.py`
2. Open `http://localhost:5000` in your browser
3. Use the interactive query interface to explore the integrated data

### SPARQL Queries

Example query to get all student enrollments:
```sparql
PREFIX uni: <http://example.org/university#>
SELECT ?student ?courseTitle ?semester ?year
WHERE {
  ?student uni:hasEnrollment ?enrollment .
  ?enrollment uni:enrolledInCourse ?course ;
              uni:semester ?semester ;
              uni:year ?year .
  ?course uni:courseTitle ?courseTitle .
}
```

## 🌐 Deployment on Render

The web application is configured for deployment on Render. See `render.yaml` for configuration.

## 📝 License

This project is part of an academic assignment for CSC 802 - Systems and Data Integration.

## 👤 Author

Evans Odhams

## 🔗 Links

- [GitHub Repository](https://github.com/EvansOdhams/Semantic-Data-Integration-Framework-for-Multi-Source-Data)
- [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/)
- [Protégé](https://protege.stanford.edu/)

