# Release Notes Manager Web App - Requirements

## Project Overview
AI-powered web application that generates release notes by analyzing Jira tasks and GitHub code changes.

## Core Features

### 1. Jira Integration
- Connect to Jira API
- Read tasks/epics by:
  - Single task number
  - Multiple task numbers
  - JQL filters
- Extract task metadata:
  - Task ID and summary
  - Description
  - Epic information
  - Assignee/Developer
  - Status
  - Labels
  - Project name
  - Task type (Story, Epic, Task, Bug, etc.)
- Handle Epic tasks:
  - When task type is Epic, fetch both epic notes and all associated story notes
  - Group stories under their parent epic
  - Include both epic-level and story-level information in release notes
- Example JQL filters:
  - `project = PRND AND "scrum team[dropdown]" = SATURN AND labels = Saturn_2025_Q4 ORDER BY created DESC`
  - Support custom JQL queries with filtering by project, team, sprint, labels, status

### 2. GitHub Integration
- Connect to GitHub API
- Map Jira tasks to GitHub repositories using:
  - Jira task number
  - Jira project name
- Find branches associated with task numbers
- Extract branch information:
  - Branch name
  - Author/Developer
  - Commit messages
  - Changed files
  - Diff/content changes
  - Git tags (for version detection)
- Detect configuration changes:
  - Identify config file modifications (application.yml, .env, config/*.yml)
  - Extract new, modified, or deprecated configuration parameters
- Detect database migrations:
  - db/migration/*.sql (Flyway)
  - db/changelog/*.xml (Liquibase)
  - Custom migration scripts
  - Extract SQL changes and descriptions
- Detect DevOps changes:
  - Dockerfile, docker-compose.yml
  - Kubernetes manifests (deployment.yaml, service.yaml, ingress.yaml)
  - Helm charts (Chart.yaml, values.yaml)
  - CI/CD files (.github/workflows/*.yml, Jenkinsfile, GitLab CI)
- Detect dependency changes:
  - pom.xml (Maven)
  - package.json (npm)
  - requirements.txt (Python)
  - build.gradle (Gradle)
  - Extract version upgrades

### 3. AI-Powered Analysis

#### Code Change Analysis
- Analyze Java code changes from GitHub commits
- Support Java-specific patterns:
  - Class/method changes
  - Spring Boot annotations (@RestController, @Service, @Repository, etc.)
  - JPA/Hibernate entity changes
  - REST endpoint changes (@GetMapping, @PostMapping, etc.)
  - DTO/Model changes
  - Exception handling changes
- Analyze diff formats:
  - Unified diffs (git diff output)
  - Individual file diffs
  - Line-by-line changes

#### Summarization
- Convert technical Java code changes to business language (for Product Managers)
- Explanation levels:
  - High-level summary (1-2 sentences) for PMs
  - Medium detail (bullet points) for technical stakeholders
  - Technical details (code snippets) for developers (optional section)
- Summarization approach:
  - Focus on "what business value is delivered"
  - Avoid technical jargon where possible
  - Explain impact on end users
  - Highlight breaking changes clearly
- Format:
  - Short, clear paragraphs
  - Bullet points for multiple changes
  - Examples for complex features

#### Impact Analysis
- Calculate impact per category:
  - **Database Schema Changes:**
    - Tables added/modified/dropped
    - Columns added/modified/dropped
    - Index changes
    - Data migration requirements
  - **API Changes:**
    - New endpoints added
    - Endpoints modified
    - Endpoints deprecated/removed
    - Breaking changes (request/response format)
    - Authentication/authorization changes
  - **UI/Frontend Changes:**
    - New UI components
    - UI layout changes
    - User workflow changes
    - Accessibility changes
  - **Performance Changes:**
    - Response time improvements/degradations
    - Memory usage changes
    - Caching changes
    - Query optimization
  - **Business Logic Changes:**
    - Rule engine changes
    - Workflow changes
    - Validation changes
    - Calculation logic changes

#### Context Understanding from Jira
- Extract and use the following from Jira tasks:
  - **Task Title:** Main feature/change description
  - **Task Description:** Detailed requirements
  - **Acceptance Criteria:** Specific conditions that must be met
  - **Comments:** Additional context from developer discussions
  - **Scrum Team:** Team responsible for the task
  - **Quarter:** Release quarter (e.g., Q4-2025)
  - **Labels:** Additional categorization (e.g., "critical", "performance")
  - **Component:** Service name associated with task
  - **Dependent Tasks:**
    - Blocked-by tasks (tasks blocking this task)
    - Blocking tasks (tasks this task is blocking)
  - **Priority:** Task priority level
  - **Assignee:** Developer responsible
- Context usage:
  - Use task description to understand business requirements
  - Use acceptance criteria to verify completeness
  - Use dependent tasks to understand dependencies
  - Use component to map to correct GitHub repository

#### Change Categorization
AI must categorize changes into:
- **New Features:** New functionality added
  - New API endpoints
  - New UI components
  - New business rules
- **Improvements:** Enhancements to existing functionality
  - Performance optimizations
  - Code refactoring
  - Library/framework upgrades
  - UI/UX improvements
- **Defect Fixes:** Bug fixes with JIRA ticket references
  - Production bugs
  - QA bugs
  - User-reported issues
- **Breaking Changes:** Changes requiring user action
  - API contract changes
  - Database schema changes requiring migration
  - Deprecated features removed
- **Deprecation:** Features marked for future removal

### 4. Release Notes Generation
- Service-based release notes generation:
  - Epic may contain stories from multiple different services/projects
  - Group stories by service/project (GitHub repository)
  - Generate separate release notes for each service
  - Example: Epic "Snapshot data integration" has 40 stories across 10 services
    - Generate release notes for product_catalog service
    - Generate release notes for each of the other services
- Release Note Template Structure (Confluence-style):
  ```
  # [Service Name] [Version] [Release Name]

  ## Version Information
  **Release Notes:** [Service Name]
  **Version:** [X.X.X]
  **Release Date:** [DD/MM/YYYY]
  **Author:** [Release Manager]

  ## 1. New Features
  [List of new features or "None for this release"]

  ## 2. Improvements
  [List of improvements or "None for this release"]

  ## 3. Defect Fixes
  - [JIRA ID] [Description of fix]
  [Or "None for this release"]

  ## 4. Configuration Changes
  [New/Modified/Deprecated config parameters]
  [Environment variable examples]
  [YAML config examples]
  [Or "None for this release"]

  ## 5. Breaking Changes
  [List of breaking changes or "None for this release"]

  ## 6. Database Migrations
  [Migration scripts or notes]
  [Or "None for this release"]

  ## 7. Known Issues
  - [CVE-XXXX-XXXXX] [Description and impact analysis]
  [Or "None for this release"]

  ## 8. DevOps Notes
  [Deployment instructions, environment changes]
  [Or "None for this release"]

  ## 9. Support
  [Support portal link or contact information]
  ```
- Standard Sections (always present, can be empty):
  1. **Version Information**: Service name, version, release date, author
  2. **New Features**: New functionality added
  3. **Improvements**: Enhancements to existing functionality (e.g., library upgrades)
  4. **Defect Fixes**: Bug fixes with JIRA ticket references
  5. **Configuration Changes**: Config file changes, environment variables
  6. **Breaking Changes**: Changes requiring user action
  7. **Database Migrations**: SQL scripts, schema changes
  8. **Known Issues**: CVE vulnerabilities, open issues
  9. **DevOps Notes**: Deployment instructions, environment requirements
  10. **Support**: Support links, contact info
- Default text for empty sections: "None for this release"
- Change categorization (auto-detected):
  - **New Features**: New functionality
  - **Improvements**: Library upgrades, performance improvements
  - **Defect Fixes**: Bug fixes with JIRA references
  - **Breaking Changes**: Backward-incompatible changes
- Configuration changes detection:
  - AI analyzes config file diffs
  - Format as environment variables and YAML snippets
  - Mark deprecated parameters
- Security/CVE detection:
  - Extract CVE numbers from Jira descriptions or commit messages
  - Generate impact analysis (No impact expected, Partial impact, etc.)
- Version management:
  - Detect version from Git tags (e.g., v2.22.0, 1.19.0)
  - Or from Jira version field
  - Or manual input if needed
- Release name:
  - Extract from Jira labels (e.g., Saturn_2025_Q4)
  - Or format as "YYYY Q[Quarter]"
- Format options:
  - Markdown
  - HTML
  - Plain text
  - Confluence-compatible format

### 5. Web Interface

#### Dashboard Layout
- Main sections:
  - Release note generation panel
  - History & archive panel
  - Saved drafts panel
  - Recent activities panel
- Responsive design:
  - Desktop (1920px+)
  - Tablet (768px - 1024px)
  - Mobile (< 768px)

#### Input Forms
- Jira input section:
  - Single task number input
  - Multiple task numbers (comma-separated or bulk upload)
  - JQL filter editor with syntax highlighting
  - Saved JQL queries dropdown
- Additional options:
  - Version input (auto-detected from Git tag)
  - Release date picker
  - Author selection (current user default)
  - Release name input
  - Template selection

#### Progress Indicators
- Real-time progress tracking:
  - Step-by-step progress bar
  - Current operation status
  - Estimated remaining time
  - Processing animation
- Multi-service processing:
  - Per-service progress bars
  - Overall progress indicator
  - Completed services list

#### Loading States
- Loading spinners for async operations
- Skeleton screens for content loading
- Cancel button for long-running operations
- Retry mechanism for failed operations

#### Error Handling
- User-friendly error messages
- Error categorization:
  - API authentication errors
  - Rate limit errors
  - Network errors
  - Validation errors
- Error recovery options:
  - Retry button
  - Contact support link
- Error logging for debugging

#### Release Notes Editor
- Rich text editor or Markdown editor
- Preview mode
- Section-based editing
- Auto-save drafts
- Version history
- Collaboration features (optional):
  - Comments per section
  - @mention support

#### Export Functionality
- Copy to clipboard
- Download as file (Markdown, HTML, PDF, Word)
- Publish to Confluence
- Publish to Jira (optional)
- Send via Email

## Technical Requirements

### Release Notes Generation Requirements

#### Standard Sections (All Required, May Be Empty)
1. **Version Information**
   - Service name
   - Version number (X.Y.Z format)
   - Release date (DD/MM/YYYY)
   - Author/Release Manager
   - Release name (e.g., "2025 Q4 Release")

2. **New Features**
   - New functionality added
   - Feature descriptions with context

3. **Improvements**
   - Library/framework upgrades (e.g., "Spring Boot upgrade to 3.5.8")
   - Performance improvements
   - Code quality improvements

4. **Defect Fixes**
   - Bug fixes with JIRA ticket references (e.g., "PRND-40370")
   - Detailed description of the fix
   - Link to JIRA ticket

5. **Configuration Changes**
   - New/Modified/Deprecated config parameters
   - Environment variable examples
   - YAML configuration snippets
   - Mark deprecated parameters

6. **Breaking Changes**
   - Backward-incompatible changes
   - Migration requirements
   - Action items for users

7. **Database Migrations**
   - SQL migration scripts
   - Flyway/Liquibase changes
   - Schema modifications
   - Data migration notes

8. **Known Issues**
   - CVE vulnerabilities with impact analysis
   - Open bugs or limitations
   - Workarounds if available

9. **DevOps Notes**
   - Deployment instructions
   - Environment changes
   - Docker/Kubernetes changes
   - CI/CD pipeline updates

10. **Support**
    - Support portal links
    - Contact information
    - Documentation links

#### Empty Section Handling
- Default text: "None for this release."
- All sections must be present even if empty

#### Configuration Changes Section
- Detect changes in configuration files:
  - application.yml, application.properties
  - .env files
  - config/*.yml, config/*.properties
  - Docker-compose files
- Format as:
  - List of changed parameters (new, modified, deprecated)
  - Environment variable examples with default values
  - YAML configuration snippets
- Mark deprecated parameters clearly
- Group related configuration changes

#### Database Migrations Section
- Detect migration files:
  - db/migration/*.sql (Flyway)
  - db/changelog/*.xml (Liquibase)
  - Custom migration scripts
- Extract migration descriptions
- List schema changes
- Note any data migration requirements

#### DevOps Notes Section
- Detect infrastructure changes:
  - Dockerfile changes
  - Kubernetes manifests (deployment.yaml, service.yaml)
  - Helm charts
  - CI/CD pipeline configurations (.github/workflows, Jenkinsfile)
- Extract deployment requirements
- Note environment-specific changes

#### Security/Known Issues Section
- Detect CVE numbers from:
  - Jira task descriptions
  - Commit messages
  - Pull request descriptions
- Analyze affected code:
  - Check if vulnerable code is actually used
  - Assess impact level (No impact, Partial, Full)
- Format as:
  - CVE number with link to vulnerability database
  - Brief description
  - Impact analysis

#### Change Categories (Auto-detected)
- **New Features**: New functionality added
- **Improvements**: Library upgrades, performance improvements
- **Defect Fixes**: Issues resolved with JIRA references
- **Breaking Changes**: Changes that require user action
- **Deprecation**: Features marked for future removal

#### Version Information
- Source options:
  1. Git tag (e.g., v2.22.0, 2.22.0, 1.19.0)
  2. Jira version field
  3. Manual input
- Extract semantic version format (major.minor.patch)
- Display prominently at top of release notes

#### JIRA Integration
- Extract task numbers from branch names/commits
- Link defect fixes to JIRA tickets
- Format: "PRND-XXXXX Description"

### Service-Based Release Notes Logic
- Epic Structure Handling:
  - Epic task may contain stories from multiple projects/services
  - Each story is linked to a specific GitHub repository (service)
  - Stories are fetched and grouped by their service/repository
- Release Notes per Service:
  - Generate independent release notes for each service
  - Each service's release notes include:
    - Epic-level context
    - Service-specific stories
    - Code changes from service-specific branches
    - AI-generated summaries for that service
- Processing Order:
  1. Identify all unique services (GitHub repositories) from Epic stories
  2. For each service:
     - Filter stories belonging to that service
     - Fetch code changes from service's GitHub repository
     - Generate AI summaries for service-specific changes
     - Create release notes for that service
  3. Present all service release notes to user
  4. User can publish individual service notes or combine them (future feature)

### APIs & Integrations
- **Jira API**: REST API for reading issues
  - Authentication (API token / OAuth)
  - Issue search by JQL
  - Get issue details
- **GitHub API**: REST API for repository access
  - Authentication (Personal Access Token)
  - List repositories
  - List branches
  - Get commits and diffs
  - Get tags (for version detection)
  - Get specific file contents (for configuration files)

### Data Flow

#### Step 1: User Input
**Action:** User enters Jira task numbers/filters in web UI

**Input Data:**
- Single task number (e.g., "PRND-1234")
- Multiple task numbers (comma-separated or bulk upload)
- JQL filter (e.g., "project = PRND AND labels = Saturn_2025_Q4")
- Additional options (optional):
  - Version number (manual or auto-detected)
  - Release date (defaults to today)
  - Author (defaults to current user)
  - Release name

**Output:**
- Structured request object
- Job created in background queue
- Job ID returned to user for progress tracking

**Error Handling:**
- Invalid Jira key format: Show validation error immediately
- Invalid JQL syntax: Show validation error immediately
- No input provided: Show "Please enter task number or JQL filter"

---

#### Step 2: Fetch Jira Task Data
**Action:** Application fetches task data from Jira (Epic + all child stories if task is Epic)

**API Calls:**
- If single task: `GET /rest/api/2/issue/{key}`
- If multiple tasks: `POST /rest/api/2/search` with JQL
- If Epic task:
  - Fetch Epic: `GET /rest/api/2/issue/{epicKey}`
  - Fetch child stories: `POST /rest/api/2/search` with JQL "parent = {epicKey}"

**Input Data:**
- Jira task key(s) or JQL filter

**Fetched Data:**
- Task ID and summary
- Description
- Epic information (if any)
- Assignee/Developer
- Status
- Labels
- Project name
- Task type (Story, Epic, Task, Bug, etc.)
- Component (service name)
- Scrum team
- Acceptance criteria (if available)
- Comments
- Dependent tasks (blocked-by, blocking)

**Data Transformation:**
- Normalize Jira API response to internal data model
- Extract relevant fields only
- Handle missing fields gracefully

**Error Handling:**
- Retry strategy: 3 attempts with exponential backoff (1s, 2s, 4s)
- Authentication error: Show "Invalid Jira credentials" to user
- Task not found: Show "Task {key} not found" to user
- JQL syntax error: Show "Invalid JQL: {error_message}" to user
- Rate limit exceeded: Wait and retry, show "Jira rate limit hit, retrying..."
- Network error: Retry, show "Failed to connect to Jira, retrying..."
- After 3 failed attempts: Show detailed error message to user with specific reason

---

#### Step 3: Map Jira Tasks to GitHub Repositories
**Action:** Application maps Jira tasks to GitHub repositories by project name/task number

**Mapping Logic:**
- Primary: Use Jira component field as GitHub repository name
- Secondary: Use Jira project name to identify GitHub organization
- Fallback: Parse task number from branch names (e.g., "PRND-1234-feature-branch")

**Input Data:**
- Jira task data from Step 2

**Mapping Rules:**
- Component = "product-catalog" → GitHub repo: "product-catalog"
- Project = "PRND" → GitHub org: "company-prnd"
- Task PRND-1234 → Search for branches containing "1234"

**Output:**
- List of (task_key, repository_name, organization) mappings
- Tasks that couldn't be mapped (marked for manual intervention)

**Error Handling:**
- No GitHub repository found: Mark task as "Cannot map to repository"
- Multiple matches: Show to user for manual selection

---

#### Step 4: Find GitHub Branches
**Action:** Application finds branches associated with tasks

**API Calls:**
- `GET /repos/{org}/{repo}/branches`

**Input Data:**
- GitHub organization and repository names from Step 3
- Task numbers to search for

**Branch Detection Logic:**
- Search for branches containing task number (e.g., "1234")
- Common branch naming patterns:
  - "PRND-1234-feature-name"
  - "feature/PRND-1234"
  - "1234-add-new-endpoint"
  - "hotfix/PRND-1234"

**Output:**
- List of branches per task
- Branch name, author, last commit SHA

**Data Transformation:**
- Normalize branch names
- Extract task number from branch name if needed

**Error Handling:**
- Retry strategy: 3 attempts with exponential backoff (1s, 2s, 4s)
- Repository not found: Show "GitHub repository {repo} not found"
- No branches found for task: Show "No branches found for task {key}, assuming task has no code changes yet"
- Authentication error: Show "Invalid GitHub credentials"
- After 3 failed attempts: Show detailed error message to user

---

#### Step 5: Fetch GitHub Code Changes
**Action:** Application fetches code changes from GitHub

**API Calls:**
- `GET /repos/{org}/{repo}/commits?sha={branch}`
- `GET /repos/{org}/{repo}/commits/{sha}`
- `GET /repos/{org}/{repo}/git/refs/tags` (for version detection)
- `GET /repos/{org}/{repo}/contents/{path}` (for specific files)

**Input Data:**
- Branches from Step 4

**Fetched Data:**
- **Commits and diffs:**
  - Commit SHA
  - Commit message
  - Author
  - Changed files
  - Diff content (unified diff format)
- **Git tags (for version detection):**
  - Tag names
  - Tag SHAs
  - Tag dates
- **File changes (filtered by type):**
  - Configuration files: application.yml, .env, config/*.yml
  - Database migrations: db/migration/*.sql, db/changelog/*.xml
  - DevOps files: Dockerfile, docker-compose.yml, deployment.yaml
  - Dependency files: pom.xml, package.json, requirements.txt

**Data Transformation:**
- Filter files by type (config, migration, devops, dependency)
- Extract relevant content from diffs
- Store raw diffs for AI analysis

**Error Handling:**
- Retry strategy: 3 attempts with exponential backoff (1s, 2s, 4s)
- Branch not found: Show "Branch {branch} not found, possibly deleted"
- Rate limit exceeded: Wait and retry
- Network error: Retry
- After 3 failed attempts: Show detailed error message to user

---

#### Step 6: AI Analysis
**Action:** AI analyzes code changes and generates summaries

**Input Data:**
- Code diffs from Step 5
- Jira task data from Step 2

**Analysis Tasks:**
- Code change summarization (business language for PMs)
- Change categorization (New Feature, Improvement, Defect Fix, Breaking Change, Deprecation)
- Impact analysis per category (Database, API, UI, Performance, Business Logic)
- Configuration change detection and formatting
- Database migration detection
- DevOps change detection
- Library upgrade detection
- Security/CVE analysis
- JIRA reference extraction

**AI API Calls:**
- Call OpenAI GPT-4o or Anthropic Claude 3.5
- Multiple prompts for different analysis types
- Or single comprehensive prompt

**Output Data:**
```json
{
  "summary": "Business-friendly summary (2-3 sentences)",
  "category": "New Feature",
  "confidence": 0.92,
  "impact": {
    "database": "...",
    "api": "...",
    "ui": "...",
    "performance": "...",
    "business_logic": "..."
  },
  "configuration_changes": [...],
  "database_migrations": [...],
  "devops_changes": [...],
  "library_upgrades": [...],
  "cves": [...],
  "jira_tickets": ["PRND-1234"]
}
```

**Data Transformation:**
- Parse AI response
- Validate categories and confidence scores
- Format configuration changes into YAML/Env examples
- Extract CVE numbers with links

**Error Handling:**
- Retry strategy: 3 attempts with exponential backoff (2s, 5s, 10s)
- AI API rate limit: Wait and retry
- AI API quota exceeded: Show "AI quota exceeded, please try again later or upgrade plan"
- AI API error: Retry
- Invalid response from AI: Retry with different prompt
- After 3 failed attempts: Show "Failed to analyze changes with AI, please try again or contact support" and allow manual completion option

---

#### Step 7: Group Tasks by Service
**Action:** Application groups tasks/stories by service (GitHub repository)

**Input Data:**
- AI analysis results from Step 6
- Jira task data from Step 2
- GitHub repository mappings from Step 3

**Grouping Logic:**
- Create groups by GitHub repository name
- Each group = One service's release notes
- Add Epic-level context to all service groups (if Epic)

**Output:**
```json
{
  "product-catalog": {
    "service_name": "product-catalog",
    "version": "2.22.0",
    "stories": [...],
    "changes": [...],
    "ai_analyses": [...]
  },
  "user-service": {
    "service_name": "user-service",
    ...
  }
}
```

**Data Transformation:**
- Merge analyses for same service
- Calculate service-level version (from Git tags)
- Group AI analyses by change category

**Error Handling:**
- No groups created: Show "No code changes found for any service"
- Empty service groups: Mark as "No changes"

---

#### Step 8: Generate Release Notes
**Action:** Application generates service-specific release notes for each unique service

**Input Data:**
- Grouped services from Step 7

**Generation Process:**
For each service:
1. Apply Confluence-style template
2. Fill 10 standard sections:
   - Version Information (service name, version, date, author)
   - New Features
   - Improvements
   - Defect Fixes (with JIRA references)
   - Configuration Changes (YAML/Env examples)
   - Breaking Changes
   - Database Migrations
   - Known Issues/CVEs
   - DevOps Notes
   - Support info
3. Fill empty sections with "None for this release."
4. Format as Markdown

**Output:**
- Markdown content for each service
- JSON structure for UI rendering
- Save to database

**Data Transformation:**
- AI analyses → Categorized sections
- Configuration changes → YAML/Env formats
- CVEs → Formatted with links
- JIRA tickets → Linked with task IDs

**Error Handling:**
- Template rendering error: Use fallback template
- Save to database error: Show "Failed to save release notes" but still display to user

---

#### Step 9: Display to User
**Action:** Display all service release notes in web UI for review/edit

**Input Data:**
- Generated release notes from Step 8

**UI Display:**
- Show all services in tabs or accordion
- Each service's release notes rendered in Markdown editor
- Allow editing of each section
- Show preview mode
- Auto-save drafts

**User Actions:**
- Edit release notes
- Add/remove sections
- Change categorization
- Add manual entries

**Error Handling:**
- Rendering error: Show raw Markdown
- Save error: Show "Auto-save failed" warning

---

#### Step 10: Export
**Action:** User can export each service's release notes individually

**Input Data:**
- Edited release notes from UI

**Export Options:**
- Markdown (.md)
- HTML (.html)
- PDF (.pdf)
- Word (.docx)

**Process:**
1. Convert Markdown to target format
2. Generate file
3. Download to user's device

**Error Handling:**
- Conversion error: Show "Failed to convert to {format}"
- Download error: Retry download button

---

### Overall Error Handling Strategy

#### Retry Logic
- All external API calls (Jira, GitHub, AI): 3 retries
- Exponential backoff: 1s → 2s → 4s (Jira/GitHub), 2s → 5s → 10s (AI)
- After 3 failures: Stop and show error to user

#### Error Messages to User
- Always show specific reason for failure
- Include helpful suggestions (e.g., "Check your API credentials")
- Provide retry button
- Allow manual completion where possible

#### Progress Updates
- Update job progress after each step
- Show current operation (e.g., "Fetching Jira tasks...", "Analyzing code changes...")
- Show percentage for multi-service processing
- Update UI in real-time via WebSocket or polling

#### Fallback Mechanism
- If AI fails: Allow user to complete release notes manually
- If Jira fails: Allow manual entry of task details
- If GitHub fails: Allow manual code change description
- If export fails: Allow copy to clipboard as fallback

### AI Capabilities Needed

#### Natural Language Understanding
- **Capability:** Understand Jira task descriptions, comments, and acceptance criteria
- **Implementation:** Use LLM's native NLP capability (no external NLP libraries needed)
- **Analysis Tasks:**
  - Extract key requirements from task description
  - Understand business context and goals
  - Identify technical requirements
  - Extract component/service names
  - Understand relationships between tasks (blocked-by, blocking)
  - Extract acceptance criteria and their implications
- **LLM Usage:** GPT-4o or Claude 3.5 can understand complex natural language natively

#### Code Analysis (Git Diff Understanding)
- **Capability:** Understand Java code changes from Git diffs
- **Implementation:** Direct LLM diff analysis (no external AST parsing tools needed)
- **Analysis Tasks:**
  - Understand unified diff format
  - Parse Java code changes
  - Recognize Spring Boot annotations (@RestController, @Service, @Entity, etc.)
  - Understand JPA/Hibernate entity changes
  - Detect REST endpoint modifications
  - Understand DTO/Model changes
  - Identify exception handling modifications
- **LLM Usage:** GPT-4o and Claude 3.5 have strong code understanding capabilities
- **Advantage:** No need for JavaParser, Spoon, or other AST tools - reduces complexity

#### Summarization (Business Language)
- **Capability:** Generate summaries in business language for Product Managers
- **Summary Length:** Medium
  - Main summary: 2-3 sentences
  - Multiple changes: Bullet points (3-5 items max)
  - Not too short (incomplete information)
  - Not too long (overwhelming)
- **Summary Approach:**
  - Focus on business value delivered
  - Avoid technical jargon
  - Explain impact on end users
  - Use simple, clear language
  - Provide concrete examples when helpful
- **Example Conversion:**
  - Technical: "Added @GetMapping('/api/v1/orders/{id}') in OrderController and implemented OrderService.getOrderById(id)"
  - Business: "Added new API endpoint to retrieve order details by order ID"
  - Technical: "Updated ProductEntity with boolean field 'isActive' and modified ProductRepository.addIsActiveColumn()"
  - Business: "Added ability to mark products as active or inactive for better inventory management"

#### Categorization (with Confidence Score)
- **Capability:** Categorize changes into: New Feature, Improvement, Defect Fix, Breaking Change, Deprecation
- **Implementation:** Calculate confidence score for each category
- **Confidence Score:**
  - Range: 0.0 to 1.0
  - Threshold: 0.7 (categories below threshold marked as "Uncertain")
  - Score calculation based on:
    - JIRA task type (Bug → Defect Fix, Epic → New Feature, etc.)
    - Commit message keywords ("fix", "bug", "feature", "improve", etc.)
    - Code change patterns (new file → New Feature, modifications → Improvement, etc.)
    - JIRA labels ("critical", "hotfix", "enhancement", etc.)
- **Category Selection:** Choose category with highest confidence score
- **Edge Case:** If multiple categories have similar scores (difference < 0.1), mark as "Requires Manual Review"
- **Output Format:**
  ```json
  {
    "category": "New Feature",
    "confidence": 0.92,
    "alternatives": [
      {"category": "Improvement", "confidence": 0.78},
      {"category": "Defect Fix", "confidence": 0.12}
    ]
  }
  ```

#### Configuration Change Detection
- **Capability:** Identify and format configuration changes
- **File Types:** application.yml, application.properties, .env, config/*.yml, config/*.properties
- **Detection Tasks:**
  - Identify new parameters added
  - Identify modified parameters
  - Identify deprecated parameters (removed)
  - Group related configuration changes
- **Formatting:**
  - Environment variable examples with default values
  - YAML configuration snippets
  - Clear marking of deprecated parameters
- **AI Analysis:**
  - Understand parameter purpose from comments
  - Explain configuration impact
  - Provide migration guidance if needed

#### Security Analysis (CVE Detection)
- **Capability:** Detect CVE numbers and assess security impact
- **Detection Sources:**
  - JIRA task descriptions
  - Commit messages
  - Pull request descriptions
  - Dependency files (Maven pom.xml, etc.)
- **Analysis Tasks:**
  - Extract CVE numbers (format: CVE-YYYY-NNNNN)
  - Search vulnerability database (optional)
  - Analyze affected code:
    - Check if vulnerable code is actually used
    - Determine if application is vulnerable
  - Generate impact assessment:
    - "No impact expected, affected code not used"
    - "Partial impact, limited scope"
    - "Full impact, action required"
- **Output Format:**
  - CVE number with link to NVD (National Vulnerability Database)
  - Brief description of vulnerability
  - Impact assessment
  - Recommended actions (if any)

#### Database Migration Detection
- **Capability:** Identify SQL migration files
- **File Types:** db/migration/*.sql (Flyway), db/changelog/*.xml (Liquibase), custom scripts
- **Analysis Tasks:**
  - Extract migration descriptions
  - List schema changes:
    - Tables added/modified/dropped
    - Columns added/modified/dropped
    - Index changes
    - Constraints changes
  - Identify data migration requirements
  - Note potential breaking changes
- **AI Analysis:**
  - Understand migration purpose
  - Explain business impact of schema changes
  - Highlight backward incompatible changes

#### DevOps Change Detection
- **Capability:** Identify infrastructure and deployment changes
- **File Types:**
  - Dockerfile, docker-compose.yml
  - Kubernetes: deployment.yaml, service.yaml, ingress.yaml
  - Helm: Chart.yaml, values.yaml
  - CI/CD: .github/workflows/*.yml, Jenkinsfile, GitLab CI
- **Analysis Tasks:**
  - Extract deployment requirements
  - Note environment-specific changes
  - Identify resource requirement changes (CPU, memory)
  - Highlight configuration changes affecting deployment

#### Library Upgrade Detection
- **Capability:** Identify dependency version upgrades
- **File Types:** pom.xml (Maven), package.json (npm), requirements.txt (Python), build.gradle (Gradle)
- **Analysis Tasks:**
  - Extract old and new versions
  - Summarize version upgrades
  - Identify major version bumps (potential breaking changes)
  - Note security patch upgrades
  - Explain why upgrade was needed (from commit context)
- **Output Format:**
  - Library name
  - Old version → New version
  - Change type (major, minor, patch)
  - Brief description of upgrade purpose

#### Version Detection
- **Capability:** Extract version from Git tags
- **Tag Formats Supported:**
  - v2.22.0 (with 'v' prefix)
  - 2.22.0 (semantic versioning)
  - 1.19.0 (simple versioning)
- **Parsing:** Extract semantic version components (major.minor.patch)
- **Fallback:** If no tag found, use Jira version field or manual input

#### JIRA Integration
- **Capability:** Extract and link JIRA information
- **Tasks:**
  - Extract JIRA task numbers from commit messages (pattern: [A-Z]+-\d+)
  - Link defect fixes to JIRA tickets
  - Extract release information from JIRA labels (e.g., "Saturn_2025_Q4" → 2025 Q4 Release)
  - Extract component name (service name)
  - Extract scrum team information
  - Extract dependent tasks (blocked-by, blocking)
  - Use JIRA context to understand business requirements

## User Stories

### As a Release Manager
- I want to enter Jira task numbers to see all related code changes
- I want to automatically generate service-specific release notes from Jira tickets and GitHub commits
- I want to see separate release notes for each service when an Epic spans multiple services
- I want to customize each service's release notes before publishing

### As a Developer
- I want my code changes to be automatically summarized in release notes
- I want release notes to reflect the actual changes I made

### As a Stakeholder
- I want clear, understandable release notes that explain what changed
- I want release notes that link back to original Jira tasks

## Example Scenario

### Epic: Snapshot Data Integration
- **Jira Epic**: PRND-1234 "Snapshot data integration"
- **Total Stories**: 40 stories
- **Affected Services**: 10 different GitHub repositories
  - product_catalog
  - user_service
  - order_service
  - inventory_service
  - payment_service
  - notification_service
  - analytics_service
  - search_service
  - cache_service
  - api_gateway

### Release Notes Generation Process
1. User enters Epic PRND-1234
2. Application fetches Epic and all 40 stories
3. Application identifies 10 unique services from story metadata
4. For **product_catalog** service:
   - Find 5 stories related to product_catalog
   - Find branches: PRND-1234-product-catalog-1, PRND-1234-product-catalog-2
   - Fetch code changes from product_catalog repository
   - Generate release notes for product_catalog
5. Repeat for remaining 9 services
6. Display 10 separate release notes in UI
7. Release Manager reviews and publishes each service's release notes

### Sample Service Release Note: product_catalog
```
# Product Catalog Management
Version: 2.22.0

## Changes

### New Feature
A new rule type, implicitEligibility, has been introduced in the Rule Engine.

Previously, only offering eligibility rules were executed when listing offerings. With this enhancement, implicitEligibility rules are now also executed during offering listings.

Each implicitEligibility rule includes an assetGroup (see the Rule Engine release notes for details), which defines the entities to which the rule applies.

This improvement allows users to create eligibility rules that apply to multiple offerings simultaneously—without the need to patch or reference the rule directly in each Product Offering.
The rules are fully managed and executed within the Rule Engine service.

The final response is now generated by combining results from both eligibility and implicitEligibility rules.

## Configuration Changes

- drules.url is changed to drules.rule-engine-url
- drules.refresh is changed to drules.refresh-ms
- implicitEligibility option is added to DRULES_RULE_CATEGORY

```yaml
DRULES_RULE_ENGINE_URL: http://rule-engine/api/ruleEngine/v1
DRULES_ENABLED: true
DRULES_RULE_CATEGORY: eligibility,implicitEligibility
DRULES_REFRESH_MS: 60000
```

```yaml
drules:
  rule-engine-url: ${DRULES_RULE_ENGINE_URL}
  refresh-ms: ${DRULES_REFRESH_MS}
  rule-category: ${DRULES_RULE_CATEGORY}
  enabled: ${DRULES_ENABLED}
```

## Known Issues

- **CVE-2025-41248** Spring Security authorization bypass for method security annotations on parameterized types: No impact is expected, affected codes are not used
- **CVE-2025-41249** Spring Framework Annotation Detection Vulnerability: No impact is expected, affected codes are not used
- **CVE-2025-55752** Relative Path Traversal Vulnerability: No impact is expected, affected codes are not used
```

### Sample Service Release Note: Service Catalog (Full Confluence Style)
```
# Service Catalog 1.19.0 2025 Q4 Release

## Version Information
**Release Notes:** Service Catalog
**Version:** 1.19.0
**Release Date:** 26/12/2025

## 1. New Features
None for this release.

## 2. Improvements
Spring Boot upgrade to 3.5.8

## 3. Defect Fixes
- **PRND-40370** A validation defect has been resolved where the lifecycleStatus field could be set to invalid values during PATCH operations on ServiceCategory and ServiceCatalog entities. While POST operations correctly validated lifecycle status values, PATCH operations bypassed validation, allowing arbitrary invalid strings to be stored. Proper validation has now been implemented for all modification operations.

## 4. Configuration Changes
None for this release.

## 5. Breaking Changes
None for this release.

## 6. Database Migrations
None for this release.

## 7. Known Issues
- **CVE-2025-66566** A vulnerability found in lz4-java. The flaw allows disclosure of sensitive data through crafted compressed input due to insufficient clearing of output buffers in Java-based decompressor implementations.

## 8. DevOps Notes
None for this release.

## 9. Support
For any issues, visit our support portal
```

### Sample Service Release Note: With All Sections Populated
```
# Order Service 2.5.0 2025 Q1 Release

## Version Information
**Release Notes:** Order Service
**Version:** 2.5.0
**Release Date:** 31/03/2025

## 1. New Features
- Implemented real-time order tracking system
- Added webhook notifications for order status changes
- New API endpoint for bulk order operations

## 2. Improvements
- Java 17 upgrade from Java 11
- Spring Boot upgrade to 3.2.0
- Database connection pool optimization

## 3. Defect Fixes
- **PRND-41050** Fixed race condition in order status updates
- **PRND-41123** Resolved memory leak in order history retrieval

## 4. Configuration Changes
- New parameter added for webhook timeout
- Database connection pool settings changed

```yaml
WEBHOOK_TIMEOUT_MS: 5000
WEBHOOK_RETRY_COUNT: 3
```

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
```

## 5. Breaking Changes
- Order status enum values changed: `COMPLETED` renamed to `FULFILLED`
- Removed deprecated API endpoint `GET /api/v1/orders/archive`

## 6. Database Migrations
- Added new table `order_webhook_events`
- Updated `orders` table with new column `webhook_status`

```sql
ALTER TABLE orders ADD COLUMN webhook_status VARCHAR(50);
CREATE TABLE order_webhook_events (
    id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    event_type VARCHAR(50),
    payload JSONB,
    created_at TIMESTAMP
);
```

## 7. Known Issues
- **CVE-2025-12345** Jackson Databind vulnerability: No impact, custom ObjectMapper used
- **CVE-2025-67890** Netty HTTP/2 vulnerability: No impact, HTTP/1.1 only

## 8. DevOps Notes
- Docker image size reduced by 30%
- New deployment requires Kubernetes 1.28+
- Memory requirements increased to 512MB minimum

## 9. Support
For any issues, visit our support portal
```



## Non-Functional Requirements

### Performance
- Fetch and analyze 50 tasks within 30 seconds
- Web UI should respond within 1 second for user interactions

### Security
- Secure storage of API tokens (encrypted)
- HTTPS required for all communications
- No sensitive data logged

### Reliability
- Handle API rate limits gracefully
- Retry failed requests with exponential backoff
- Show clear error messages to users

## Future Enhancements (Optional)
- Scheduled release notes generation
- Integration with Slack/Teams notifications
- Release notes templates
- Multi-language support
- Historical release notes archive

## Documentation

### User Documentation
- Getting started guide
- User manual
- Video tutorials
- FAQ

### Developer Documentation
- API documentation (Swagger/OpenAPI)
- Architecture overview
- Setup guide
- Contributing guide

### Release Notes
- Changelog for application
- Version history
- Migration guides

## Backend API Design

### REST API Endpoints

#### Release Notes Endpoints
```
POST   /api/release-notes/generate
GET    /api/release-notes
GET    /api/release-notes/{id}
PUT    /api/release-notes/{id}
DELETE /api/release-notes/{id}
GET    /api/release-notes/{id}/export/{format}
```

#### Job Status Endpoints
```
GET    /api/jobs/{jobId}
GET    /api/jobs/{jobId}/status
POST   /api/jobs/{jobId}/cancel
```

### Request/Response Schemas
- Standard response format:
  ```json
  {
    "success": true,
    "data": {...},
    "message": "Success"
  }
  ```
- Error response format:
  ```json
  {
    "success": false,
    "data": null,
    "message": "Error description",
    "errors": [...],
    "code": "ERROR_CODE"
  }
  ```

### Background Job Processing

#### Why Background Jobs?
Large epics can take 1-2+ minutes to process:
- Jira fetch: 40 stories (5-10s)
- GitHub fetch: 10 services × (branch + commits + diffs + files) (30-50s)
- AI analysis: 40 stories × AI processing (30-60s)
- Release notes generation: 10 services (5s)
**Total:** 90-120+ seconds

Without background jobs: User sees frozen screen for 2+ minutes
With background jobs: User sees progress bar and can navigate away

#### Job Types
```python
class JobType(Enum):
    FETCH_JIRA_ISSUES = "fetch_jira_issues"
    FETCH_GITHUB_CHANGES = "fetch_github_changes"
    AI_ANALYZE_CHANGES = "ai_analyze_changes"
    GENERATE_RELEASE_NOTES = "generate_release_notes"
    GENERATE_ALL = "generate_all"  # Orchestrates all steps
```

#### Job Status States
```python
class JobStatus(Enum):
    PENDING = "pending"      # Job created, waiting to start
    RUNNING = "running"      # Job is currently executing
    COMPLETED = "completed"  # Job finished successfully
    FAILED = "failed"        # Job failed with error
    CANCELLED = "cancelled"  # Job cancelled by user
```

#### Job Data Structure
```python
{
    "id": "550e8400-e29b-41d4-a716-446655440000",  # UUID
    "type": "GENERATE_ALL",  # Job type
    "status": "running",     # Current status
    "progress": 45,         # 0-100 percentage
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
        "services": [...],  # Generated release notes
        "total_services": 10,
        "completed_services": 3
    },
    "error": null,
    "started_at": "2025-01-02T12:00:00Z",
    "updated_at": "2025-01-02T12:01:00Z",
    "completed_at": null
}
```

#### Database Schema (SQLite)
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

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created ON jobs(started_at DESC);
```

#### Job Queue Implementation
```python
import asyncio
import sqlite3
from typing import Optional
import json
from datetime import datetime

class JobQueue:
    """Database-backed job queue using SQLite"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database and create tables"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                status TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                current_step TEXT,
                input TEXT NOT NULL,
                result TEXT,
                error TEXT,
                started_at TIMESTAMP,
                updated_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    async def create_job(self, job_type: str, input_data: dict) -> str:
        """Create new job and return job ID"""
        import uuid
        job_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO jobs (id, type, status, input, started_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (job_id, job_type, "pending", json.dumps(input_data), now, now))
        conn.commit()
        conn.close()

        return job_id

    async def update_job(self, job_id: str, **kwargs):
        """Update job fields (progress, status, result, error, etc.)"""
        allowed_fields = {"status", "progress", "current_step", "result", "error", "completed_at"}

        updates = []
        values = []
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value if field != "completed_at" else datetime.utcnow().isoformat())

        if not updates:
            return

        values.append(datetime.utcnow().isoformat())  # updated_at
        values.append(job_id)

        query = f"UPDATE jobs SET {', '.join(updates)}, updated_at = ? WHERE id = ?"

        conn = sqlite3.connect(self.db_path)
        conn.execute(query, values)
        conn.commit()
        conn.close()

    async def get_job(self, job_id: str) -> Optional[dict]:
        """Get job by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "type": row[1],
            "status": row[2],
            "progress": row[3],
            "current_step": row[4],
            "input": json.loads(row[5]),
            "result": json.loads(row[6]) if row[6] else None,
            "error": row[7],
            "started_at": row[8],
            "updated_at": row[9],
            "completed_at": row[10]
        }

    async def cancel_job(self, job_id: str) -> bool:
        """Cancel job (if running or pending)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "UPDATE jobs SET status = ?, completed_at = ?, updated_at = ? WHERE id = ? AND status IN (?, ?)",
            ("cancelled", datetime.utcnow().isoformat(), datetime.utcnow().isoformat(), job_id, "pending", "running")
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    async def list_jobs(self, status: Optional[str] = None, limit: int = 10) -> list:
        """List recent jobs"""
        conn = sqlite3.connect(self.db_path)
        if status:
            cursor = conn.execute(
                "SELECT * FROM jobs WHERE status = ? ORDER BY started_at DESC LIMIT ?",
                (status, limit)
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM jobs ORDER BY started_at DESC LIMIT ?",
                (limit,)
            )
        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row) -> dict:
        return {
            "id": row[0],
            "type": row[1],
            "status": row[2],
            "progress": row[3],
            "current_step": row[4],
            "input": json.loads(row[5]),
            "result": json.loads(row[6]) if row[6] else None,
            "error": row[7],
            "started_at": row[8],
            "updated_at": row[9],
            "completed_at": row[10]
        }
```

#### Job Worker Implementation
```python
import asyncio
from typing import Optional

class JobWorker:
    """Background job worker for processing jobs"""

    def __init__(self, job_queue: JobQueue, jira_client, github_client, ai_service, release_notes_generator):
        self.queue = job_queue
        self.jira = jira_client
        self.github = github_client
        self.ai = ai_service
        self.generator = release_notes_generator
        self.running = False
        self.cancelled_jobs = set()

    async def start(self):
        """Start worker loop"""
        self.running = True
        while self.running:
            # Get next pending job
            job = await self._get_next_pending_job()
            if job:
                await self._process_job(job)
            else:
                # No jobs, wait before checking again
                await asyncio.sleep(1)

    async def _get_next_pending_job(self) -> Optional[dict]:
        """Get next pending job"""
        jobs = await self.queue.list_jobs(status="pending", limit=1)
        return jobs[0] if jobs else None

    async def _process_job(self, job: dict):
        """Process a single job"""
        job_id = job["id"]

        # Mark as running
        await self.queue.update_job(job_id, status="running", current_step="Starting...", progress=0)

        try:
            # Check if cancelled
            if job_id in self.cancelled_jobs:
                await self.queue.update_job(job_id, status="cancelled", current_step="Cancelled by user")
                self.cancelled_jobs.remove(job_id)
                return

            # Execute based on job type
            if job["type"] == "GENERATE_ALL":
                await self._generate_all(job)
            else:
                raise ValueError(f"Unknown job type: {job['type']}")

            # Mark as completed
            await self.queue.update_job(job_id, status="completed", progress=100, current_step="Completed")

        except Exception as e:
            # Mark as failed
            await self.queue.update_job(
                job_id,
                status="failed",
                current_step=f"Failed: {str(e)}",
                error=str(e)
            )
            logger.error(f"Job {job_id} failed: {e}", exc_info=True)

    async def cancel_job(self, job_id: str):
        """Cancel a running or pending job"""
        self.cancelled_jobs.add(job_id)
        success = await self.queue.cancel_job(job_id)
        return success

    async def _generate_all(self, job: dict):
        """Generate release notes (complete workflow)"""
        job_id = job["id"]
        input_data = job["input"]

        # Step 1: Fetch Jira tasks
        await self.queue.update_job(job_id, current_step="Fetching Jira tasks...", progress=5)
        await self._check_cancelled(job_id)
        jira_tasks = await self.jira.get_issues(input_data["jira_input"])

        # Step 2: Map to GitHub
        await self.queue.update_job(job_id, current_step="Mapping to GitHub repositories...", progress=10)
        await self._check_cancelled(job_id)
        github_mappings = self._map_to_github(jira_tasks)

        # Step 3: Fetch GitHub changes
        await self.queue.update_job(job_id, current_step="Fetching GitHub changes...", progress=20)
        await self._check_cancelled(job_id)
        github_changes = await self._fetch_github_changes(github_mappings)

        # Step 4: AI analysis (longest step, 40-60s)
        total_stories = len(jira_tasks)
        for i, story in enumerate(jira_tasks):
            await self.queue.update_job(
                job_id,
                current_step=f"AI analyzing {i+1}/{total_stories}...",
                progress=20 + int((i / total_stories) * 40)  # 20-60%
            )
            await self._check_cancelled(job_id)
            await self.ai.analyze_code(story["diff"], story["jira_context"])

        # Step 5: Generate release notes
        await self.queue.update_job(job_id, current_step="Generating release notes...", progress=80)
        await self._check_cancelled(job_id)
        release_notes = await self.generator.generate(github_changes, jira_tasks)

        # Step 6: Save results
        await self.queue.update_job(
            job_id,
            result=release_notes,
            current_step="Saving results...",
            progress=90
        )

    async def _check_cancelled(self, job_id: str):
        """Check if job was cancelled"""
        if job_id in self.cancelled_jobs:
            await self.queue.update_job(job_id, status="cancelled", current_step="Cancelled")
            self.cancelled_jobs.remove(job_id)
            raise JobCancelledException("Job was cancelled")

    def stop(self):
        """Stop worker loop"""
        self.running = False


class JobCancelledException(Exception):
    """Exception raised when job is cancelled"""
    pass
```

#### Progress Update Mechanism

##### Frontend Polling (Simple)
```javascript
// Poll for job status every 1 second
async function pollJobStatus(jobId) {
    const pollInterval = setInterval(async () => {
        const response = await fetch(`/api/jobs/${jobId}`);
        const job = await response.json();

        updateProgressUI(job);

        if (job.status === 'completed' || job.status === 'failed' || job.status === 'cancelled') {
            clearInterval(pollInterval);
            showResults(job);
        }
    }, 1000);
}
```

##### WebSocket (Real-time, better UX)
```python
# Backend WebSocket handler
from fastapi import WebSocket

@app.websocket("/ws/jobs/{job_id}")
async def job_updates(websocket: WebSocket, job_id: str):
    await websocket.accept()

    # Send initial job state
    job = await job_queue.get_job(job_id)
    await websocket.send_json(job)

    # Subscribe to job updates
    async for update in job_queue.subscribe(job_id):
        await websocket.send_json(update)

        if update["status"] in ["completed", "failed", "cancelled"]:
            await websocket.close()
```

```javascript
// Frontend WebSocket connection
const ws = new WebSocket(`ws://localhost:8000/ws/jobs/${jobId}`);

ws.onmessage = (event) => {
    const job = JSON.parse(event.data);
    updateProgressUI(job);

    if (job.status === 'completed' || job.status === 'failed' || job.status === 'cancelled') {
        ws.close();
        showResults(job);
    }
};
```

#### API Endpoints

```python
from fastapi import FastAPI, BackgroundTasks
from .job_queue import JobQueue, JobWorker
from .workflow import WorkflowService

app = FastAPI()
job_queue = JobQueue("jobs.db")
worker = JobWorker(job_queue, jira_client, github_client, ai_service, release_notes_generator)

# Start worker in background
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker.start())

@app.on_event("shutdown")
async def shutdown_event():
    worker.stop()

# Create job
@app.post("/api/release-notes/generate")
async def generate_release_notes(request: GenerateRequest):
    """Start new release notes generation job"""
    job_id = await job_queue.create_job("GENERATE_ALL", request.dict())
    return {"success": True, "job_id": job_id}

# Get job status
@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    """Get job status"""
    job = await job_queue.get_job(job_id)
    if not job:
        return {"success": False, "message": "Job not found"}
    return {"success": True, "data": job}

# Get job status (simplified)
@app.get("/api/jobs/{job_id}/status")
async def get_job_status(job_id: str):
    """Get simplified job status"""
    job = await job_queue.get_job(job_id)
    if not job:
        return {"success": False, "message": "Job not found"}

    return {
        "success": True,
        "data": {
            "status": job["status"],
            "progress": job["progress"],
            "current_step": job["current_step"]
        }
    }

# Cancel job
@app.post("/api/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a job"""
    success = await worker.cancel_job(job_id)
    if success:
        return {"success": True, "message": "Job cancelled"}
    else:
        return {"success": False, "message": "Job not found or already completed"}
```

#### Job Cancellation Flow

```
1. User clicks "Cancel" button
2. Frontend sends POST /api/jobs/{job_id}/cancel
3. Backend:
   a. Adds job_id to cancelled_jobs set
   b. Updates job status to "cancelled" in database
   c. Worker checks cancelled_jobs on next iteration
   d. Raises JobCancelledException
   e. Job exits gracefully
4. Frontend shows "Job cancelled" message
```

#### Error Handling in Jobs

```python
try:
    await self._generate_all(job)
except JobCancelledException:
    # Job was cancelled, already marked as cancelled
    pass
except JiraAuthenticationError as e:
    await self.queue.update_job(
        job_id,
        status="failed",
        error=f"Jira authentication failed: {str(e)}"
    )
except GitHubRateLimitError as e:
    # Wait and retry
    await asyncio.sleep(60)  # Wait 1 minute
    await self._generate_all(job)  # Retry
except AIQuotaExceededError as e:
    await self.queue.update_job(
        job_id,
        status="failed",
        error=f"AI quota exceeded: {str(e)}. Please try again later."
    )
except Exception as e:
    logger.error(f"Job {job_id} failed unexpectedly: {e}", exc_info=True)
    await self.queue.update_job(
        job_id,
        status="failed",
        error=f"Unexpected error: {str(e)}"
    )
```

#### Job Cleanup
```python
# Clean up old jobs (older than 30 days)
import sqlite3
from datetime import datetime, timedelta

async def cleanup_old_jobs():
    """Delete jobs older than 30 days"""
    cutoff = (datetime.utcnow() - timedelta(days=30)).isoformat()
    conn = sqlite3.connect(self.db_path)
    conn.execute("DELETE FROM jobs WHERE started_at < ? AND status = 'completed'", (cutoff,))
    conn.commit()
    conn.close()
    logger.info("Cleaned up old jobs")
```

#### Progress Calculation Examples

```
Example: Epic with 40 stories, 10 services

Step 1: Fetch Jira tasks          -> 0-5%   (5%)
Step 2: Map to GitHub            -> 5-10%  (5%)
Step 3: Fetch GitHub changes       -> 10-20% (10%)
Step 4: AI Analysis (40 stories) -> 20-60% (40%)
  Story 1/40 -> 20.5%
  Story 20/40 -> 40%
  Story 40/40 -> 60%
Step 5: Generate release notes  -> 60-80% (20%)
Step 6: Save results             -> 80-90% (10%)
Step 7: Complete                 -> 100%

Total time: ~90-120 seconds
```

#### Multi-Job Support
```python
# Multiple jobs can run concurrently
# Worker processes one job at a time by default
# To support concurrent jobs, use multiple workers:

workers = [
    JobWorker(job_queue, ...),
    JobWorker(job_queue, ...),
    JobWorker(job_queue, ...)  # 3 workers, 3 concurrent jobs
]

for worker in workers:
    asyncio.create_task(worker.start())
```

## Data Persistence

### Database Schema
- Release notes table
- Jobs table
- Settings table

### Release Notes Storage
- Store release notes with metadata:
  - Service name
  - Version
  - Release date
  - Author
  - Generated date
  - Related Jira tasks
  - Content (JSON or Markdown)
- Local file storage (JSON format)

## Export Options

### Format Options
- **Markdown** (.md) - Default format
- **HTML** (.html) - Browser-viewable
- **PDF** (.pdf) - Professional output
- **Word** (.docx) - Office document format

### Download Options
- Single service download
- Bulk download (all services as ZIP)

## AI Model Integration

### Supported AI Providers

#### OpenAI
- **Models:** GPT-4o, GPT-4, GPT-3.5-turbo
- **Library:** `openai` Python package
- **Configuration:**
  ```bash
  AI_PROVIDER=openai
  OPENAI_API_KEY=sk-...
  OPENAI_MODEL=gpt-4o
  OPENAI_BASE_URL=https://api.openai.com/v1
  ```

#### Anthropic Claude
- **Models:** Claude-3-5-sonnet-20241022, Claude-3-opus-20240229, Claude-3-haiku-20240307
- **Library:** `anthropic` Python package
- **Configuration:**
  ```bash
  AI_PROVIDER=anthropic
  ANTHROPIC_API_KEY=sk-ant-...
  ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
  ```

#### Google Gemini
- **Models:** Gemini-1.5-pro, Gemini-1.5-flash, Gemini-1.0-pro
- **Library:** `google-generativeai` Python package
- **Configuration:**
  ```bash
  AI_PROVIDER=gemini
  GEMINI_API_KEY=...
  GEMINI_MODEL=gemini-1.5-pro
  ```

#### Groq (Default)
- **Models:** Llama-3-70b-versatile, Llama-3-8b-instant, Mixtral-8x7b-32768
- **Library:** `groq` Python package
- **Configuration:**
  ```bash
  AI_PROVIDER=groq
  GROQ_API_KEY=gsk_...
  GROQ_MODEL=llama-3-70b-versatile
  GROQ_BASE_URL=https://api.groq.com/openai/v1
  ```
- **Advantages:** Fast, cost-effective, good code understanding

### Default Configuration
- **Default Provider:** Groq
- **Default Model:** llama-3-70b-versatile
- **Fallback:** If Groq fails, automatically try OpenAI if configured

### Provider Selection Logic
1. Read `AI_PROVIDER` from environment variables
2. If not set, default to `groq`
3. Initialize appropriate client based on provider
4. Use provider-specific API key from environment variables

### Model Selection Guidelines

#### OpenAI Models
- **GPT-4o:** Best overall, expensive, excellent code analysis
- **GPT-4-turbo:** Good balance, cheaper than GPT-4o
- **GPT-3.5-turbo:** Fast, cheap, good for simple tasks

#### Anthropic Claude Models
- **Claude-3-5-Sonnet:** Excellent code analysis, cost-effective
- **Claude-3-Opus:** Most capable, expensive
- **Claude-3-Haiku:** Fast, cheap, good for simple tasks

#### Google Gemini Models
- **Gemini-1.5-pro:** Excellent multimodal, good for complex tasks
- **Gemini-1.5-flash:** Fast, cost-effective
- **Gemini-1.0-pro:** Stable, good for general tasks

#### Groq Models
- **Llama-3-70b-versatile:** Best overall on Groq
- **Llama-3-8b-instant:** Very fast, good for simple tasks
- **Mixtral-8x7b-32768:** Long context, good for large diffs

### Unified AI Service Interface

#### Client Initialization
```python
class AIService:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "groq")
        self.model = self._get_model()
        self.client = self._get_client()

    def _get_model(self):
        if self.provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4o")
        elif self.provider == "anthropic":
            return os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        elif self.provider == "gemini":
            return os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        elif self.provider == "groq":
            return os.getenv("GROQ_MODEL", "llama-3-70b-versatile")

    def _get_client(self):
        if self.provider == "openai":
            from openai import OpenAI
            return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            return genai.GenerativeModel(self.model)
        elif self.provider == "groq":
            from groq import Groq
            return Groq(api_key=os.getenv("GROQ_API_KEY"))
```

#### Unified Chat Completion
```python
async def analyze_code(self, diff_content: str, jira_context: dict) -> dict:
    """Unified method that works with all providers"""
    prompt = self._build_prompt(diff_content, jira_context)

    if self.provider in ["openai", "groq"]:
        # OpenAI-compatible API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    elif self.provider == "anthropic":
        # Anthropic API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.content[0].text)

    elif self.provider == "gemini":
        # Gemini API
        response = self.client.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json"
            }
        )
        return json.loads(response.text)
```

### Prompt Engineering

#### Provider-Specific Prompt Adaptations
- **OpenAI/Groq:** Use JSON response format for structured output
- **Anthropic:** Use max_tokens parameter, no native JSON mode
- **Gemini:** Use response_mime_type for JSON output

#### Base Prompt Template
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
  "confidence": 0.92,
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

### AI Cost Management

#### Token Usage Tracking
- Track input tokens per request
- Track output tokens per request
- Calculate cost based on provider pricing:
  - OpenAI: Input $0.005/1K, Output $0.015/1K (GPT-4o)
  - Anthropic: Input $0.003/1K, Output $0.015/1K (Claude 3.5 Sonnet)
  - Gemini: Input $0.00125/1K, Output $0.005/1K (Gemini 1.5 Pro)
  - Groq: Input $0.59/1M, Output $0.59/1M (Llama 3 70B) - Very cheap!

#### Cost Tracking Display
```json
{
  "total_requests": 15,
  "total_input_tokens": 45000,
  "total_output_tokens": 12000,
  "total_cost": 0.45,
  "cost_by_service": {
    "product-catalog": 0.20,
    "user-service": 0.15,
    "order-service": 0.10
  }
}
```

#### Cost Optimization Tips
- Use Groq by default (much cheaper)
- Cache results where possible
- Use smaller models for simple tasks
- Limit context size (truncate large diffs)
- Batch requests where possible

### Fallback Mechanism

#### Multi-Provider Fallback
```python
async def analyze_with_fallback(self, diff: str, context: dict) -> dict:
    """Try primary provider, fallback to secondary"""
    try:
        # Try primary provider (Groq by default)
        return await self.analyze(diff, context)
    except Exception as e:
        logger.error(f"Primary AI provider failed: {e}")

        # Fallback to OpenAI if configured
        if os.getenv("OPENAI_API_KEY"):
            logger.info("Falling back to OpenAI")
            original_provider = self.provider
            self.provider = "openai"
            self._reinit_client()
            try:
                result = await self.analyze(diff, context)
                self.provider = original_provider
                return result
            except Exception as e2:
                logger.error(f"Fallback provider also failed: {e2}")
                self.provider = original_provider
                self._reinit_client()

        # Manual completion fallback
        raise ManualCompletionRequiredException(
            "All AI providers failed, please complete manually"
        )
```

#### Retry Logic
- Retry failed requests (max 3 attempts)
- Exponential backoff: 2s → 5s → 10s
- Different backoff per provider:
  - OpenAI/Groq: 2s, 5s, 10s
  - Anthropic: 3s, 7s, 15s
  - Gemini: 4s, 10s, 20s

### Model Performance Comparison

| Model | Accuracy | Speed | Cost (per 1M tokens) | Best For |
|-------|----------|-------|----------------------|----------|
| GPT-4o | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $20 (in) / $60 (out) | Best overall |
| Claude 3.5 Sonnet | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $3 (in) / $15 (out) | Excellent value |
| Gemini 1.5 Pro | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $1.25 (in) / $5 (out) | Fast & cheap |
| Llama 3 70B (Groq) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0.59 (in) / $0.59 (out) | Very fast & cheap |

**Recommendation:** Start with Groq (Llama 3 70B) - best balance of speed, cost, and accuracy. Use OpenAI GPT-4o for complex cases if needed.

## Monitoring & Logging

### Application Logging
- Log levels:
  - ERROR: Critical errors
  - WARN: Warning messages
  - INFO: General information
  - DEBUG: Detailed debugging
- Log format:
  - Timestamp
  - Log level
  - Message
  - Stack trace (for errors)
- Log output:
  - Console (terminal)
  - File (optional)

### Health Check Endpoints
```
GET /health          # Basic health check
GET /health/ready    # Readiness check (dependencies)
```

## Testing Strategy

### Unit Tests
- Test coverage goal: 70%+
- Testing frameworks:
  - Python: pytest
- Test areas:
  - Business logic
  - Data validation
  - Configuration parsing
  - Utility functions

### Integration Tests
- Test external integrations:
  - Jira API (mocked for CI)
  - GitHub API (mocked for CI)
  - Database (SQLite for tests)

## Security Best Practices

### Input Validation
- Validate all user inputs
- Sanitize JQL queries
- Validate file uploads

### Code Security
- SQL injection prevention (use parameterized queries)
- XSS prevention (sanitize HTML output)
- CSRF protection (if forms are used)

### Dependency Scanning
- Regular vulnerability scanning
- Keep dependencies updated

## Configuration Management

### Environment Variables (.env)
All configuration managed via environment variables:

```bash
# ============================================
# Jira Configuration
# ============================================
JIRA_BASE_URL=https://your-jira-instance.atlassian.net
JIRA_API_TOKEN=your-jira-api-token
JIRA_USERNAME=your-email@company.com
JIRA_PROJECT_KEY=PRND

# ============================================
# GitHub Configuration
# ============================================
GITHUB_TOKEN=your-github-personal-access-token
GITHUB_ORG=your-organization

# ============================================
# AI Service Configuration
# ============================================
# AI Provider: openai | anthropic | gemini | groq
# Default: groq
AI_PROVIDER=groq

# OpenAI Configuration (if AI_PROVIDER=openai)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic Claude Configuration (if AI_PROVIDER=anthropic)
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Google Gemini Configuration (if AI_PROVIDER=gemini)
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-1.5-pro

# Groq Configuration (if AI_PROVIDER=groq) - Default
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1

# Fallback provider (if primary fails)
# Set to empty string to disable fallback
FALLBACK_AI_PROVIDER=openai

# ============================================
# Application Configuration
# ============================================
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false

# ============================================
# Database Configuration (SQLite by default)
# ============================================
DATABASE_URL=sqlite:///./release_notes.db

# ============================================
# Logging Configuration
# ============================================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# ============================================
# Cache Configuration (Optional)
# ============================================
CACHE_ENABLED=false
CACHE_TYPE=redis
CACHE_HOST=localhost
CACHE_PORT=6379
CACHE_DB=0
CACHE_TTL_SECONDS=3600
```

### Configuration File (.env.example)
Create `.env.example` file with default values:

```bash
# .env.example
AI_PROVIDER=groq
GROQ_MODEL=llama-3-70b-versatile
GROQ_API_KEY=gsk-your-api-key-here

FALLBACK_AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4o

JIRA_BASE_URL=https://your-jira.atlassian.net
JIRA_API_TOKEN=your-jira-token-here
JIRA_USERNAME=your-email@company.com
JIRA_PROJECT_KEY=PRND

GITHUB_TOKEN=ghp-your-github-token-here
GITHUB_ORG=your-organization

APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false
DATABASE_URL=sqlite:///./release_notes.db
LOG_LEVEL=INFO
```

### Setup Instructions
Before starting the application:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your API credentials:
   - Groq API key (recommended, cheapest and fast)
   - Fallback provider API key (optional, e.g., OpenAI)
   - Jira API token
   - GitHub personal access token

3. Get API keys:
   - **Groq:** https://console.groq.com/keys
   - **OpenAI:** https://platform.openai.com/api-keys
   - **Anthropic:** https://console.anthropic.com/settings/keys
   - **Gemini:** https://makersuite.google.com/app/apikey
   - **Jira:** https://id.atlassian.com/manage-profile/security/api-tokens
   - **GitHub:** https://github.com/settings/tokens

4. Choose AI provider:
   - For cheapest option: Set `AI_PROVIDER=groq` (default)
   - For best accuracy: Set `AI_PROVIDER=openai` with `OPENAI_MODEL=gpt-4o`
   - For good value: Set `AI_PROVIDER=anthropic` with `ANTHROPIC_MODEL=claude-3-5-sonnet-20241022`

5. Start application:
   ```bash
   python backend/main.py
   ```

6. Open web UI:
   ```
   http://localhost:8000
   ```

### Environment Validation
- Validate required environment variables on startup
- Show clear error messages for missing configuration
- Exit if required variables are missing
- Validate AI provider model availability
- Check API key formats (basic validation)

### Configuration Validation Rules

#### AI Provider Validation
- `AI_PROVIDER` must be one of: `openai`, `anthropic`, `gemini`, `groq`
- If `AI_PROVIDER` is not set, default to `groq`
- If provider is set but API key is missing, show error

#### API Key Validation
- **Groq:** Must start with `gsk_`
- **OpenAI:** Must start with `sk-`
- **Anthropic:** Must start with `sk-ant-`
- **Gemini:** Format varies (no strict validation)
- **Jira:** Token format varies
- **GitHub:** Must start with `ghp_`, `gho_`, `ghu_`, or `ghs_`

#### Error Messages
```
ERROR: Missing required environment variable 'GROQ_API_KEY'
Please set GROQ_API_KEY in .env file
Get your API key at: https://console.groq.com/keys

ERROR: Invalid AI_PROVIDER 'invalid'
Valid options are: openai, anthropic, gemini, groq
```

### Configuration Loader Implementation
```python
import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # AI Configuration
    ai_provider: str = Field(default="groq", env="AI_PROVIDER")
    fallback_ai_provider: Optional[str] = Field(default=None, env="FALLBACK_AI_PROVIDER")

    # Groq
    groq_api_key: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3-70b-versatile", env="GROQ_MODEL")
    groq_base_url: str = Field(default="https://api.groq.com/openai/v1", env="GROQ_BASE_URL")

    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    openai_base_url: str = Field(default="https://api.openai.com/v1", env="OPENAI_BASE_URL")

    # Anthropic
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")

    # Gemini
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-1.5-pro", env="GEMINI_MODEL")

    # Jira
    jira_base_url: str = Field(..., env="JIRA_BASE_URL")
    jira_api_token: str = Field(..., env="JIRA_API_TOKEN")
    jira_username: str = Field(..., env="JIRA_USERNAME")
    jira_project_key: str = Field(default="PRND", env="JIRA_PROJECT_KEY")

    # GitHub
    github_token: str = Field(..., env="GITHUB_TOKEN")
    github_org: str = Field(..., env="GITHUB_ORG")

    # Application
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")
    app_debug: bool = Field(default=False, env="APP_DEBUG")

    # Database
    database_url: str = Field(default="sqlite:///./release_notes.db", env="DATABASE_URL")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")

    def validate(self):
        """Validate configuration"""
        # Validate AI provider
        if self.ai_provider not in ["openai", "anthropic", "gemini", "groq"]:
            raise ValueError(f"Invalid AI_PROVIDER: {self.ai_provider}")

        # Check API keys
        if self.ai_provider == "groq" and not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is required when AI_PROVIDER=groq")
        if self.ai_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when AI_PROVIDER=openai")
        if self.ai_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when AI_PROVIDER=anthropic")
        if self.ai_provider == "gemini" and not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when AI_PROVIDER=gemini")

        # Check fallback
        if self.fallback_ai_provider and not self._has_api_key(self.fallback_ai_provider):
            raise ValueError(f"FALLBACK_AI_PROVIDER {self.fallback_ai_provider} has no API key")

    def _has_api_key(self, provider: str) -> bool:
        """Check if provider has API key configured"""
        key_map = {
            "openai": self.openai_api_key,
            "anthropic": self.anthropic_api_key,
            "gemini": self.gemini_api_key,
            "groq": self.groq_api_key,
        }
        return bool(key_map.get(provider))

# Usage
try:
    settings = Settings()
    settings.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file")
    exit(1)
```

## Cache Layer (Optional for Performance)

### Cache Strategy
Cache frequently accessed data to reduce API calls and improve response time.

### Cached Data Types
- **Jira Data:**
  - Project list
  - Issue types
  - Custom fields
  - Common JQL query results
- **GitHub Data:**
  - Repository list
  - Branch information
  - Commit metadata
- **Application Data:**
  - Release note templates
  - User preferences (future)

### Cache Technology
- **Redis** (Recommended)
  - Fast in-memory data store
  - Easy setup with Docker
  - Supports TTL (Time To Live)
  - Persistence option
- **Memcached** (Alternative)
  - Simple key-value store
  - No persistence
  - Faster but less features

### Cache Configuration
```bash
# .env configuration (Optional)
CACHE_ENABLED=true
CACHE_TYPE=redis
CACHE_HOST=localhost
CACHE_PORT=6379
CACHE_PASSWORD=
CACHE_DB=0
CACHE_TTL_SECONDS=3600
```

### Cache TTL (Time To Live)
- **Jira Data:** 1 hour (3600 seconds)
- **GitHub Data:** 30 minutes (1800 seconds)
- **Templates:** 24 hours (86400 seconds)
- **JQL Results:** 15 minutes (900 seconds)

### Cache Invalidation
- **Time-based:** Auto-expire after TTL
- **Event-based:** Invalidate on specific events:
  - New release notes generated
  - Configuration changed
  - Manual cache clear button in UI

### Cache Key Format
```
jira:project:list
jira:issue:types:PRND
github:repo:list:orgname
jql:project:PRND:team:SATURN:Q4-2025
```

### Cache Implementation
```python
# Example cache usage
from functools import lru_cache
from datetime import timedelta

# In-memory cache for simple cases
@lru_cache(maxsize=128)
def get_jira_projects():
    return jira_api.get_projects()

# Redis cache for distributed scenarios
import redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_with_cache(key, fetch_func, ttl=3600):
    cached = cache.get(key)
    if cached:
        return json.loads(cached)
    data = fetch_func()
    cache.setex(key, ttl, json.dumps(data))
    return data
```

### Cache Performance Metrics
- Cache hit rate
- Cache miss rate
- Memory usage
- Response time comparison (cached vs uncached)

### Cache Management UI
- Manual cache clear button
- View cache statistics
- Clear specific cache entries
- Cache hit/miss rate display

### When NOT to Use Cache
- Real-time data (e.g., current job status)
- User-specific data (if multiple users)
- Frequently changing data
- Small data sets (< 100KB)

### Implementation Notes
- Cache layer is optional for MVP
- Can be added later without code changes
- Use decorators for easy caching
- Graceful degradation if cache is unavailable

### Setup Instructions (Optional with Redis)
If using Redis for caching:

1. Install Redis:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server

   # macOS
   brew install redis
   ```

2. Start Redis:
   ```bash
   redis-server
   ```

3. Add cache configuration to `.env`
4. Install Redis client library:
   ```bash
   pip install redis
   ```

### Environment Validation
- Validate required environment variables on startup
- Show clear error messages for missing configuration
- Exit if required variables are missing
