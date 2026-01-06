# Jira Integration (Advanced) - Future Feature

## Overview
Direct integration with Jira for publishing release notes and creating issues.

## Features

### Add Comment to Issue
- Add release notes as comment to Jira issue
- Link back to generated release notes
- Format comment with Markdown
- Option to attach PDF export

### Create New Issue
- Create new Jira issue for release notes
- Issue type: Release Note, Documentation, or Custom
- Link to related Epic or Task
- Set custom fields

### Attach to Epic
- Link release notes to parent Epic
- Add comment to Epic with summary
- Include all service release notes in single comment
- Use Epic for grouping releases

## API Endpoints

### Publish to Jira (Add Comment)
```
POST /api/publish/jira/comment
```

**Request Body:**
```json
{
  "release_note_id": "uuid",
  "issue_key": "PRND-1234",
  "comment_format": "markdown",
  "attach_pdf": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "comment_id": "12345",
    "issue_key": "PRND-1234",
    "url": "https://your-jira.atlassian.net/browse/PRND-1234"
  }
}
```

### Publish to Jira (Create Issue)
```
POST /api/publish/jira/issue
```

**Request Body:**
```json
{
  "release_note_id": "uuid",
  "project_key": "PRND",
  "issue_type": "Documentation",
  "summary": "[Release Notes] Service Catalog 1.19.0",
  "description": "Release notes generated for...",
  "epic_key": "PRND-1234",
  "labels": ["release-notes", "q4-2025"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "issue_key": "PRND-5678",
    "issue_id": "123456",
    "url": "https://your-jira.atlassian.net/browse/PRND-5678"
  }
}
```

### Attach to Epic
```
POST /api/publish/jira/epic
```

**Request Body:**
```json
{
  "release_notes_ids": ["uuid1", "uuid2", "uuid3"],
  "epic_key": "PRND-1234",
  "comment_format": "markdown"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "comment_id": "12345",
    "epic_key": "PRND-1234",
    "url": "https://your-jira.atlassian.net/browse/PRND-1234"
  }
}
```

## Jira REST API Used

### Get Issue
```
GET /rest/api/2/issue/{issueKeyOrId}
```

### Add Comment
```
POST /rest/api/2/issue/{issueKeyOrId}/comment
```

### Create Issue
```
POST /rest/api/2/issue
```

### Get Issue Types
```
GET /rest/api/2/issuetype
```

### Get Custom Fields
```
GET /rest/api/2/field
```

## Comment Formatting

### Markdown Comment Example
```markdown
h2. Release Notes Generated

*Service:* Product Catalog
*Version:* 2.22.0
*Release Date:* 26/12/2025

h3. New Features
* A new rule type, implicitEligibility, has been introduced...

h3. Configuration Changes
{code:bash}
DRULES_RULE_ENGINE_URL: http://rule-engine/api/ruleEngine/v1
{code}

[View Full Release Notes|https://confluence.company.com/pages/123456]
```

### Epic Summary Comment
```markdown
h2. Release Notes Summary - Snapshot Data Integration (PRND-1234)

The following services have been updated as part of this epic:

* *Product Catalog* - [v2.22.0|https://confluence.company.com/pages/111]
* *User Service* - [v1.5.0|https://confluence.company.com/pages/222]
* *Order Service* - [v2.5.0|https://confluence.company.com/pages/333]

Total services: 10
Total stories: 40
Release date: 26/12/2025

[View All Release Notes|https://confluence.company.com/display/RN/Snapshot+Data+Integration]
```

## Configuration

### Jira API Configuration
```bash
# .env configuration
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_API_TOKEN=your-jira-api-token
JIRA_USERNAME=your-email@company.com
JIRA_PROJECT_KEY=PRND
JIRA_ISSUE_TYPE_DOCUMENTATION=Documentation
JIRA_ISSUE_TYPE_RELEASE_NOTE=Release Note
```

### Custom Fields (Optional)
```bash
# Custom field IDs for Jira
JIRA_CUSTOM_FIELD_VERSION=customfield_10100
JIRA_CUSTOM_FIELD_RELEASE_DATE=customfield_10101
JIRA_CUSTOM_FIELD_AUTHOR=customfield_10102
```

## Issue Type Mapping

### Default Issue Types
- **Documentation**: Standard documentation issue type
- **Task**: General task type
- **Release Note**: Custom issue type (if exists)

### Issue Type Detection
- Auto-detect available issue types from project
- Fall back to "Documentation" if "Release Note" not found
- Allow user to override default issue type

## Attachment Support

### Attach PDF to Comment
```
POST /rest/api/2/issue/{issueKeyOrId}/attachments
```

**Attach:**
- Generated PDF of release notes
- Markdown source file
- Optional: Export as Word

## Error Handling

### Common Errors
- **Issue Not Found**: Issue key doesn't exist
- **Permission Denied**: User doesn't have comment/create issue permission
- **Invalid Issue Type**: Issue type not available in project
- **Invalid Custom Field**: Custom field ID doesn't exist
- **Rate Limit**: Jira API rate limit exceeded

### Error Response Example
```json
{
  "success": false,
  "data": null,
  "message": "Issue not found",
  "errors": [
    {
      "code": "ISSUE_NOT_FOUND",
      "message": "Issue PRND-9999 does not exist"
    }
  ]
}
```

### Retry Logic
- Retry failed requests with exponential backoff
- Max 3 attempts
- Wait 1s, 2s, 4s between retries

## Implementation Notes

### Markdown to Jira Markup
- Convert Markdown to Jira's Wiki/Markdown format
- Handle code blocks (```language -> {code:language})
- Handle tables
- Preserve headings, lists, links

### Link Management
- Generate links to Confluence pages
- Link to Jira Epic/Task
- Use absolute URLs

### Comment Updates
- Add new comment instead of editing existing
- Include timestamp in comment
- Allow manual deletion of old comments

## Testing

### Test Scenarios
- Add comment to existing issue
- Create new issue with release notes
- Attach to Epic with multiple services
- Test with invalid issue key
- Test with permission denied

### Test Environment
- Use test project/space
- Don't publish to production Jira space
- Validate comment formatting
- Test attachment upload

## Future Enhancements

- Support for Jira Service Management (JSM)
- Create release notes as article in Confluence Knowledge Base
- Automatic Epic status update on publish
- Send email notifications to Epic watchers
- Generate release notes from Sprint completion
- Link Jira tasks directly to release note sections
