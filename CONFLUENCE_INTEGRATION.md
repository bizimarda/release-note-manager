# Confluence Integration - Future Feature

## Overview
Direct integration with Confluence for publishing release notes automatically.

## Features

### Create New Page
- Create a new Confluence page for release notes
- Page title format: `[Service Name] [Version] Release Notes`
- Parent page configurable
- Space configurable (e.g., "Release Notes" space)

### Update Existing Page
- Update existing Confluence page with new content
- Keep page history intact
- Add "Updated on [date]" comment
- Option to create version or overwrite

### Page Formatting
- Convert release notes to Confluence storage format (XHTML/Confluence markup)
- Preserve code blocks, tables, lists
- Add metadata:
  - Last updated timestamp
  - Author
  - Version
  - Related Jira epic/task links

### Attachments
- Attach PDF export of release notes
- Attach Markdown source file
- Attach related artifacts (optional)

### Space Configuration
```bash
# .env configuration
CONFLUENCE_BASE_URL=https://your-company.atlassian.net/wiki
CONFLUENCE_USERNAME=your-email@company.com
CONFLUENCE_API_TOKEN=your-confluence-api-token
CONFLUENCE_SPACE_KEY=RN
CONFLUENCE_PARENT_PAGE_ID=123456789
```

## API Endpoints

### Publish to Confluence
```
POST /api/publish/confluence
```

**Request Body:**
```json
{
  "release_note_id": "uuid",
  "service_name": "product_catalog",
  "version": "2.22.0",
  "options": {
    "create_new_page": false,
    "page_id": "987654321",
    "attachments": ["pdf", "md"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "page_url": "https://your-company.atlassian.net/wiki/pages/987654321",
    "page_id": "987654321",
    "version": 5
  }
}
```

## Confluence REST API Used

### Get Page
```
GET /wiki/rest/api/content/{id}
```

### Create Page
```
POST /wiki/rest/api/content
```

### Update Page
```
PUT /wiki/rest/api/content/{id}
```

### Add Attachment
```
POST /wiki/rest/api/content/{id}/child/attachment
```

### Get Space
```
GET /wiki/rest/api/space/{key}
```

## Page Template

### Confluence Storage Format Example
```xml
<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">Release Information</ac:parameter>
  <ac:rich-text-body>
    <p><strong>Service:</strong> Product Catalog</p>
    <p><strong>Version:</strong> 2.22.0</p>
    <p><strong>Release Date:</strong> 26/12/2025</p>
    <p><strong>Author:</strong> Release Manager</p>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>1. New Features</h2>
<p>A new rule type, implicitEligibility, has been introduced...</p>

<h2>2. Improvements</h2>
<p>None for this release.</p>

<h2>3. Defect Fixes</h2>
<ul>
  <li><ac:link ac:anchor="PRND-40370">PRND-40370</ac:link> A validation defect has been resolved...</li>
</ul>

<h2>4. Configuration Changes</h2>
<ac:structured-macro ac:name="code">
  <ac:plain-text-body><![CDATA[
  DRULES_RULE_ENGINE_URL: http://rule-engine/api/ruleEngine/v1
  DRULES_ENABLED: true
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

## Error Handling

### Common Errors
- **Page Not Found**: Parent page ID invalid
- **Permission Denied**: User doesn't have write access to space
- **Rate Limit**: Confluence API rate limit exceeded
- **Invalid Space**: Space key doesn't exist

### Retry Logic
- Retry failed requests with exponential backoff
- Max 3 attempts
- Wait 1s, 2s, 4s between retries

## Implementation Notes

### Markdown to Confluence Conversion
- Use library: `atlassian-python-api` or `markdown-to-confluence`
- Convert Markdown syntax to Confluence storage format
- Handle code blocks, tables, lists, headings
- Preserve formatting

### Version Management
- Confluence tracks page versions automatically
- Each update creates new version
- Show version history in Confluence

### Testing
- Test in staging Confluence space first
- Validate page formatting
- Test update workflow (create, update, update again)

## Future Enhancements

- Label pages automatically (e.g., "release-notes", "Q1-2025")
- Create parent page hierarchy by year/quarter
- Generate index page with all release notes
- Add comments to page with Jira task links
- Email notification on successful publish
