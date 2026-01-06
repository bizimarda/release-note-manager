# Development Prompts - Release Notes Manager Web App

This file contains structured prompts for AI agents to develop the Release Notes Manager Web Application based on the requirements in APP_REQUIREMENTS.md.

---

## 01_Project_Overview_and_Architecture

**Prompt:**
```
You are a senior software architect and developer. Your task is to design the overall architecture for a Release Notes Manager Web Application.

## Context
This is a monolithic web application (local use, team internal) that:
- Reads Jira tasks/epics via API
- Reads GitHub code changes via API
- Uses AI to analyze code changes
- Generates service-specific release notes in Confluence-style format
- Provides a web UI for users to input Jira tasks and view/edit release notes
- Runs locally on each team member's machine
- No authentication/users needed (single user local app)
- Configuration via .env file

## Requirements Reference
- Read APP_REQUIREMENTS.md for full requirements
- Core technologies: Python (FastAPI or Flask), SQLite (local database), React/Vue.js for frontend
- AI Integration: OpenAI GPT-4o or Anthropic Claude 3.5
- External APIs: Jira REST API, GitHub REST API

## Task
1. Design the overall application architecture
2. Define the tech stack (frameworks, libraries, tools)
3. Create a high-level component diagram
4. Define the project structure (folders/files)
5. Identify key modules and their responsibilities

## Output Format
Provide:
1. Architecture Overview
2. Tech Stack Selection with rationale
3. Project Structure (directory tree)
4. Key Components and their interactions
5. Data flow diagram (text-based)
```

---

## 02_Tech_Stack_Selection

**Prompt:**
```
You are a senior software engineer. Select the appropriate tech stack for the Release Notes Manager Web Application.

## Context
- Monolithic web application
- Local deployment (no Docker, no Kubernetes)
- Python preferred for backend
- Needs web UI
- External API integrations (Jira, GitHub, OpenAI/Anthropic)
- SQLite for local database
- Background job processing (async operations)
- Export to multiple formats (Markdown, HTML, PDF, Word)

## Requirements
- Simple setup for local users
- Good documentation and community support
- Easy to develop and maintain
- Performant for single-user usage

## Task
1. Select backend framework (FastAPI vs Flask vs Django)
2. Select frontend framework (React vs Vue vs Svelte vs plain HTML/JS)
3. Select AI client library
4. Select HTTP client library for external APIs
5. Select background job processing library
6. Select export/formatting libraries (PDF, Word)
7. Select caching library (Redis - optional)

## Output Format
For each technology selection:
- Technology name
- Rationale (why this choice)
- Key alternatives considered
- Pros and Cons

Example:
```
### Backend Framework
**Selected:** FastAPI
**Rationale:** Fast, modern, async support, automatic API docs, type hints
**Alternatives:** Flask (simpler but slower), Django (too heavy)
**Pros:** Fast, async, auto-generated Swagger docs, Pydantic validation
**Cons:** Newer than Flask, learning curve
```
```

---

## 03_Project_Structure_and_Setup

**Prompt:**
```
You are a senior Python developer. Create the project structure and setup instructions for the Release Notes Manager Web Application.

## Context
Based on the selected tech stack (from previous prompts), create a well-organized project structure.

## Task
1. Define the complete project directory structure
2. List all required dependencies with versions
3. Create requirements.txt
4. Create .env.example with all required environment variables
5. Create setup instructions (installation steps)
6. Create README.md template

## Project Structure Requirements
- Separate backend and frontend (if applicable)
- Organized by feature/module
- Clear separation of concerns
- Easy to navigate

## Output Format
1. Directory tree (ASCII art)
2. requirements.txt content
3. .env.example content
4. Setup/installation instructions (step-by-step)
5. README.md template

## Example Structure
```
release-notes-manager/
├── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── integrations/
│   └── main.py
├── frontend/
│   ├── src/
│   └── public/
├── .env.example
├── requirements.txt
└── README.md
```
```

---

## 04_Jira_Integration_Module

**Prompt:**
```
You are a backend developer. Design and implement the Jira Integration Module.

## Context
This module connects to Jira REST API to:
- Fetch single tasks by task number (e.g., PRND-1234)
- Fetch multiple tasks by task numbers
- Search tasks using JQL filters
- Extract task metadata (ID, summary, description, epic info, assignee, status, labels, project, task type)
- Handle Epic tasks: fetch epic + all associated stories

## Requirements from APP_REQUIREMENTS.md
Reference Section 1: Jira Integration

## Task
1. Design the JiraClient class
2. Implement authentication (API token)
3. Implement methods:
   - get_issue(issue_key)
   - get_issues(issue_keys)
   - search_by_jql(jql_query)
   - get_epic_stories(epic_key)
4. Implement error handling
5. Implement rate limiting respect

## Output Format
Provide:
1. Class structure (Python)
2. Method signatures
3. Example usage
4. Error handling approach
5. Rate limiting strategy

## Jira API Endpoints to Use
- GET /rest/api/2/issue/{issueIdOrKey}
- POST /rest/api/2/search
- GET /rest/api/2/issue/{issueIdOrKey}?fields=...
```

---

## 05_GitHub_Integration_Module

**Prompt:**
```
You are a backend developer. Design and implement the GitHub Integration Module.

## Context
This module connects to GitHub REST API to:
- Map Jira tasks to GitHub repositories (by task number or project name)
- Find branches associated with task numbers
- Extract branch information (name, author, commits)
- Extract commit messages, changed files, diffs
- Extract Git tags (for version detection)
- Detect specific file changes:
  - Configuration files (application.yml, .env, config/*.yml)
  - Database migrations (db/migration/*.sql, db/changelog/*.xml)
  - DevOps files (Dockerfile, deployment.yaml, etc.)
  - Dependency files (pom.xml, package.json, requirements.txt, build.gradle)

## Requirements from APP_REQUIREMENTS.md
Reference Section 2: GitHub Integration

## Task
1. Design the GitHubClient class
2. Implement authentication (Personal Access Token)
3. Implement methods:
   - list_repositories(org)
   - get_branches(repo)
   - get_commits(repo, branch)
   - get_commit_diff(repo, sha)
   - get_file_content(repo, path)
   - get_tags(repo)
4. Implement file change detection logic
5. Implement version detection from tags

## Output Format
Provide:
1. Class structure (Python)
2. Method signatures
3. File pattern matching for each file type
4. Version detection logic
5. Example usage

## GitHub API Endpoints to Use
- GET /repos/{owner}/{repo}
- GET /repos/{owner}/{repo}/branches
- GET /repos/{owner}/{repo}/commits
- GET /repos/{owner}/{repo}/commits/{sha}
- GET /repos/{owner}/{repo}/git/refs/tags
- GET /repos/{owner}/{repo}/contents/{path}
```

---

## 06_AI_Service_and_Analysis_Module

**Prompt:**
```
You are an AI/ML engineer. Design and implement an AI Service Module for code analysis and release note generation with multi-provider support.

## Context
This module:
- Analyzes GitHub Java code changes (commits, diffs)
- Generates meaningful summaries (what changed, why, impact)
- Converts technical Java code changes to business language (for Product Managers)
- Categorizes changes (New Feature, Improvement, Defect Fix, Breaking Change)
- Calculates impact per category (Database, API, UI, Performance, Business Logic)
- Detects and formats configuration changes
- Identifies database migrations
- Identifies DevOps changes
- Detects library upgrades
- Identifies CVE numbers and assesses security impact
- Extracts JIRA ticket references
- Understands context from Jira: title, description, acceptance criteria, comments, scrum team, quarter, dependent tasks, component
- **Multi-provider support:** OpenAI, Anthropic Claude, Google Gemini, Groq
- **Default provider:** Groq (cost-effective and fast)

## Requirements from APP_REQUIREMENTS.md
Reference Section 3: AI-Powered Analysis
Reference Section 10: AI Capabilities Needed
Reference Section 19: AI Model Integration
Reference Section: Configuration Management

## Task
1. Design AIService class with multi-provider support
2. Implement unified interface for all providers (OpenAI, Anthropic, Gemini, Groq)
3. Implement provider selection logic from environment variables (AI_PROVIDER)
4. Default to Groq if not specified
5. Implement fallback mechanism (try secondary provider if primary fails)
6. Design prompts for each analysis type:
    - Code change summarization (Java-specific)
    - Change categorization
    - Impact analysis (per category: Database, API, UI, Performance, Business Logic)
    - Configuration change detection
    - Database migration detection
    - DevOps change detection
    - Library upgrade detection
    - Security/CVE analysis
    - JIRA reference extraction
    - Business language conversion
7. Implement method to combine all analyses
8. Implement cost tracking (token usage per provider)
9. Implement retry logic with exponential backoff

## Output Format
Provide:
1. Class structure (Python)
2. Provider client initialization (OpenAI, Anthropic, Gemini, Groq)
3. Unified chat completion method
4. Prompt templates for each analysis type
5. Example input/output for each prompt
6. Cost tracking implementation
7. Fallback logic
8. Retry logic with exponential backoff
9. Provider-specific adaptations (JSON response format, max tokens, etc.)

## Supported AI Providers

### Groq (Default)
- **Models:** Llama-3-70b-versatile, Llama-3-8b-instant, Mixtral-8x7b-32768
- **Library:** `groq` Python package
- **Configuration:**
  ```python
  AI_PROVIDER=groq
  GROQ_API_KEY=gsk_...
  GROQ_MODEL=llama-3-70b-versatile
  GROQ_BASE_URL=https://api.groq.com/openai/v1
  ```
- **Advantages:** Very fast, extremely cheap ($0.59/1M tokens), good code understanding
- **API Format:** OpenAI-compatible

### OpenAI
- **Models:** GPT-4o, GPT-4, GPT-3.5-turbo
- **Library:** `openai` Python package
- **Configuration:**
  ```python
  AI_PROVIDER=openai
  OPENAI_API_KEY=sk-...
  OPENAI_MODEL=gpt-4o
  OPENAI_BASE_URL=https://api.openai.com/v1
  ```
- **Advantages:** Best overall accuracy, excellent code analysis
- **API Format:** Native OpenAI API

### Anthropic Claude
- **Models:** Claude-3-5-sonnet-20241022, Claude-3-opus-20240229, Claude-3-haiku-20240307
- **Library:** `anthropic` Python package
- **Configuration:**
  ```python
  AI_PROVIDER=anthropic
  ANTHROPIC_API_KEY=sk-ant-...
  ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
  ```
- **Advantages:** Excellent code analysis, cost-effective
- **API Format:** Anthropic Messages API

### Google Gemini
- **Models:** Gemini-1.5-pro, Gemini-1.5-flash, Gemini-1.0-pro
- **Library:** `google-generativeai` Python package
- **Configuration:**
  ```python
  AI_PROVIDER=gemini
  GEMINI_API_KEY=...
  GEMINI_MODEL=gemini-1.5-pro
  ```
- **Advantages:** Fast, cheap, good multimodal support
- **API Format:** Gemini Generative API

## AIService Class Structure
```python
class AIService:
    """Multi-provider AI service for code analysis"""

    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "groq")
        self.model = self._get_model()
        self.client = self._get_client()
        self.fallback_provider = os.getenv("FALLBACK_AI_PROVIDER")

    def _get_model(self):
        """Get model name based on provider"""
        if self.provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4o")
        elif self.provider == "anthropic":
            return os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        elif self.provider == "gemini":
            return os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        elif self.provider == "groq":
            return os.getenv("GROQ_MODEL", "llama-3-70b-versatile")

    def _get_client(self):
        """Initialize provider client"""
        if self.provider == "openai":
            from openai import OpenAI
            return OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            )
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            return genai.GenerativeModel(self.model)
        elif self.provider == "groq":
            from groq import Groq
            return Groq(
                api_key=os.getenv("GROQ_API_KEY"),
                base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
            )

    async def analyze_code(self, diff_content: str, jira_context: dict) -> dict:
        """Analyze code changes with retry and fallback"""
        try:
            return await self._analyze_with_provider(diff_content, jira_context, self.provider)
        except Exception as e:
            logger.error(f"Primary provider {self.provider} failed: {e}")
            if self.fallback_provider:
                logger.info(f"Falling back to {self.fallback_provider}")
                return await self._analyze_with_provider(diff_content, jira_context, self.fallback_provider)
            raise

    async def _analyze_with_provider(self, diff: str, context: dict, provider: str) -> dict:
        """Analyze with specific provider with retry logic"""
        for attempt in range(3):
            try:
                if provider in ["openai", "groq"]:
                    return await self._analyze_openai_format(diff, context, provider)
                elif provider == "anthropic":
                    return await self._analyze_anthropic(diff, context)
                elif provider == "gemini":
                    return await self._analyze_gemini(diff, context)
            except Exception as e:
                if attempt == 2:
                    raise
                wait_time = 2 ** attempt
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)

    async def _analyze_openai_format(self, diff: str, context: dict, provider: str) -> dict:
        """Analyze using OpenAI-compatible API (OpenAI, Groq)"""
        prompt = self._build_prompt(diff, context)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=4096,
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)

    async def _analyze_anthropic(self, diff: str, context: dict) -> dict:
        """Analyze using Anthropic API"""
        prompt = self._build_prompt(diff, context)
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return json.loads(response.content[0].text)

    async def _analyze_gemini(self, diff: str, context: dict) -> dict:
        """Analyze using Gemini API"""
        prompt = self._build_prompt(diff, context)
        response = self.client.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.3,
                "max_output_tokens": 4096
            }
        )
        return json.loads(response.text)

    def _build_prompt(self, diff: str, context: dict) -> str:
        """Build analysis prompt"""
        return f"""
You are a software engineer analyzing Java code changes for a release note.

## Code Changes (Java)
{diff}

## JIRA Task Context
**Title:** {context.get('title')}
**Description:** {context.get('description')}
**Acceptance Criteria:** {context.get('acceptance_criteria', 'Not specified')}
**Component:** {context.get('component')}
**Scrum Team:** {context.get('scrum_team')}
**Quarter:** {context.get('quarter')}
**Dependent Tasks:** {context.get('dependent_tasks', 'None')}

## Task
1. Summarize what changed (2-3 sentences, business language for PMs)
2. Categorize as: New Feature / Improvement / Defect Fix / Breaking Change / Deprecation
3. Calculate confidence score (0.0 to 1.0) for categorization
4. Analyze impact per category:
   - Database: Any schema or data changes?
   - API: New/modified/deprecated endpoints?
   - UI: Frontend changes?
   - Performance: Performance impact?
   - Business Logic: Rule/workflow changes?
5. Extract JIRA ticket references from commit messages (format: [A-Z]+-\d+)

## Output Format (JSON)
{{
  "summary": "Business-friendly summary (2-3 sentences)",
  "category": "New Feature | Improvement | Defect Fix | Breaking Change | Deprecation",
  "confidence": 0.92,
  "impact": {{
    "database": "Description of database changes or 'None'",
    "api": "Description of API changes or 'None'",
    "ui": "Description of UI changes or 'None'",
    "performance": "Description of performance impact or 'None'",
    "business_logic": "Description of business logic changes or 'None'"
  }},
  "jira_tickets": ["PRND-1234"]
}}
"""

    def track_cost(self, input_tokens: int, output_tokens: int, provider: str):
        """Track AI usage costs"""
        pricing = {
            "openai": {"input": 0.005, "output": 0.015},  # GPT-4o per 1K
            "anthropic": {"input": 0.003, "output": 0.015},  # Claude 3.5 Sonnet per 1K
            "gemini": {"input": 0.00125, "output": 0.005},  # Gemini 1.5 Pro per 1K
            "groq": {"input": 0.00000059, "output": 0.00000059}  # Llama 3 70B per 1 token
        }
        rates = pricing.get(provider, pricing["groq"])
        cost = (input_tokens / 1000 * rates["input"]) + (output_tokens / 1000 * rates["output"])
        logger.info(f"Provider: {provider}, Tokens: {input_tokens + output_tokens}, Cost: ${cost:.4f}")
```

## Java-Specific Analysis
- Recognize Spring Boot annotations (@RestController, @Service, @Repository, @Entity, etc.)
- Understand JPA/Hibernate entity changes
- Detect REST endpoint changes (@GetMapping, @PostMapping, etc.)
- Understand DTO/Model changes
- Recognize exception handling patterns

## Business Language Conversion
- Convert: "Added @RestController for /api/v1/orders"
  To: "Added new API endpoint to retrieve order information"
- Convert: "Updated ProductEntity with new field isActive"
  To: "Added ability to mark products as active/inactive"
- Focus on business value, not technical implementation
- Use simple language for Product Managers

## JIRA Context Integration
Extract and use from JIRA:
- Task title
- Task description
- Acceptance criteria
- Comments
- Scrum team
- Quarter (e.g., Q4-2025)
- Dependent tasks (blocked-by, blocking)
- Component (service name)
- Priority
- Assignee

## Retry Logic
- 3 attempts per provider
- Exponential backoff: 2s → 5s → 10s
- Provider-specific backoff:
  - OpenAI/Groq: 2s, 5s, 10s
  - Anthropic: 3s, 7s, 15s
  - Gemini: 4s, 10s, 20s

## Fallback Mechanism
- Primary provider fails → Try fallback provider
- Configure fallback provider via `FALLBACK_AI_PROVIDER` environment variable
- Example: `AI_PROVIDER=groq`, `FALLBACK_AI_PROVIDER=openai`
- If all providers fail → Allow manual completion

## Cost Tracking

### Pricing Reference
| Provider | Model | Input Cost | Output Cost | Per 1K Tokens |
|----------|--------|-------------|--------------|-----------------|
| Groq | Llama 3 70B | $0.59/1M | $0.59/1M | $0.00059 |
| Groq | Llama 3 8B | $0.59/1M | $0.59/1M | $0.00059 |
| Gemini | 1.5 Pro | $1.25/1M | $5.00/1M | $0.00125 / $0.005 |
| Anthropic | Claude 3.5 Sonnet | $3.00/1M | $15.00/1M | $0.003 / $0.015 |
| OpenAI | GPT-4o | $5.00/1M | $15.00/1M | $0.005 / $0.015 |

### Cost Tracking Implementation
- Track input/output tokens per request
- Calculate cost based on provider pricing
- Display total cost per release notes generation
- Show cost breakdown by service

### Example Cost Display
```
Total AI Cost: $0.45
- Product Catalog: $0.20 (34,500 tokens)
- User Service: $0.15 (25,800 tokens)
- Order Service: $0.10 (17,200 tokens)
Provider: Groq (Llama 3 70B)
```
You are an AI/ML engineer. Design and implement AI Service Module for code analysis and release note generation.

## Context
This module:
- Analyzes GitHub Java code changes (commits, diffs)
- Generates meaningful summaries (what changed, why, impact)
- Converts technical Java code changes to business language (for Product Managers)
- Categorizes changes (New Feature, Improvement, Defect Fix, Breaking Change)
- Calculates impact per category (Database, API, UI, Performance, Business Logic)
- Detects and formats configuration changes
- Identifies database migrations
- Identifies DevOps changes
- Detects library upgrades
- Identifies CVE numbers and assesses security impact
- Extracts JIRA ticket references
- Understands context from Jira: title, description, acceptance criteria, comments, scrum team, quarter, dependent tasks, component

## Requirements from APP_REQUIREMENTS.md
Reference Section 3: AI-Powered Analysis
Reference Section 10: AI Capabilities Needed
Reference Section 19: AI Model Integration

## Task
1. Design AIService class
2. Select AI model (OpenAI GPT-4o or Anthropic Claude 3.5)
3. Design prompts for each analysis type:
    - Code change summarization (Java-specific)
    - Change categorization
    - Impact analysis (per category: Database, API, UI, Performance, Business Logic)
    - Configuration change detection
    - Database migration detection
    - DevOps change detection
    - Library upgrade detection
    - Security/CVE analysis
    - JIRA reference extraction
    - Business language conversion
4. Implement method to combine all analyses
5. Implement cost tracking (token usage)
6. Implement fallback mechanism

## Output Format
Provide:
1. Class structure (Python)
2. Prompt templates for each analysis type
3. Example input/output for each prompt
4. Cost tracking implementation
5. Fallback logic
6. Token usage optimization tips

## Java-Specific Analysis
- Recognize Spring Boot annotations (@RestController, @Service, @Repository, @Entity, etc.)
- Understand JPA/Hibernate entity changes
- Detect REST endpoint changes (@GetMapping, @PostMapping, etc.)
- Understand DTO/Model changes
- Recognize exception handling patterns

## Business Language Conversion
- Convert: "Added @RestController for /api/v1/orders"
  To: "Added new API endpoint to retrieve order information"
- Convert: "Updated ProductEntity with new field isActive"
  To: "Added ability to mark products as active/inactive"
- Focus on business value, not technical implementation
- Use simple language for Product Managers

## JIRA Context Integration
Extract and use from JIRA:
- Task title
- Task description
- Acceptance criteria
- Comments
- Scrum team
- Quarter (e.g., Q4-2025)
- Dependent tasks (blocked-by, blocking)
- Component (service name)
- Priority
- Assignee

## Example Prompt Template
```
You are a software engineer analyzing Java code changes for a release note.

## Code Changes (Java)
{diff_content}

## JIRA Task Context
**Title:** {jira_title}
**Description:** {jira_description}
**Acceptance Criteria:** {acceptance_criteria}
**Component:** {component}
**Scrum Team:** {scrum_team}
**Quarter:** {quarter}
**Dependent Tasks:** {dependent_tasks}

## Task
1. Summarize what changed (2-3 sentences, business language for PMs)
2. Categorize as: New Feature / Improvement / Defect Fix / Breaking Change / Deprecation
3. Analyze impact per category:
   - Database: Any schema or data changes?
   - API: New/modified/deprecated endpoints?
   - UI: Frontend changes?
   - Performance: Performance impact?
   - Business Logic: Rule/workflow changes?
4. Extract JIRA ticket references from commit messages

## Output Format (JSON)
{
  "summary": "Business-friendly summary",
  "category": "New Feature | Improvement | Defect Fix | Breaking Change | Deprecation",
  "impact": {
    "database": "...",
    "api": "...",
    "ui": "...",
    "performance": "...",
    "business_logic": "..."
  },
  "jira_tickets": ["PRND-1234"]
}
```

## Impact Analysis Categories

### Database Schema Changes
- Tables added/modified/dropped
- Columns added/modified/dropped
- Index changes
- Data migration requirements

### API Changes
- New endpoints added
- Endpoints modified
- Endpoints deprecated/removed
- Breaking changes (request/response format)
- Authentication/authorization changes

### UI/Frontend Changes
- New UI components
- UI layout changes
- User workflow changes
- Accessibility changes

### Performance Changes
- Response time improvements/degradations
- Memory usage changes
- Caching changes
- Query optimization

### Business Logic Changes
- Rule engine changes
- Workflow changes
- Validation changes
- Calculation logic changes
```
You are an AI/ML engineer. Design and implement the AI Service Module for code analysis and release note generation.

## Context
This module:
- Analyzes GitHub code changes (commits, diffs)
- Generates meaningful summaries (what changed, why, impact)
- Categorizes changes (New Feature, Improvement, Defect Fix, Breaking Change)
- Detects and formats configuration changes
- Identifies database migrations
- Identifies DevOps changes
- Detects library upgrades
- Identifies CVE numbers and assesses security impact
- Extracts JIRA ticket references
- Converts technical changes to user-friendly release notes

## Requirements from APP_REQUIREMENTS.md
Reference Section 3: AI-Powered Analysis
Reference Section 10: AI Capabilities Needed
Reference Section 19: AI Model Integration

## Task
1. Design the AIService class
2. Select AI model (OpenAI GPT-4o or Anthropic Claude 3.5)
3. Design prompts for each analysis type:
   - Code change summarization
   - Change categorization
   - Configuration change detection
   - Database migration detection
   - DevOps change detection
   - Library upgrade detection
   - Security/CVE analysis
   - JIRA reference extraction
4. Implement method to combine all analyses
5. Implement cost tracking (token usage)
6. Implement fallback mechanism

## Output Format
Provide:
1. Class structure (Python)
2. Prompt templates for each analysis type
3. Example input/output for each prompt
4. Cost tracking implementation
5. Fallback logic
6. Token usage optimization tips

## Example Prompt Template
```
You are a software engineer analyzing code changes for a release note.

## Code Changes
{diff_content}

## JIRA Task Context
{jira_description}

## Task
1. Summarize what changed
2. Categorize as: New Feature / Improvement / Defect Fix / Breaking Change
3. Explain the impact

## Output Format
[Your structured output]
```
```

---

## 07_Release_Notes_Generation_Module

**Prompt:**
```
You are a backend developer. Design and implement the Release Notes Generation Module.

## Context
This module:
- Generates service-specific release notes
- Groups stories by service (GitHub repository)
- Applies Confluence-style template with 10 standard sections
- Detects version from Git tags
- Extracts release name from JIRA labels

## Requirements from APP_REQUIREMENTS.md
Reference Section 4: Release Notes Generation
Reference Section 6: Release Notes Generation Requirements

## Task
1. Design the ReleaseNotesGenerator class
2. Implement the template engine (Confluence-style format)
3. Implement section generation:
   1. Version Information
   2. New Features
   3. Improvements
   4. Defect Fixes
   5. Configuration Changes
   6. Breaking Changes
   7. Database Migrations
   8. Known Issues
   9. DevOps Notes
   10. Support
4. Implement service grouping logic
5. Implement version detection
6. Handle empty sections ("None for this release")

## Output Format
Provide:
1. Class structure (Python)
2. Template format (with placeholders)
3. Example complete release note
4. Service grouping algorithm
5. Version detection logic

## Release Note Template
```
# [Service Name] [Version] [Release Name]

## Version Information
**Release Notes:** [Service Name]
**Version:** [X.X.X]
**Release Date:** [DD/MM/YYYY]

## 1. New Features
[Content]

## 2. Improvements
[Content]

...

## 9. Support
[Content]
```
```

---

## 08_Background_Job_Processing

**Prompt:**
```
You are a backend developer. Design and implement Background Job Processing system with SQLite database.

## Context
Large epics can take 1-2+ minutes to process. Background jobs allow users to:
- See progress in real-time
- Navigate away and come back
- Cancel long-running jobs
- Run multiple jobs concurrently (optional)

Why needed:
- Jira fetch: 40 stories (5-10s)
- GitHub fetch: 10 services × (branch + commits + diffs + files) (30-50s)
- AI analysis: 40 stories × AI processing (30-60s)
- Release notes generation: 10 services (5s)
**Total:** 90-120+ seconds

## Requirements from APP_REQUIREMENTS.md
Reference Section: Backend API Design - Background Job Processing

## Task
1. Design JobQueue system using SQLite
2. Define job types:
   - FETCH_JIRA_ISSUES
   - FETCH_GITHUB_CHANGES
   - AI_ANALYZE_CHANGES
   - GENERATE_RELEASE_NOTES
   - GENERATE_ALL (orchestrates all steps)
3. Implement job status states:
   - pending: Job created, waiting to start
   - running: Job is currently executing
   - completed: Job finished successfully
   - failed: Job failed with error
   - cancelled: Job cancelled by user
4. Implement retry mechanism with exponential backoff
5. Implement progress tracking (0-100%)
6. Implement current_step tracking (human-readable status)
7. Implement job cancellation support
8. Implement job worker with async processing
9. Implement progress updates to frontend
   - Polling (simple)
   - WebSocket (real-time, recommended)
10. Implement job cleanup (old jobs > 30 days)

## Output Format
Provide:
1. Job database schema (SQLite CREATE TABLE)
2. JobQueue class implementation
3. JobWorker class implementation
4. Job types and their parameters
5. Progress calculation example
6. Job cancellation flow
7. API endpoints for job management
8. Frontend integration (polling or WebSocket)
9. Error handling in jobs
10. Example job workflow with progress updates

## Job Data Structure
```python
{
    "id": "550e8400-e29b-41d4-a716-446655440000",  # UUID
    "type": "GENERATE_ALL",
    "status": "running",
    "progress": 45,  # 0-100
    "current_step": "AI analyzing...",
    "input": {
        "jira_input": "PRND-1234",
        "input_type": "task",  # task | jql
        "options": {
            "version": null,  # null = auto-detect
            "release_date": "2025-01-02",
            "author": "serkan.kaya",
            "release_name": null
        }
    },
    "result": {
        "services": [...],
        "total_services": 10,
        "completed_services": 3
    },
    "error": null,
    "started_at": "2025-01-02T12:00:00Z",
    "updated_at": "2025-01-02T12:01:00Z",
    "completed_at": null
}
```

## Database Schema
```sql
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,  -- UUID
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    progress INTEGER DEFAULT 0,
    current_step TEXT,
    input TEXT NOT NULL,  -- JSON
    result TEXT,  -- JSON
    error TEXT,
    started_at TIMESTAMP,
    updated_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

## Progress Calculation Example
Epic with 40 stories, 10 services:
- Fetch Jira: 0-5% (5s)
- Map to GitHub: 5-10% (5s)
- Fetch GitHub: 10-20% (10s)
- AI Analysis: 20-60% (40s)  <- Longest step
  Story 1/40 -> 20.5%
  Story 20/40 -> 40%
  Story 40/40 -> 60%
- Generate notes: 60-80% (20s)
- Save results: 80-90% (10s)
- Complete: 100%

Total: ~90 seconds

## API Endpoints
```
POST   /api/release-notes/generate  # Create job, return job_id
GET    /api/jobs/{jobId}         # Get full job status
GET    /api/jobs/{jobId}/status  # Get simplified status
POST   /api/jobs/{jobId}/cancel  # Cancel job
GET    /api/jobs                # List recent jobs
```

## WebSocket Endpoint (Real-time updates)
```
WS /ws/jobs/{jobId}  # Stream job updates
```

## Frontend Integration Options

### Option 1: Polling (Simple)
```javascript
// Poll every 1 second
setInterval(async () => {
    const job = await fetch(`/api/jobs/${jobId}`).then(r => r.json());
    updateUI(job);
    if (job.status === 'completed') clearInterval();
}, 1000);
```

### Option 2: WebSocket (Recommended)
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/jobs/${jobId}`);
ws.onmessage = (e) => {
    const job = JSON.parse(e.data);
    updateUI(job);
    if (job.status === 'completed') ws.close();
};
```

## Job Cancellation Flow
1. User clicks "Cancel"
2. Frontend: POST /api/jobs/{jobId}/cancel
3. Backend:
   - Add job_id to cancelled_jobs set
   - Update status to "cancelled"
   - Worker checks cancelled_jobs
   - Raises JobCancelledException
   - Job exits gracefully

## Error Handling
- Jira auth error → Mark failed, show clear message
- GitHub rate limit → Wait 60s, retry
- AI quota exceeded → Mark failed, show quota message
- Unexpected error → Log, mark failed
```

## Testing
- Test job creation
- Test progress updates
- Test job cancellation
- Test error handling
- Test concurrent jobs
- Test WebSocket updates (if implemented)
```
You are a backend developer. Design and implement the Background Job Processing system.

## Context
Long-running operations need to be processed asynchronously:
- Jira data fetching
- GitHub data fetching
- AI analysis
- Multi-service processing

## Requirements from APP_REQUIREMENTS.md
Reference Section: Backend API Design - Background Job Processing

## Task
1. Design the JobQueue system
2. Use database-backed queue (SQLite)
3. Implement job types:
   - FETCH_JIRA_ISSUES
   - FETCH_GITHUB_CHANGES
   - AI_ANALYZE_CHANGES
   - GENERATE_RELEASE_NOTES
4. Implement retry mechanism with exponential backoff
5. Implement job status tracking:
   - pending
   - running
   - completed
   - failed
   - cancelled
6. Implement progress tracking

## Output Format
Provide:
1. Job model/database schema
2. JobWorker class
3. Job types and their parameters
4. Retry logic implementation
5. Progress update mechanism
6. Example job workflow

## Job Example
```python
{
    "id": "uuid",
    "type": "GENERATE_RELEASE_NOTES",
    "status": "running",
    "progress": 45,
    "input": {"jira_tasks": ["PRND-1234"]},
    "result": null,
    "error": null
}
```
```

---

## 09_Backend_API_Design

**Prompt:**
```
You are a backend developer. Design and implement the REST API for the Release Notes Manager.

## Context
FastAPI-based REST API with the following endpoints:

## Requirements from APP_REQUIREMENTS.md
Reference Section: Backend API Design

## Endpoints to Implement

### Release Notes Endpoints
```
POST   /api/release-notes/generate
GET    /api/release-notes
GET    /api/release-notes/{id}
PUT    /api/release-notes/{id}
DELETE /api/release-notes/{id}
GET    /api/release-notes/{id}/export/{format}
```

### Job Status Endpoints
```
GET    /api/jobs/{jobId}
GET    /api/jobs/{jobId}/status
POST   /api/jobs/{jobId}/cancel
```

### Health Check Endpoints
```
GET /health
GET /health/ready
```

## Task
1. Design request/response schemas using Pydantic
2. Implement standard response format
3. Implement error handling
4. Implement all endpoints
5. Add OpenAPI/Swagger documentation

## Output Format
Provide:
1. Pydantic models for all requests/responses
2. API endpoint implementations
3. Error handling approach
4. Swagger/OpenAPI configuration

## Standard Response Format
```json
{
  "success": true,
  "data": {...},
  "message": "Success"
}
```

## Error Response Format
```json
{
  "success": false,
  "data": null,
  "message": "Error description",
  "errors": [...],
  "code": "ERROR_CODE"
}
```
```

---

## 10_Frontend_Design_and_Implementation

**Prompt:**
```
You are a frontend developer. Design and implement the Web UI for the Release Notes Manager.

## Context
Modern, responsive web UI with the following sections:
- Release note generation panel (input Jira tasks/filters)
- Progress indicators (multi-service processing)
- Release notes display and editor
- Export functionality

## Requirements from APP_REQUIREMENTS.md
Reference Section 5: Web Interface

## Components to Implement

### Dashboard Layout
- Main sections
- Responsive design (desktop, tablet, mobile)

### Input Forms
- Jira input section (single task, multiple tasks, JQL filter)
- Additional options (version, release date, author, release name)

### Progress Indicators
- Step-by-step progress bar
- Multi-service progress bars
- Current operation status

### Release Notes Editor
- Markdown editor with preview
- Section-based editing
- Auto-save drafts

### Export Buttons
- Download as Markdown, HTML, PDF, Word

## Task
1. Choose frontend framework (React/Vue/Svelte)
2. Design component hierarchy
3. Implement all components
4. Implement API integration
5. Add error handling and loading states
6. Style the UI (CSS/Tailwind)

## Output Format
Provide:
1. Component tree/diagram
2. Component implementations
3. State management approach
4. API service layer
5. Styling approach

## Example Component Structure
```
App
├── Dashboard
│   ├── Sidebar
│   ├── GenerationPanel
│   └── ReleaseNotesList
└── ReleaseNotesEditor
    ├── SectionEditor
    ├── Preview
    └── ExportButtons
```
```

---

## 11_Data_Persistence_and_Database

**Prompt:**
```
You are a backend developer. Design and implement the data persistence layer using SQLite.

## Context
SQLite database for local storage.

## Requirements from APP_REQUIREMENTS.md
Reference Section: Data Persistence

## Tables to Create

### release_notes
- id (UUID, primary key)
- service_name (text)
- version (text)
- release_date (text)
- author (text)
- generated_date (timestamp)
- related_jira_tasks (json)
- content (json)
- status (text: draft, published, archived)

### jobs
- id (UUID, primary key)
- type (text)
- status (text: pending, running, completed, failed, cancelled)
- progress (integer)
- input (json)
- result (json)
- error (text)
- created_at (timestamp)
- updated_at (timestamp)

### settings
- key (text, primary key)
- value (text)

## Task
1. Design database schema
2. Create SQLAlchemy models
3. Implement database connection
4. Create migration scripts
5. Implement CRUD operations

## Output Format
Provide:
1. Database schema diagram
2. SQLAlchemy model definitions
3. Database initialization script
4. Example queries

## Model Example
```python
class ReleaseNote(Base):
    __tablename__ = "release_notes"

    id = Column(String, primary_key=True)
    service_name = Column(String)
    version = Column(String)
    ...
```
```

---

## 12_Export_Functionality

**Prompt:**
```
You are a backend developer. Implement the export functionality for multiple formats.

## Context
Export release notes to:
- Markdown (.md)
- HTML (.html)
- PDF (.pdf)
- Word (.docx)

## Requirements from APP_REQUIREMENTS.md
Reference Section: Export Options

## Task
1. Implement Markdown export
2. Implement HTML export (styled)
3. Implement PDF export (formatted)
4. Implement Word export (.docx)
5. Create export service

## Output Format
Provide:
1. Export service class
2. Implementation for each format
3. Required libraries for each format
4. Example usage

## Required Libraries
- Markdown: Built-in string manipulation
- HTML: Jinja2 templates or similar
- PDF: ReportLab or WeasyPrint
- Word: python-docx

## File Format Examples
```
# Markdown
# Service Name X.X.X
## 1. New Features
...

# HTML
<html>
  <head><style>...</style></head>
  <body>...</body>
</html>

# PDF
Rendered from HTML or direct

# Word
Document with proper formatting
```
```

---

## 13_Environment_Configuration

**Prompt:**
```
You are a DevOps engineer. Implement environment configuration management using .env files.

## Context
All configuration via environment variables, no UI for settings.

## Requirements from APP_REQUIREMENTS.md
Reference Section: Configuration Management

## Environment Variables

```bash
# Jira Configuration
JIRA_BASE_URL=https://your-jira-instance.atlassian.net
JIRA_API_TOKEN=your-jira-api-token
JIRA_USERNAME=your-email@company.com
JIRA_PROJECT_KEY=PRND

# GitHub Configuration
GITHUB_TOKEN=your-github-personal-access-token
GITHUB_ORG=your-organization

# AI Service Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o
# OR
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false

# Database Configuration
DATABASE_URL=sqlite:///./release_notes.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Cache Configuration (Optional)
CACHE_ENABLED=false
CACHE_TYPE=redis
CACHE_HOST=localhost
CACHE_PORT=6379
```

## Task
1. Create configuration loader
2. Validate required environment variables on startup
3. Show clear error messages for missing variables
4. Create .env.example file
5. Document all variables

## Output Format
Provide:
1. Configuration loader class
2. Validation logic
3. .env.example file
4. Documentation for each variable
```

---

## 14_Monitoring_and_Logging

**Prompt:**
```
You are a backend developer. Implement application logging and monitoring.

## Context
Basic logging and health checks for local application.

## Requirements from APP_REQUIREMENTS.md
Reference Section: Monitoring & Logging

## Task
1. Implement structured logging
2. Log to console and file
3. Support log levels: ERROR, WARN, INFO, DEBUG
4. Implement health check endpoints:
   - GET /health
   - GET /health/ready
5. Add request ID tracking

## Output Format
Provide:
1. Logging configuration
2. Logger setup
3. Health check implementation
4. Example log output

## Log Format
```
2025-01-02 12:00:00 | INFO | main | Starting application...
2025-01-02 12:00:01 | INFO | jira | Fetching issue PRND-1234...
2025-01-02 12:00:02 | ERROR | github | Failed to fetch branches: 404
```
```

---

## 15_Testing_Strategy

**Prompt:**
```
You are a QA engineer. Design and implement the testing strategy.

## Context
Unit tests and integration tests for the application.

## Requirements from APP_REQUIREMENTS.md
Reference Section: Testing Strategy

## Task
1. Set up pytest framework
2. Implement unit tests:
   - Business logic
   - Data validation
   - Configuration parsing
   - Utility functions
3. Implement integration tests:
   - Jira API integration (mocked)
   - GitHub API integration (mocked)
   - Database operations (SQLite in-memory)
   - AI service (mocked)
4. Aim for 70%+ code coverage

## Output Format
Provide:
1. Test structure
2. pytest configuration
3. Mock strategies for external APIs
4. Example unit tests
5. Example integration tests

## Test Structure
```
tests/
├── unit/
│   ├── test_jira_client.py
│   ├── test_github_client.py
│   ├── test_ai_service.py
│   └── test_release_notes_generator.py
└── integration/
    ├── test_api.py
    └── test_jobs.py
```
```

---

## 16_Security_and_Input_Validation

**Prompt:**
```
You are a security engineer. Implement security best practices and input validation.

## Context
Local application but still needs security measures.

## Requirements from APP_REQUIREMENTS.md
Reference Section: Security Best Practices

## Task
1. Implement input validation for all user inputs
2. Sanitize JQL queries
3. Validate file uploads
4. Implement SQL injection prevention (parameterized queries)
5. Implement XSS prevention (sanitize HTML output)
6. Add security headers (if applicable)
7. Implement dependency vulnerability scanning

## Output Format
Provide:
1. Input validation approach
2. JQL query sanitization
3. SQL injection prevention examples
4. XSS prevention examples
5. Security best practices checklist
6. Dependency scanning setup

## Validation Examples
```python
# Input validation
def validate_jira_key(key: str) -> bool:
    pattern = r'^[A-Z]+-\d+$'
    return bool(re.match(pattern, key))

# JQL sanitization
def sanitize_jql(jql: str) -> str:
    # Remove dangerous keywords
    ...

# SQL injection prevention
def get_release_note(id: str):
    # Use parameterized query
    session.execute(
        "SELECT * FROM release_notes WHERE id = :id",
        {"id": id}
    )
```
```

---

## 17_Complete_Workflow_Implementation

**Prompt:**
```
You are a senior developer. Implement the complete end-to-end workflow.

## Context
The complete data flow from user input to release notes generation with detailed error handling and data transformations.

## Requirements from APP_REQUIREMENTS.md
Reference Section: Data Flow

## Detailed Data Flow

### Step 1: User Input
**Action:** User enters Jira task numbers/filters in web UI
**Input:** Task number(s), JQL filter, additional options (version, date, author)
**Output:** Structured request object, job created, job ID returned
**Error Handling:** Validation errors shown immediately

### Step 2: Fetch Jira Task Data
**Action:** Fetch task data from Jira (Epic + all child stories if Epic)
**API:** GET /rest/api/2/issue/{key} or POST /rest/api/2/search
**Input:** Jira task key(s) or JQL filter
**Output:** Task data (ID, summary, description, epic, assignee, status, labels, project, task type, component, scrum team, acceptance criteria, comments, dependent tasks)
**Transform:** Normalize Jira API response to internal data model
**Retry:** 3 attempts (1s, 2s, 4s), then show error to user

### Step 3: Map Jira Tasks to GitHub Repositories
**Action:** Map Jira tasks to GitHub repositories
**Mapping Rules:** Component → Repository name, Project → GitHub organization, Task number → Branch search
**Input:** Jira task data
**Output:** List of (task_key, repository_name, organization) mappings
**Error Handling:** Show tasks that couldn't be mapped

### Step 4: Find GitHub Branches
**Action:** Find branches associated with tasks
**API:** GET /repos/{org}/{repo}/branches
**Input:** Organization, repository names, task numbers
**Output:** Branches per task (name, author, last commit SHA)
**Transform:** Normalize branch names, extract task number
**Retry:** 3 attempts (1s, 2s, 4s), then show error to user

### Step 5: Fetch GitHub Code Changes
**Action:** Fetch code changes from GitHub
**API:** GET /repos/{org}/{repo}/commits, /commits/{sha}, /git/refs/tags, /contents/{path}
**Input:** Branches
**Output:** Commits, diffs, git tags, file changes (config, migrations, devops, dependencies)
**Transform:** Filter files by type, extract relevant content from diffs
**Retry:** 3 attempts (1s, 2s, 4s), then show error to user

### Step 6: AI Analysis
**Action:** AI analyzes code changes and generates summaries
**API:** OpenAI GPT-4o or Anthropic Claude 3.5
**Input:** Code diffs, Jira task data
**Output:** Summary, category with confidence, impact per category, config changes, migrations, devops changes, library upgrades, CVEs, JIRA tickets
**Transform:** Parse AI response, validate categories, format config changes
**Retry:** 3 attempts (2s, 5s, 10s), then allow manual completion

### Step 7: Group Tasks by Service
**Action:** Group tasks/stories by service (GitHub repository)
**Input:** AI analysis results, Jira task data, GitHub repository mappings
**Output:** Grouped services with stories, changes, AI analyses
**Transform:** Merge analyses for same service, calculate service-level version
**Error Handling:** Show "No code changes found for any service"

### Step 8: Generate Release Notes
**Action:** Generate service-specific release notes
**Input:** Grouped services
**Output:** Markdown content for each service, JSON structure for UI
**Transform:** AI analyses → Categorized sections, config changes → YAML/Env formats, CVEs → Formatted with links
**Error Handling:** Fallback template if rendering fails

### Step 9: Display to User
**Action:** Display all service release notes in web UI
**Input:** Generated release notes
**Output:** UI with tabs/accordion for each service, Markdown editor, preview mode
**Actions:** User can edit, add sections, change categorization, add manual entries

### Step 10: Export
**Action:** Export release notes
**Input:** Edited release notes from UI
**Output:** Files downloaded (Markdown, HTML, PDF, Word)
**Error Handling:** Retry download, show "Copy to clipboard" as fallback

## Error Handling Strategy

### Retry Logic
- All external API calls (Jira, GitHub, AI): 3 retries
- Exponential backoff: 1s → 2s → 4s (Jira/GitHub), 2s → 5s → 10s (AI)
- After 3 failures: Stop and show error to user with specific reason

### Error Messages to User
- Always show specific reason for failure
- Include helpful suggestions (e.g., "Check your API credentials")
- Provide retry button
- Allow manual completion where possible

### Progress Updates
- Update job progress after each step
- Show current operation (e.g., "Fetching Jira tasks...", "Analyzing code changes...")
- Show percentage for multi-service processing
- Update UI in real-time via WebSocket or polling

### Fallback Mechanism
- If AI fails: Allow user to complete release notes manually
- If Jira fails: Allow manual entry of task details
- If GitHub fails: Allow manual code change description
- If export fails: Allow copy to clipboard as fallback

## Task
1. Implement the orchestration service (WorkflowService class)
2. Connect all modules (Jira, GitHub, AI, Release Notes)
3. Implement error handling with retry logic
4. Implement progress tracking with real-time updates
5. Implement data transformation between steps
6. Implement fallback mechanisms
7. Test the complete workflow end-to-end

## Output Format
Provide:
1. WorkflowService class implementation
2. Detailed workflow diagram with data flow
3. Step-by-step implementation for each step
4. Error handling implementation with retry logic
5. Progress update mechanism
6. Testing approach for each step

## WorkflowService Class Structure
```python
class WorkflowService:
    def __init__(self):
        self.jira_client = JiraClient()
        self.github_client = GitHubClient()
        self.ai_service = AIService()
        self.release_notes_generator = ReleaseNotesGenerator()

    async def generate_release_notes(self, input_data):
        # Step 1: Validate input
        # Step 2: Fetch Jira data (with retry)
        # Step 3: Map to GitHub
        # Step 4: Find branches (with retry)
        # Step 5: Fetch changes (with retry)
        # Step 6: AI analysis (with retry)
        # Step 7: Group by service
        # Step 8: Generate release notes
        # Step 9: Return results

    def handle_error(self, error, step):
        # Implement retry logic
        # Provide user-friendly error message
        # Allow fallback mechanisms

    def update_progress(self, job_id, progress, message):
        # Update job status in database
        # Notify frontend
```

## Workflow Diagram (Detailed)
```
User Input
    ↓ [Validate Input]
Jira Integration
    ↓ [3x Retry, Exponential Backoff]
GitHub Mapping
    ↓ [Component → Repository]
Find Branches
    ↓ [3x Retry]
Fetch Changes
    ↓ [3x Retry, Filter by Type]
AI Analysis
    ↓ [3x Retry, Confidence Scores]
Group by Service
    ↓ [Merge Analyses]
Generate Release Notes
    ↓ [Apply Template, Transform Data]
Display to User
    ↓ [Markdown Editor, Preview]
Export
    ↓ [Convert Format, Download]
```

## Testing Approach
For each step:
1. Unit test the step in isolation
2. Test error handling with mock failures
3. Test retry logic
4. Test data transformation
5. Integration test connecting to next step
6. End-to-end test with real services (if available)


---

## 18_Final_Assembly_and_Packaging

**Prompt:**
```
You are a DevOps engineer. Assemble and package the application for local deployment.

## Context
Prepare the application for local use by team members.

## Task
1. Ensure all components work together
2. Create startup script
3. Create installation guide
4. Create user documentation
5. Final testing
6. Package application

## Output Format
Provide:
1. Installation guide (step-by-step)
2. User manual
3. Troubleshooting guide
4. Startup script
5. Final checklist

## Installation Steps
1. Install Python 3.11+
2. Clone repository
3. Install dependencies: pip install -r requirements.txt
4. Copy .env.example to .env
5. Fill in API credentials
6. Run: python backend/main.py
7. Open http://localhost:8000
```

---

## Prompt Usage Guide

### How to Use These Prompts

1. **Sequential Execution**: Start with prompt #01 and proceed in order
2. **Parallel Execution**: Prompts #02, #03, #04, #05 can be executed in parallel
3. **Review Before Next Step**: Review output of each prompt before proceeding
4. **Iterative Refinement**: If output doesn't meet requirements, refine and re-run

### Agent Assignment

Each prompt can be assigned to appropriate agent:
- Architecture/Tech Stack → ArchitectureAdvisorAgent, TechnologySelectionAgent
- Module Development → CodeGenerationAgent
- Testing → TestGenerationAgent
- API Design → CodeGenerationAgent
- Frontend → CodeGenerationAgent
- Security → SecurityAgent
- Documentation → DocumentationAgent

### Expected Deliverables

After completing all prompts, you should have:
- Complete application code
- Working REST API
- Functional web UI
- Database schema and migrations
- All integrations working (Jira, GitHub, AI)
- Test suite
- Documentation
- Installation guide
