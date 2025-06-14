# 🚀 Marketing Insights Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Ready-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)

**An AI-powered marketing insights generator that transforms company data into actionable strategies**

**Features • Quick Start • Architecture • API Reference • Deployment**

</div>

---

## 📋 Table of Contents
<details>
<summary>Click to expand</summary>

- Overview  
- Features  
- Architecture  
- Prerequisites  
- Installation  
  - Local Development  
  - Docker Setup  
- Configuration  
  - Environment Variables  
  - Company Configuration  
- Usage  
  - Web Interface  
  - API Endpoints  
- Deployment  
  - Google Cloud Run  
  - Docker Deployment  
- Development  
- API Reference  
- Troubleshooting  
- Contributing  
- License  

</details>

---

## 🌟 Overview
Marketing Insights Bot is a sophisticated Flask-based web application that leverages Google's Gemini AI to generate data-driven marketing recommendations. It analyzes company data from MySQL databases and provides actionable insights for strategic decision-making.

---

## 🎯 Key Benefits

- 🤖 **AI-Powered Analysis**: Utilizes Google Gemini 1.5 Pro for advanced insights  
- 🏢 **Multi-Company Support**: Manage multiple companies with isolated data  
- 💬 **Contextual Conversations**: Maintains conversation history for coherent interactions  
- 📊 **Real-Time Data Integration**: Connects directly to MySQL databases  
- 🎨 **Customizable Backgrounds**: Edit company contexts for tailored responses  
- ☁️ **Cloud-Native**: Optimized for Google Cloud Platform deployment  

---

## ✨ Features

<details><summary><b>🔍 Intelligent Marketing Analysis</b></summary>

- Data-driven recommendations  
- Market expansion strategies  
- Branding insights  
- Competitive positioning  

</details>

<details><summary><b>🏗️ Robust Architecture</b></summary>

- Modular design with separate managers  
- Error handling and recovery  
- Connection pooling  
- Async processing support  

</details>

<details><summary><b>🛡️ Enterprise Features</b></summary>

- Multi-tenant architecture  
- Session management  
- Data isolation  
- Audit trails  

</details>

<details><summary><b>🎨 Modern UI/UX</b></summary>

- Responsive design  
- Real-time typing animation  
- Dark/light themes  
- Mobile-friendly interface  

</details>

---

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Web Interface]
        API[REST API Client]
    end
    
    subgraph "Application Layer"
        Flask[Flask Server]
        CM[Company Manager]
        DM[Data Manager]
        BM[Background Manager]
        Conv[Conversation Manager]
    end
    
    subgraph "Data Layer"
        MySQL[(MySQL Database)]
        Cache[Session Cache]
    end
    
    subgraph "External Services"
        Gemini[Google Gemini AI]
    end
    
    UI --> Flask
    API --> Flask
    Flask --> CM
    CM --> DM
    CM --> BM
    CM --> Conv
    DM --> MySQL
    Flask --> Gemini
    Conv --> Cache
📋 Prerequisites
Python 3.10+

MySQL 8.0+

Google Cloud Account (for Gemini API)

Docker (optional, for containerization)

Node.js (for frontend development)

🚀 Installation
Local Development
<details><summary><b>Step 1: Clone the Repository</b></summary>
bash
Copy
Edit
git clone https://github.com/yourusername/marketing-insights-bot.git
cd marketing-insights-bot
</details> <details><summary><b>Step 2: Create Virtual Environment</b></summary>
bash
Copy
Edit
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
</details> <details><summary><b>Step 3: Install Dependencies</b></summary>
bash
Copy
Edit
pip install -r requirements.txt
</details> <details><summary><b>Step 4: Set Up Environment Variables</b></summary>
Create a .env file:

env
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key_here
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
INSTANCE_CONNECTION_NAME=project:region:instance

MYSQL_DB_COMPANY1=company1_db
MYSQL_DB_COMPANY2=company2_db
MYSQL_DB_COMPANY3=company3_db
MYSQL_DB_COMPANY4=company4_db

PORT=8080
FLASK_ENV=development
</details> <details><summary><b>Step 5: Initialize Database</b></summary>
sql
Copy
Edit
CREATE TABLE `company-background` (
    background_text TEXT
);

CREATE TABLE scans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scan_date DATETIME,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    location VARCHAR(100)
);
</details> <details><summary><b>Step 6: Run the Application</b></summary>
bash
Copy
Edit
python app.py
Visit http://localhost:8080

</details>
Docker Setup
<details><summary><b>Build and Run with Docker</b></summary>
bash
Copy
Edit
docker build -t marketing-insights-bot .

docker run -p 8080:8080 \
  --env-file .env \
  -v /path/to/cloudsql:/cloudsql \
  marketing-insights-bot
</details> <details><summary><b>Docker Compose Setup</b></summary>
docker-compose.yml:

yaml
Copy
Edit
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    env_file:
      - .env
    volumes:
      - cloudsql:/cloudsql
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: marketing_insights
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  cloudsql:
  mysql_data:
Run with:

bash
Copy
Edit
docker-compose up
</details>
⚙️ Configuration
<details><summary><b>Required Variables</b></summary>
Variable	Description	Example
GEMINI_API_KEY	Google Gemini API key	AIza...
MYSQL_USER	MySQL username	root
MYSQL_PASSWORD	MySQL password	password123
INSTANCE_CONNECTION_NAME	Cloud SQL instance	project:region:instance
MYSQL_DB_COMPANY[1-4]	Company database names	company1_db

</details> <details><summary><b>Optional Variables</b></summary>
Variable	Description	Default
PORT	Application port	8080
FLASK_ENV	Flask environment	production
MAX_WORKERS	Gunicorn workers	1
TIMEOUT	Request timeout	300

</details>
Company Configuration
<details><summary><b>Adding New Companies</b></summary>
Update app.py:

python
Copy
Edit
COMPANY_CONFIG = {
    'company5': {
        'name': 'Company Five',
        'db_env': 'MYSQL_DB_COMPANY5',
        'icon': '🏭'
    }
}
Add to .env:

env
Copy
Edit
MYSQL_DB_COMPANY5=company5_database
</details>
📱 Usage
<details><summary><b>Getting Started</b></summary>
Select Company: Choose from the landing page

Ask Questions: Enter queries in chat

View Insights: Get AI-generated suggestions

Manage Background: Click background icon to update company context

</details> <details><summary><b>Example Questions</b></summary>
"What are the top-performing products in Q4?"

"Suggest a marketing strategy for the Indian market"

"How can we improve brand visibility in urban areas?"

"Analyze customer demographics and suggest targeting strategies"

</details>
🔌 API Endpoints
<details><summary><b>Core Endpoints</b></summary>
Generate Insights

http
Copy
Edit
POST /ask
Content-Type: application/json

{
  "company_id": "company1",
  "prompt": "Analyze sales trends",
  "background": "Optional custom background"
}
Get Background

http
Copy
Edit
GET /get_background?company_id=company1
Update Background

http
Copy
Edit
POST /update_background
Content-Type: application/json

{
  "company_id": "company1",
  "background": "New background text"
}
</details>
🚢 Deployment
Google Cloud Run
<details><summary><b>Automated Deployment</b></summary>
bash
Copy
Edit
gcloud services enable run.googleapis.com \
  cloudbuild.googleapis.com \
  sqladmin.googleapis.com

gcloud builds submit --config cloudbuild.yaml

gcloud run services update marketing-insights-bot \
  --set-env-vars="GEMINI_API_KEY=your_key,MYSQL_USER=user" \
  --region=us-central1
</details> <details><summary><b>Manual Deployment</b></summary>
bash
Copy
Edit
gcloud builds submit --tag gcr.io/PROJECT_ID/marketing-insights-bot

gcloud run deploy marketing-insights-bot \
  --image gcr.io/PROJECT_ID/marketing-insights-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars-from-file=.env.yaml
</details>
Docker Deployment
<details><summary><b>Production Setup</b></summary>
bash
Copy
Edit
docker build -t marketing-insights-bot:prod --build-arg ENV=production .

docker run -d \
  --name marketing-bot \
  -p 80:8080 \
  --restart unless-stopped \
  -v /var/cloudsql:/cloudsql:ro \
  --env-file .env.prod \
  marketing-insights-bot:prod
</details>
🛠️ Development
Project Structure
cpp
Copy
Edit
marketing-insights-bot/
├── app.py
├── static/
│   ├── script.js
│   └── styles.css
├── templates/
│   ├── index.html
│   └── company-selector.html
├── Dockerfile
├── cloudbuild.yaml
├── requirements.txt
├── .env.example
└── README.md
<details><summary><b>Custom Managers</b></summary>
python
Copy
Edit
class CustomManager:
    def __init__(self, company_manager):
        self.company_manager = company_manager
        
    def custom_operation(self):
        # Your logic here
        pass
Register in CompanyDataManager:

python
Copy
Edit
self.custom_manager = CustomManager(self)
</details> <details><summary><b>New API Endpoints</b></summary>
python
Copy
Edit
@app.route('/custom_endpoint', methods=['POST'])
def custom_endpoint():
    try:
        # Custom logic
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
</details>
📚 API Reference
<details><summary><b>Complete API Documentation</b></summary>
Authentication: Not yet implemented — use JWT or OAuth2 in production.
Rate Limiting: None yet — consider Flask-Limiter.
Response Format:

json
Copy
Edit
{
  "data": {},
  "error": null,
  "metadata": {
    "timestamp": "2024-01-01T00:00:00Z",
    "version": "1.0"
  }
}
Error Codes:

400: Bad Request

404: Not Found

500: Internal Server Error

</details>
🔧 Troubleshooting
<details><summary><b>Common Issues</b></summary>
Database Connection Failed

Check MySQL credentials

Verify Cloud SQL proxy

Ensure DB exists

Gemini API Errors

Check API key validity

Verify quota

Review payload size

Docker Issues

Ensure Docker daemon is active

Check port availability

Verify volume mounts

</details> <details><summary><b>Debug Mode</b></summary>
python
Copy
Edit
import logging
logging.basicConfig(level=logging.DEBUG)
Test endpoint:

bash
Copy
Edit
curl http://localhost:8080/test?company_id=company1
</details>
🤝 Contributing
We welcome contributions!
Steps:

Fork the repo

Create a feature branch: git checkout -b feature/AmazingFeature

Commit your changes

Push the branch

Open a Pull Request

Style Guide:

Follow PEP 8

Add docstrings

Write unit tests

📄 License
This project is licensed under the MIT License – see the LICENSE file.

<div align="center">
Built with ❤️ by the Marketing Insights Team
Report Bug • Request Feature

</div> ```
Let me know if you'd like this saved as a README.md file or want help pushing it to GitHub.
