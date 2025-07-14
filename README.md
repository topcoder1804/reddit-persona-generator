# Reddit User Persona Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq%20API-orange.svg)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> This project generates comprehensive user personas from Reddit profiles using Groq's Llama 4 Scout model.

## 🚀 Features

- **⚡ Ultra-Fast Processing**: Powered by Groq's LPU architecture with meta-llama/llama-4-scout-17b-16e-instruct
- **🔍 Comprehensive Analysis**: Demographics, personality traits, interests, and behavioral patterns
- **📊 Evidence-Based Insights**: Every characteristic backed by specific citations from user content
- **🆓 Free API Usage**: Utilizes Groq's generous free tier
- **🔒 Privacy Focused**: No data storage, real-time analysis only

## 📋 Quick Start

### Prerequisites
- Python 3.8 or higher
- Reddit API credentials
- Groq API key (free)

### Installation

1. **Clone the repository**
> git clone https://github.com/topcoder1804/reddit-persona-generator.git

2. **Install dependencies**
> pip install -r requirements.txt

3. **Configure environment variables**
> cp .env.example .env

4. **Get API Keys**
- **Reddit API**: Visit https://www.reddit.com/prefs/apps → Create "script" app
- **Groq API**: Visit https://console.groq.com → Create free API key

### Usage
> python3 main.py <reddit_profile_url>

**Examples:**

- python3 main.py https://www.reddit.com/user/kojied/
- python3 main.py https://www.reddit.com/user/Hungry-Move-6603/

## 🔧 Configuration

### Environment Variables (.env)
REDDIT_CLIENT_ID=your_reddit_client_id <br />
REDDIT_CLIENT_SECRET=your_reddit_client_secret <br />
REDDIT_USER_AGENT=PersonaGenerator/1.0 <br />
GROQ_API_KEY=your_groq_api_key <br />

### Reddit API Setup
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" → Choose "script"
3. Use `http://localhost` as redirect URL
4. Note your client_id and client_secret

### Groq API Setup
1. Visit https://console.groq.com
2. Sign up for free account
3. Create new API key
4. Copy key to .env file

## 📊 Output Format

The script generates two files per user:
- `{username}_persona.txt` - Comprehensive persona analysis
- `{username}_raw_data.json` - Raw scraped Reddit data

### Sample Outputs
Two sample persona outputs have been generated and are stored in the `output/` directory:
- **kojied_persona.txt** - Persona analysis for user kojied
- **Hungry-Move-6603_persona.txt** - Persona analysis for user Hungry-Move-6603

These samples demonstrate the comprehensive analysis capabilities of the tool and serve as examples of the expected output format.

### Sample Persona Sections:
- **Demographics** (age, location, occupation estimates)
- **Personality Traits** (communication style, emotional patterns)
- **Interests & Expertise** (ranked by engagement)
- **Online Behavior Patterns** (posting habits, interaction style)
- **Motivations & Goals** (what drives participation)
- **Behavioral Insights** (advanced psychological analysis)
- **Supporting Evidence** (cited posts and comments)

## 🤖 Technical Details

- **Model**: meta-llama/llama-4-scout-17b-16e-instruct
- **Provider**: Groq API
- **Speed**: <1ms per token latency
- **Context Window**: 128K tokens
- **Analysis Depth**: 25 top posts + 35 top comments
- **Citation System**: Direct quotes with URLs

