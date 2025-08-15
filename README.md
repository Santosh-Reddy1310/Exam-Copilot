# Exam Copilot

> An intelligent AI-powered study companion that transforms your exam preparation through automated paper analysis, personalized study planning, and on-demand concept explanations.

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://exam-copilot.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Live Demo

Experience Exam Copilot in action: **[Launch Application](https://exam-copilot.streamlit.app/)**

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [Project Architecture](#project-architecture)
- [API Configuration](#api-configuration)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)
- [Support](#support)

## 🎯 Overview

Exam Copilot leverages advanced AI technology to revolutionize exam preparation by providing three core functionalities:

1. **Intelligent Paper Analysis** - Automatically extracts and prioritizes key topics from multiple PDF exam papers
2. **Adaptive Study Planning** - Generates personalized daily study timetables based on your constraints and goals
3. **Contextual Learning Assistant** - Provides concept explanations tailored to your learning level

Built with modern web technologies and powered by Google's Gemini 1.5 Flash AI model, Exam Copilot offers a seamless, dark-themed user experience designed for focused study sessions.

## ✨ Key Features

### 📊 Paper Analysis Engine
- **Multi-PDF Processing**: Upload and analyze multiple exam papers simultaneously
- **Topic Extraction**: AI-powered identification of the most relevant topics
- **Importance Weighting**: Quantified importance scores (%) for strategic focus
- **Interactive Tables**: Sortable, filterable topic overview with detailed summaries

### 📅 Smart Study Planner
- **Personalized Scheduling**: Custom daily timetables based on your availability
- **Time Slot Management**: Organized into Morning, Afternoon, and Evening sessions
- **Balanced Learning**: Automatic inclusion of breaks and realistic study loads
- **Flexible Configuration**: Adaptable to various study constraints and preferences

### 🤖 Clarity Bot
- **Multi-Level Explanations**: Concept explanations for Beginner, Intermediate, Advanced, and Expert levels
- **Instant Clarification**: Real-time responses to concept queries
- **Learning Path Optimization**: Adaptive explanations based on your current understanding

### 🎨 User Experience
- **Modern Dark Theme**: Eye-friendly interface optimized for extended study sessions
- **Responsive Design**: Seamless experience across desktop and mobile devices
- **Intuitive Navigation**: Clean, professional UI with logical information architecture

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend & Backend** | Python, Streamlit | Full-stack web application framework |
| **AI Engine** | Google Gemini 1.5 Flash | Natural language processing and generation |
| **PDF Processing** | PyPDF2 | Document parsing and text extraction |
| **Environment Management** | python-dotenv | Secure configuration management |
| **Styling** | Custom CSS | Enhanced UI/UX with dark theme |

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get yours here](https://makersuite.google.com/app/apikey))
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/exam-copilot.git
   cd exam-copilot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv exam-copilot-env
   
   # On Windows
   exam-copilot-env\Scripts\activate
   
   # On macOS/Linux
   source exam-copilot-env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your Gemini API key
   ```

5. **Launch the application**
   ```bash
   streamlit run app.py
   ```

The application will be available at `http://localhost:8501`

## 📖 Usage Guide

### 1. Paper Analysis
1. Navigate to the **Paper Analysis** section
2. Upload one or more PDF exam papers using the file uploader
3. Click "Analyze Papers" to process the documents
4. Review the extracted topics with importance scores and summaries
5. Use the sortable table to prioritize your study focus

### 2. Study Planning
1. Go to the **Study Planner** section
2. Input your available study topics (from analysis or manual entry)
3. Set your study constraints (hours per day, preferred time slots)
4. Generate your personalized daily study timetable
5. Follow the structured schedule with built-in breaks

### 3. Concept Clarification
1. Access the **Clarity Bot** feature
2. Enter any concept or topic you need explained
3. Select your desired explanation level (Beginner to Expert)
4. Receive tailored explanations to enhance understanding

## 📁 Project Architecture

```
exam-copilot/
├── app.py                 # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── paper_analysis.py  # PDF processing and topic extraction
│   ├── study_planner.py   # Timetable generation algorithms
│   └── clarity_bot.py     # Concept explanation engine
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## 🔑 API Configuration

### Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or sign in to your Google account
3. Generate a new API key
4. Add the key to your `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

**Note**: The application uses Gemini 1.5 Flash (free tier). Ensure your API key has appropriate access permissions.

## 🤝 Contributing

We welcome contributions to improve Exam Copilot! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Update tests for new features
- Ensure compatibility with Python 3.8+

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Multi-PDF paper analysis
- [x] Smart study planning
- [x] Concept explanation bot
- [x] Dark theme UI

### Phase 2 (Planned)
- [ ] User authentication and profiles
- [ ] Study progress tracking
- [ ] Export functionality (PDF/CSV)
- [ ] Mobile app development

### Phase 3 (Future)
- [ ] Integration with educational video platforms
- [ ] Collaborative study groups
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/yourusername/exam-copilot/issues)
- **Discussions**: Join community discussions in [GitHub Discussions](https://github.com/yourusername/exam-copilot/discussions)

### Frequently Asked Questions

**Q: Is the Gemini API free to use?**  
A: Yes, Gemini 1.5 Flash offers a generous free tier suitable for personal use.

**Q: What PDF formats are supported?**  
A: The application supports standard PDF files with extractable text content.

**Q: Can I use this for commercial purposes?**  
A: Yes, the MIT license allows commercial use with proper attribution.

---

<p align="center">
  <strong>Built with ❤️ by developers who understand the struggle of exam preparation</strong>
</p>

<p align="center">
  <sub>Powered by Google Gemini AI • Built with Streamlit • Designed for Success</sub>
</p>