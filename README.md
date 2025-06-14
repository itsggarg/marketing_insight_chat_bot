# 🚀 Marketing Insights Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Ready-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)

**An AI-powered marketing insights generator that transforms company data into actionable strategies**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Reference](#-api-reference) • [Deployment](#-deployment)

</div>

---

## 📋 Table of Contents

<details>
<summary>Click to expand</summary>

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Local Development](#local-development)
  - [Docker Setup](#docker-setup)
- [Configuration](#-configuration)
  - [Environment Variables](#environment-variables)
  - [Company Configuration](#company-configuration)
- [Usage](#-usage)
  - [Web Interface](#web-interface)
  - [API Endpoints](#api-endpoints)
- [Deployment](#-deployment)
  - [Google Cloud Run](#google-cloud-run)
  - [Docker Deployment](#docker-deployment)
- [Development](#-development)
  - [Project Structure](#project-structure)
  - [Adding New Companies](#adding-new-companies)
  - [Customization](#customization)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

</details>

## 🌟 Overview

Marketing Insights Bot is a sophisticated Flask-based web application that leverages Google's Gemini AI to generate data-driven marketing recommendations. It analyzes company data from MySQL databases and provides actionable insights for strategic decision-making.

### 🎯 Key Benefits

- **🤖 AI-Powered Analysis**: Utilizes Google Gemini 1.5 Pro for advanced insights
- **🏢 Multi-Company Support**: Manage multiple companies with isolated data
- **💬 Contextual Conversations**: Maintains conversation history for coherent interactions
- **📊 Real-Time Data Integration**: Connects directly to MySQL databases
- **🎨 Customizable Backgrounds**: Edit company contexts for tailored responses
- **☁️ Cloud-Native**: Optimized for Google Cloud Platform deployment

## ✨ Features

<details>
<summary><b>🔍 Intelligent Marketing Analysis</b></summary>

- Data-driven recommendations
- Market expansion strategies
- Branding insights
- Competitive positioning

</details>

<details>
<summary><b>🏗️ Robust Architecture</b></summary>

- Modular design with separate managers
- Error handling and recovery
- Connection pooling
- Async processing support

</details>

<details>
<summary><b>🛡️ Enterprise Features</b></summary>

- Multi-tenant architecture
- Session management
- Data isolation
- Audit trails

</details>

<details>
<summary><b>🎨 Modern UI/UX</b></summary>

- Responsive design
- Real-time typing animation
- Dark/light themes
- Mobile-friendly interface

</details>

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

## 📋 Prerequisites

- **Python 3.10+**
- **MySQL 8.0+**
- **Google Cloud Account** (for Gemini API)
- **Docker** (optional, for containerization)
- **Node.js** (for frontend development)

## 🚀 Installation

### Local Development

<details>
<summary><b>Step 1: Clone the Repository</b></summary>

```bash
git clone https://github.com/yourusername/marketing-insights-bot.git
cd marketing-insights-bot
</details><details> <summary><b>Step 2: Create Virtual Environment</b></summary>
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
</details><details> <summary><b>Step 3: Install Dependencies</b></summary>
pip install -r requirements.txt
</details><details> <summary><b>Step 4: Set Up Environment Variables</b></summary>
Create a .env file in the project root:

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# MySQL Configuration
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
INSTANCE_CONNECTION_NAME=project:region:instance

# Company Databases
MYSQL_DB_COMPANY1=company1_db
MYSQL_DB_COMPANY2=company2_db
MYSQL_DB_COMPANY3=company3_db
MYSQL_DB_COMPANY4=company4_db

# Application Settings
PORT=8080
FLASK_ENV=development
</details><details> <summary><b>Step 5: Initialize Database</b></summary>
-- Create company background table
CREATE TABLE `company-background` (
    background_text TEXT
);

-- Create scans table
CREATE TABLE scans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scan_date DATETIME,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    location VARCHAR(100),
    -- Add more columns as needed
);
</details><details> <summary><b>Step 6: Run the Application</b></summary>
python app.py
Visit http://localhost:8080 in your browser.

</details>
Docker Setup
<details> <summary><b>Build and Run with Docker</b></summary>
# Build the image
docker build -t marketing-insights-bot .

# Run the container
docker run -p 8080:8080 \
  --env-file .env \
  -v /path/to/cloudsql:/cloudsql \
  marketing-insights-bot
</details><details> <summary><b>Docker Compose Setup</b></summary>
Create docker-compose.yml:

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

docker-compose up
</details>
⚙️ Configuration
Environment Variables
<details> <summary><b>Required Variables</b></summary>
Variable	Description	Example
GEMINI_API_KEY	Google Gemini API key	AIza...
MYSQL_USER	MySQL username	root
MYSQL_PASSWORD	MySQL password	password123
INSTANCE_CONNECTION_NAME	Cloud SQL instance	project:region:instance
MYSQL_DB_COMPANY[1-4]	Company database names	company1_db
</details><details> <summary><b>Optional Variables</b></summary>
Variable	Description	Default
PORT	Application port	8080
FLASK_ENV	Flask environment	production
MAX_WORKERS	Gunicorn workers	1
TIMEOUT	Request timeout	300
</details>
Company Configuration
<details> <summary><b>Adding New Companies</b></summary>
Edit app.py to add new companies:

COMPANY_CONFIG = {
    'company5': {
        'name': 'Company Five',
        'db_env': 'MYSQL_DB_COMPANY5',
        'icon': '🏭'
    }
}
Then add the corresponding environment variable:

MYSQL_DB_COMPANY5=company5_database
</details>
📱 Usage
Web Interface
<details> <summary><b>Getting Started</b></summary>
Select Company: Choose from available companies on the landing page
Ask Questions: Type marketing-related questions in the chat interface
View Insights: Receive AI-generated recommendations based on your data
Manage Background: Click the background button to edit company context
</details><details> <summary><b>Example Questions</b></summary>
"What are the top-performing products in Q4?"
"Suggest a marketing strategy for the Indian market"
"How can we improve brand visibility in urban areas?"
"Analyze customer demographics and suggest targeting strategies"
</details>
API Endpoints
<details> <summary><b>Core Endpoints</b></summary>
Generate Insights
POST /ask
Content-Type: application/json

{
  "company_id": "company1",
  "prompt": "Analyze sales trends",
  "background": "Optional custom background"
}
Get Background
GET /get_background?company_id=company1
Update Background
POST /update_background
Content-Type: application/json

{
  "company_id": "company1",
  "background": "New background text"
}
</details>
🚢 Deployment
Google Cloud Run
<details> <summary><b>Automated Deployment</b></summary>
Enable APIs:
gcloud services enable run.googleapis.com \
  cloudbuild.googleapis.com \
  sqladmin.googleapis.com
Configure Cloud Build:
gcloud builds submit --config cloudbuild.yaml
Set Environment Variables:
gcloud run services update marketing-insights-bot \
  --set-env-vars="GEMINI_API_KEY=your_key" \
  --set-env-vars="MYSQL_USER=user" \
  --region=us-central1
</details><details> <summary><b>Manual Deployment</b></summary>
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/marketing-insights-bot

# Deploy to Cloud Run
gcloud run deploy marketing-insights-bot \
  --image gcr.io/PROJECT_ID/marketing-insights-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars-from-file=.env.yaml
</details>
Docker Deployment
<details> <summary><b>Production Setup</b></summary>
# Build production image
docker build -t marketing-insights-bot:prod \
  --build-arg ENV=production .

# Run with volume mounts
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
marketing-insights-bot/
├── app.py                 # Main Flask application
├── static/
│   ├── script.js         # Frontend JavaScript
│   └── styles.css        # CSS styles
├── templates/
│   ├── index.html        # Main chat interface
│   └── company-selector.html  # Company selection page
├── Dockerfile            # Container configuration
├── cloudbuild.yaml       # Cloud Build configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
Adding New Features
<details> <summary><b>Custom Managers</b></summary>
Create a new manager class:

class CustomManager:
    def __init__(self, company_manager):
        self.company_manager = company_manager
        
    def custom_operation(self):
        # Your custom logic here
        pass
Register in CompanyDataManager:

self.custom_manager = CustomManager(self)
</details><details> <summary><b>New API Endpoints</b></summary>
@app.route('/custom_endpoint', methods=['POST'])
def custom_endpoint():
    try:
        # Your endpoint logic
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
</details>
📚 API Reference
<details> <summary><b>Complete API Documentation</b></summary>
Authentication
Currently, the API doesn't require authentication. For production, implement JWT or OAuth2.

Rate Limiting
No rate limiting is implemented. Consider adding Flask-Limiter for production.

Response Format
All responses follow this structure:

{
  "data": {},
  "error": null,
  "metadata": {
    "timestamp": "2024-01-01T00:00:00Z",
    "version": "1.0"
  }
}
Error Codes
400: Bad Request
404: Not Found
500: Internal Server Error
</details>
🔧 Troubleshooting
<details> <summary><b>Common Issues</b></summary>
Database Connection Failed
Check MySQL credentials
Verify Cloud SQL proxy is running
Ensure database exists
Gemini API Errors
Verify API key is valid
Check quota limits
Review request size
Docker Issues
Ensure Docker daemon is running
Check port availability
Verify volume mounts
</details><details> <summary><b>Debug Mode</b></summary>
Enable debug logging:

import logging
logging.basicConfig(level=logging.DEBUG)
Test endpoints:

curl http://localhost:8080/test?company_id=company1
</details>
🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)
Open a Pull Request
Code Style
Follow PEP 8
Add docstrings to functions
Write unit tests for new features
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center">
Built with ❤️ by the Marketing Insights Team

Report Bug • Request Feature

</div> ```
