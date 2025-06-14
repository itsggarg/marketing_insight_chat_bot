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
