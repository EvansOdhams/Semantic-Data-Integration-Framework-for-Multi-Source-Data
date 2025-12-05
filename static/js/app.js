// Semantic Integration Framework - Frontend JavaScript

const queryEditor = document.getElementById('queryEditor');
const executeBtn = document.getElementById('executeBtn');
const clearBtn = document.getElementById('clearBtn');
const formatBtn = document.getElementById('formatBtn');
const examplesBtn = document.getElementById('examplesBtn');
const resultsContainer = document.getElementById('resultsContainer');
const resultCount = document.getElementById('resultCount');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorToast = document.getElementById('errorToast');
const toastMessage = document.getElementById('toastMessage');
const examplesModal = document.getElementById('examplesModal');
const closeModal = document.getElementById('closeModal');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadExamples();
    checkConnection();
    
    // Set default query
    queryEditor.value = `PREFIX uni: <http://example.org/university#>
SELECT ?student ?courseTitle ?semester ?year
WHERE {
  ?student uni:hasEnrollment ?enrollment .
  ?enrollment uni:enrolledInCourse ?course ;
              uni:semester ?semester ;
              uni:year ?year .
  ?course uni:courseTitle ?courseTitle .
}`;
});

// Execute Query
executeBtn.addEventListener('click', executeQuery);
queryEditor.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        executeQuery();
    }
});

async function executeQuery() {
    const query = queryEditor.value.trim();
    
    if (!query) {
        showToast('Please enter a SPARQL query');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.results);
            updateStatus(true);
        } else {
            showToast(data.error || 'Query execution failed');
            displayError(data.error);
            updateStatus(false);
        }
    } catch (error) {
        showToast('Failed to connect to server');
        displayError(error.message);
        updateStatus(false);
    } finally {
        showLoading(false);
    }
}

function displayResults(results) {
    if (!results || !results.rows || results.rows.length === 0) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <h3>No Results</h3>
                <p>The query executed successfully but returned no results</p>
            </div>
        `;
        resultCount.textContent = '0 results';
        return;
    }
    
    const variables = results.variables;
    const rows = results.rows;
    
    let tableHTML = '<table class="results-table"><thead><tr>';
    variables.forEach(variable => {
        tableHTML += `<th>${variable}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';
    
    rows.forEach(row => {
        tableHTML += '<tr>';
        variables.forEach(variable => {
            const value = row[variable] || '';
            tableHTML += `<td>${escapeHtml(value)}</td>`;
        });
        tableHTML += '</tr>';
    });
    
    tableHTML += '</tbody></table>';
    resultsContainer.innerHTML = tableHTML;
    resultCount.textContent = `${rows.length} result${rows.length !== 1 ? 's' : ''}`;
}

function displayError(error) {
    resultsContainer.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">⚠️</div>
            <h3>Error</h3>
            <p style="color: var(--error);">${escapeHtml(error)}</p>
        </div>
    `;
    resultCount.textContent = 'Error';
}

// Clear Query
clearBtn.addEventListener('click', () => {
    queryEditor.value = '';
    queryEditor.focus();
});

// Format Query (simple indentation)
formatBtn.addEventListener('click', () => {
    const query = queryEditor.value;
    // Simple formatting - add line breaks after keywords
    const formatted = query
        .replace(/\b(SELECT|WHERE|PREFIX|OPTIONAL|FILTER|ORDER BY|GROUP BY)\b/gi, '\n$1')
        .replace(/\{/g, ' {\n    ')
        .replace(/\}/g, '\n}')
        .replace(/;\s+/g, ';\n    ')
        .replace(/\.\s+/g, '.\n    ')
        .replace(/\n\s+\n/g, '\n')
        .trim();
    
    queryEditor.value = formatted;
});

// Examples Modal
examplesBtn.addEventListener('click', () => {
    examplesModal.classList.add('active');
});

closeModal.addEventListener('click', () => {
    examplesModal.classList.remove('active');
});

examplesModal.addEventListener('click', (e) => {
    if (e.target === examplesModal) {
        examplesModal.classList.remove('active');
    }
});

async function loadExamples() {
    try {
        const response = await fetch('/api/examples');
        const examples = await response.json();
        
        const examplesList = document.getElementById('examplesList');
        examplesList.innerHTML = examples.map(example => `
            <div class="example-item" onclick="loadExample('${escapeForJS(example.query)}')">
                <h4>${escapeHtml(example.name)}</h4>
                <p>${escapeHtml(example.description)}</p>
                <div class="example-query">${escapeHtml(example.query.substring(0, 150))}...</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load examples:', error);
    }
}

function loadExample(query) {
    queryEditor.value = query;
    examplesModal.classList.remove('active');
    queryEditor.focus();
}

// Connection Status
async function checkConnection() {
    try {
        const response = await fetch('/api/examples');
        if (response.ok) {
            updateStatus(true);
        } else {
            updateStatus(false);
        }
    } catch (error) {
        updateStatus(false);
    }
}

function updateStatus(connected) {
    if (connected) {
        statusDot.classList.add('connected');
        statusText.textContent = 'Connected';
    } else {
        statusDot.classList.remove('connected');
        statusText.textContent = 'Disconnected';
    }
}

// Loading Overlay
function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add('active');
    } else {
        loadingOverlay.classList.remove('active');
    }
}

// Toast Notification
function showToast(message) {
    toastMessage.textContent = message;
    errorToast.classList.add('show');
    
    setTimeout(() => {
        errorToast.classList.remove('show');
    }, 5000);
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeForJS(text) {
    return text.replace(/'/g, "\\'").replace(/\n/g, '\\n');
}

