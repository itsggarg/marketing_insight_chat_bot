# 🚀 Marketing Insights Bot

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3.3-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/Google%20Gemini-AI-red.svg" alt="Gemini">
  <img src="https://img.shields.io/badge/MySQL-8.0+-orange.svg" alt="MySQL">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

<div align="center">
  <h3>🤖 AI-Powered Marketing Intelligence Platform</h3>
  <p>Transform your business data into actionable marketing insights using Google's Gemini AI</p>
  <p>
    <a href="#-features">Features</a> •
    <a href="#-demo">Demo</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-documentation">Documentation</a> •
    <a href="#-contributing">Contributing</a>
  </p>
</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
  - [Cloud Deployment](#cloud-deployment)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## 🌟 Overview

The **Marketing Insights Bot** is an enterprise-grade web application that leverages Google's Gemini AI to analyze company data and generate strategic marketing recommendations. Built with scalability and user experience in mind, it provides real-time insights for multiple companies through an intuitive chat interface.

### 🎯 Key Benefits

- **Data-Driven Decisions**: Transform raw data into actionable marketing strategies.
- **Multi-Company Support**: Manage insights for multiple businesses from one platform.
- **AI-Powered Analysis**: Leverage Google's latest Gemini AI for intelligent recommendations.
- **Real-Time Insights**: Get instant answers to your marketing questions.
- **Customizable Context**: Tailor AI responses with company-specific backgrounds.

## ✨ Features

<details>
<summary><b>🤖 AI-Powered Intelligence</b></summary>

- Integration with Google Gemini 1.5 Pro
- Context-aware responses based on company data
- Marketing strategy recommendations
- Customer behavior analysis
- Market expansion insights
</details>

<details>
<summary><b>💼 Multi-Company Management</b></summary>

- Support for multiple companies with isolated data
- Company-specific backgrounds and contexts
- Easy switching between different businesses
- Customizable company profiles
</details>

<details>
<summary><b>💬 Smart Conversation Management</b></summary>

- Conversation history with context retention
- Relevant history retrieval for better responses
- Export conversation capabilities
- Clear history functionality
</details>

<details>
<summary><b>📊 Data Integration</b></summary>

- MySQL database connectivity
- Real-time data analysis
- Support for large datasets (5000+ records)
- Automatic data sampling for performance
</details>

<details>
<summary><b>🎨 Modern User Interface</b></summary>

- Responsive design for all devices
- Real-time typing animations
- Loading states and error handling
- Clean, professional aesthetics
</details>

<details>
<summary><b>🔒 Security & Performance</b></summary>

- Environment-based configuration
- Secure API key management
- Optimized for production deployment
- Rate limiting and error handling
</details>

## 🎥 Demo

<div align="center">
  <img src="https://via.placeholder.com/800x400/667eea/ffffff?text=Marketing+Insights+Bot+Demo" alt="Demo Screenshot">
</div>

### 🖥️ Live Demo

> **Note**: A live demo is coming soon! For now, please follow the installation guide to run the application locally.

### 📸 Screenshots

<details>
<summary>View Screenshots</summary>

#### Company Selection
<img src="https://via.placeholder.com/600x400/667eea/ffffff?text=Company+Selection" alt="Company Selection">

#### Chat Interface
<img src="https://via.placeholder.com/600x400/764ba2/ffffff?text=Chat+Interface" alt="Chat Interface">

#### Background Editor
<img src="https://via.placeholder.com/600x400/667eea/ffffff?text=Background+Editor" alt="Background Editor">

</details>

## 🏗️ Architecture

```mermaid
graph TB
    A[Client Browser] -->|HTTPS| B[Flask Web Server]
    B --> C{Application Logic}
    C --> D[Company Manager]
    C --> E[Conversation Manager]
    C --> F[Data Manager]
    F -->|SQL| G[MySQL Database]
    C -->|API Call| H[Google Gemini AI]
    
    subgraph "Backend (Python/Flask)"
        B
        C
        D
        E
        F
    end

    style A fill:#e0f2fe,stroke:#0ea5e9,stroke-width:2px
    style G fill:#fef9c3,stroke:#eab308,stroke-width:2px
    style H fill:#fce7f3,stroke:#ec4899,stroke-width:2px
