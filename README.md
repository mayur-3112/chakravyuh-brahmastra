# 🔱 Chakravyuh-Brahmastra

**AI-Powered Cyber Defense Framework**

An indigenous cybersecurity platform developed at Sir MVIT for proactive threat detection and response.

## 🚀 Features

- **Surya Scanner**: Network reconnaissance and vulnerability scanning
- **RESTful API**: FastAPI-based async architecture
- **Real-time Dashboard**: Live scan monitoring and results
- **Modular Design**: Extensible plugin architecture

## 📋 Prerequisites

- Python 3.11+
- Nmap
- Linux/Kali (recommended)

## 🔧 Installation

Clone repository
git clone https://github.com/mayur3112/chakravyuh-brahmastra.git
cd chakravyuh-brahmastra

Create virtual environment
python3 -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

text

## 🎯 Quick Start

Start the API server
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

Access dashboard
open http://localhost:8000/dashboard

API documentation
open http://localhost:8000/docs

text

## 📁 Project Structure

sentinel-recon/
├── api/ # FastAPI application
│ ├── routes/ # API endpoints
│ └── templates/ # Dashboard UI
├── surya/ # Scanner module
├── brahmastra/ # Response engine (WIP)
├── config/ # Configuration
├── common/ # Shared utilities
└── tests/ # Test suite

text

## 🧪 Testing

Run a test scan
curl -X POST "http://localhost:8000/api/v1/scan/start"
-H "Content-Type: application/json"
-d '{"target": "127.0.0.1", "ports": "1-1000", "scan_type": "tcp_connect"}'

text

## 📊 Status

- ✅ Part 1: Surya Scanner Module
- ✅ Part 2: API & Dashboard
- ⏳ Part 3: Brahmastra Response Engine
- ⏳ Part 4: AI Threat Analysis

## 👥 Team

**Project Chakravyuh**  
Sir M. Visvesvaraya Institute of Technology  
Bangalore, India

## 📄 License

[Choose appropriate license]

## 🔒 Security

For security concerns, please contact: mayur311agarwal@gmail.com

---

**Built with ❤️ for India's Cyber Defense**
