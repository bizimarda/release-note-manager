# 🚀 Release Notes Manager

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

AI-powered release notes generation platform that analyzes Jira tasks and GitHub code changes to create professional, comprehensive release documentation.

## ✨ Features

### 🎯 Core Capabilities
- **Multiple Jira Task Support**: Generate release notes for single tasks, multiple tasks (comma-separated), or JQL queries
- **Real-time Progress Tracking**: Monitor job progress with live WebSocket updates
- **AI-Powered Analysis**: Automatically analyze code changes and generate professional release notes
- **GitHub Integration**: Fetch branches, commits, diffs, and detect configuration changes
- **Export Options**: Export release notes to Markdown and HTML formats

### 🔧 Advanced Features
- **JQL Query Filtering**: Use JQL to filter and select tasks (e.g., by project, team, sprint, labels)
- **Epic Support**: Automatically fetch and include all related stories when processing Epic tasks
- **Configuration Detection**: Identify and document application config changes
- **Database Migration Tracking**: Detect and document SQL migration files
- **Job History**: View and reload previously generated release notes

### 🤖 AI Agents

The project includes **21 specialized AI agents** for various development tasks:

#### Development
- Code Generation, Code Review, Test Generation

#### Analysis
- Architecture Advisory, Technology Selection, Code Analysis

#### Maintenance
- Debugging, Refactoring, Documentation

#### Workflow
- Project Planning, Task Management, CI/CD

#### Security
- Security Analysis

#### Quality
- Performance Optimization, Compliance

#### Data
- Database Design, API Design, Integration Management

#### Operations
- Monitoring, Scaling, Migration

#### UI/UX
- UI/UX Recommendations

## 📸 Screenshots

### Generate Tab
- Single task, multiple tasks, or JQL query input
- Real-time progress tracking
- Version and release date configuration

### History Tab
- View all previous jobs
- Filter by status (completed, failed, running)
- Load completed job results with task IDs displayed

### Results Tab
- View generated release notes by service
- Copy to clipboard, download Markdown, export HTML
- Load all completed results at once

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js (for frontend development, optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/bizimarda/release-note-manager.git
cd release-note-manager
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Required configurations in `.env`:**
```env
# Jira Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token

# GitHub Configuration
GITHUB_TOKEN=your-github-personal-access-token
GITHUB_API_URL=https://api.github.com

# AI Provider (groq, openai, anthropic, gemini)
AI_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
```

5. **Setup repository mapping** (optional)
```bash
# Create repo_mapping.conf to map Jira components to GitHub repositories
# Format: jira-component=github-repo
```

6. **Run the application**
```bash
python3 main.py
```

7. **Open in browser**
```
http://localhost:8000
```

## 📖 Usage

### Single Task
1. Select "Single Task" from Input Type dropdown
2. Enter Jira task number (e.g., `PRND-1234`)
3. Click "Generate Release Notes"

### Multiple Tasks
1. Select "Multiple Tasks" from Input Type dropdown
2. Enter multiple task numbers separated by commas (e.g., `PRND-1234, PRND-1235, PRND-1236`)
3. Click "Generate Release Notes"

### JQL Query
1. Select "JQL Filter" from Input Type dropdown
2. Enter JQL query in the editor:
   ```jql
   project = PRND AND status = Done AND labels = Release-2025-Q1 ORDER BY created DESC
   ```
3. Use template buttons for quick JQL queries
4. Click "Generate Release Notes"

### Viewing Results
- **Real-time**: Watch the Progress tab for live updates
- **History**: Go to History tab to see all previous jobs
- **Reload**: Click "View Results" on any completed job in History
- **Load All**: Use "Load All Completed Results" to see all past results

### Export Options
- **Copy**: Copy release notes to clipboard
- **Markdown**: Download as `.md` file
- **HTML**: Export as HTML document

## 🔌 API Documentation

Once the application is running, visit:
- API Docs: http://localhost:8000/docs
- Alternative UI: http://localhost:8000/redoc

### Main Endpoints

#### Generate Release Notes
```http
POST /api/release-notes/generate
Content-Type: application/json

{
  "jira_input": "PRND-1234",
  "input_type": "task",
  "version": "1.2.3",
  "release_date": "2025-01-15",
  "author": "John Doe",
  "release_name": "Q1 2025 Release"
}
```

#### Get Job Status
```http
GET /api/jobs/{job_id}
```

#### List All Jobs
```http
GET /api/jobs?limit=20
```

#### WebSocket Updates
```javascript
ws://localhost:8000/api/jobs/{job_id}
```

## 🏗️ Architecture

### Backend (FastAPI)
- `backend/api/`: REST API endpoints
- `backend/services/`: Business logic
  - `job_worker.py`: Async job processing
  - `jira_service.py`: Jira API integration
  - `github_service.py`: GitHub API integration
  - `ai_service.py`: AI providers (Groq, OpenAI, Anthropic, Gemini)
- `backend/core/`: Configuration and database
- `backend/models/`: Data models and schemas

### Frontend
- `frontend/templates/`: HTML templates
- `frontend/static/js/`: JavaScript application
- `frontend/static/css/`: Styling

### AI Agents
- `agents/`: 21 specialized AI agents for various development tasks

## 🔧 Configuration

### AI Providers

Supported AI providers:
- **Groq** (default): `llama-3.70b-versatile`
- **OpenAI**: `gpt-4o`
- **Anthropic**: `claude-3-5-sonnet-20241022`
- **Google Gemini**: `gemini-1.5-pro`

Configure in `.env`:
```env
AI_PROVIDER=groq
GROQ_API_KEY=your-api-key
GROQ_MODEL=llama-3.70b-versatile
```

### Jira Integration
- Set up API token in Atlassian account settings
- Required permissions: Browse projects and issues
- Epic support automatically includes related stories

### GitHub Integration
- Personal access token with `repo` scope
- Automatic branch detection by task number
- Diff analysis and configuration change detection

## 📊 Workflow

1. **Input Selection**: Choose single task, multiple tasks, or JQL query
2. **Jira Fetch**: Fetch task metadata and related information
3. **GitHub Mapping**: Map tasks to GitHub repositories
4. **Code Analysis**: Analyze code changes and configuration updates
5. **AI Generation**: Generate professional release notes using AI
6. **Result Display**: Show formatted release notes by service
7. **Export**: Download or copy release notes

For detailed workflow information, see [WORKFLOW.md](WORKFLOW.md)

## 🛠️ Development

### Running with different port
```bash
PORT=3000 python3 main.py
```

### Running with uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html
```

### Code Quality
```bash
# Format code
black backend frontend

# Lint code
ruff check backend frontend

# Type check
mypy backend
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Documentation

- [Requirements](APP_REQUIREMENTS.md) - Detailed project requirements
- [Development Prompts](DEVELOPMENT_PROMPTS.md) - AI agent prompts
- [Jira Integration](JIRA_INTEGRATION_ADVANCED.md) - Advanced Jira setup
- [Confluence Integration](CONFLUENCE_INTEGRATION.md) - Confluence setup
- [Workflow](WORKFLOW.md) - Detailed workflow guide

## 🐛 Troubleshooting

### Job stuck in "pending" status
- Check if job worker is running
- Verify database connectivity
- Check logs in `logs/` directory

### Jira connection failed
- Verify Jira URL and credentials
- Check API token permissions
- Ensure network connectivity

### GitHub rate limiting
- Wait for rate limit to reset
- Use authenticated requests with API token
- Reduce concurrent requests

### AI provider errors
- Verify API key is valid
- Check provider status/outages
- Switch to alternative AI provider

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Groq](https://groq.com/) - Fast AI inference
- [Jira](https://www.atlassian.com/software/jira) - Issue tracking
- [GitHub](https://github.com/) - Code hosting and version control

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

Made with ❤️ by [bizimarda](https://github.com/bizimarda)
