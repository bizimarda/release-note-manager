# Release Notes Manager

AI-powered release notes generation from Jira tickets and GitHub commits.

## Features

- **Jira Integration**: Fetch tasks, epics, and stories
- **GitHub Integration**: Analyze code changes from branches and commits
- **AI Analysis**: Automatic summarization and categorization of changes
- **Service-Based Release Notes**: Generate separate notes for each service
- **Real-time Progress**: WebSocket support for live updates
- **Multiple Export Formats**: Markdown, HTML, PDF
- **Modern UI**: Clean, intuitive interface with blue-white color scheme

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and configure:

- **AI Provider**: Set `AI_PROVIDER=groq` (default) and provide `GROQ_API_KEY`
- **Jira**: Configure `JIRA_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN`
- **GitHub**: Set `GITHUB_TOKEN`

### 3. Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:8000`

## Configuration

### AI Providers

#### Groq (Default - Fast & Free)
```env
AI_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3-70b-versatile
```

Get API key from: https://console.groq.com/

#### OpenAI
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o
```

#### Anthropic Claude
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

#### Google Gemini
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-pro
```

### Jira Configuration

Get API token from: https://id.atlassian.com/manage-profile/security/api-tokens

```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
```

### GitHub Configuration

Create a Personal Access Token from: https://github.com/settings/tokens

Required scopes: `repo`, `read:org`

```env
GITHUB_TOKEN=github_pat_xxxxxxxxxxxxx
GITHUB_API_URL=https://api.github.com
```

## Usage

### Generate Release Notes

1. Navigate to `http://localhost:8000`
2. Select input type (Task / JQL Filter)
3. Enter Jira task number or JQL query
4. Optionally provide version, release date, and author
5. Click "Generate Release Notes"
6. Monitor progress in real-time
7. Review and export results

### Supported Input Types

- **Single Task**: Enter task number (e.g., `PRND-1234`)
  - If task is Epic, automatically fetches all stories
- **Multiple Tasks**: Comma-separated task numbers (e.g., `PRND-1234, PRND-1235`)
- **JQL Filter**: Custom JQL query (e.g., `project = PRND AND status = Done`)

### Export Options

- **Markdown**: Download as `.md` file
- **HTML**: View in browser
- **PDF**: Professional document export

## API Endpoints

### Release Notes
- `POST /api/release-notes/generate` - Start new generation job
- `GET /api/jobs/{job_id}` - Get job details
- `GET /api/jobs/{job_id}/status` - Get job status
- `POST /api/jobs/{job_id}/cancel` - Cancel job
- `GET /api/jobs` - List recent jobs

### Export
- `GET /api/export/{job_id}/markdown` - Export as Markdown
- `GET /api/export/{job_id}/html` - Export as HTML
- `GET /api/export/{job_id}/pdf` - Export as PDF

### WebSocket
- `WS /api/jobs/{job_id}` - Real-time job updates

## Project Structure

```
agentic/
├── backend/
│   ├── api/              # API endpoints
│   ├── core/             # Core configuration
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   └── utils/            # Utilities
├── frontend/
│   ├── static/
│   │   ├── css/         # Stylesheets
│   │   └── js/          # JavaScript
│   └── templates/        # HTML templates
├── data/                 # Database files
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── .env                 # Environment configuration
```

## Development

### Run with Hot Reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

```bash
# Format code
black backend/ frontend/

# Lint
ruff check backend/ frontend/

# Type check
mypy backend/
```

### Run Tests

```bash
pytest tests/ -v
```

## License

MIT

## Support

For issues and questions, please visit the project repository.
