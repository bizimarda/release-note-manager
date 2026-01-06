from typing import Dict, Any, List, Optional
from backend.core.config import settings
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
import httpx
import json


class AIService:
    def __init__(self):
        self.provider = settings.ai_provider.lower()
        self._init_provider()

    def _init_provider(self):
        if self.provider == "groq":
            # Groq uses direct HTTP calls, no client needed
            self.client = None
        elif self.provider == "openai":
            api_key = settings.openai_api_key.strip() if settings.openai_api_key else ""
            self.client = OpenAI(
                api_key=api_key,
                base_url=settings.openai_base_url.strip() if settings.openai_base_url else ""
            )
            self.model = settings.openai_model.strip() if settings.openai_model else ""
        elif self.provider == "anthropic":
            api_key = settings.anthropic_api_key.strip() if settings.anthropic_api_key else ""
            self.client = Anthropic(api_key=api_key)
            self.model = settings.anthropic_model.strip() if settings.anthropic_model else ""
        elif self.provider == "gemini":
            api_key = settings.gemini_api_key.strip() if settings.gemini_api_key else ""
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(settings.gemini_model.strip() if settings.gemini_model else "")
            self.model = settings.gemini_model.strip() if settings.gemini_model else ""

    async def analyze_code_changes(self, diff: str, jira_context: Dict, pr_context: Dict = None) -> Dict:
        prompt = self._build_analysis_prompt(diff, jira_context, pr_context)

        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
        elif self.provider == "gemini":
            response = self.client.generate_content(prompt)
            content = response.text
        elif self.provider == "groq":
            content = await self._call_groq_api(prompt)
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            content = response.choices[0].message.content

        return self._parse_analysis_response(content)

    async def _call_groq_api(self, prompt: str) -> str:
        """Direct HTTP call to Groq API like TypeScript implementation"""
        import logging
        logger = logging.getLogger(__name__)

        base_url = settings.groq_base_url.strip() if settings.groq_base_url else "https://api.groq.com/openai/v1"
        api_key = settings.groq_api_key.strip() if settings.groq_api_key else ""
        model = settings.groq_model.strip() if settings.groq_model else "llama-3.3-70b-versatile"

        logger.info(f"Groq API call - Base URL: {base_url}")
        logger.info(f"Groq API call - Model: {model}")
        logger.info(f"Groq API call - API Key length: {len(api_key)}")
        logger.info(f"Groq API call - API Key prefix: {api_key[:10]}...")

        async with httpx.AsyncClient(timeout=60.0) as client:
            url = f"{base_url}/chat/completions"
            logger.info(f"Groq API call - Full URL: {url}")

            response = await client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                }
            )

            logger.info(f"Groq API response status: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"Groq API error response: {response.text}")

            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def _build_analysis_prompt(self, diff: str, jira_context: Dict, pr_context: Dict = None) -> str:
        pr_info = ""
        if pr_context:
            pr_title = pr_context.get("pr_title", "")
            pr_body = pr_context.get("pr_body", "")
            pr_messages = pr_context.get("pr_messages", [])
            pr_merged = pr_context.get("pr_merged", False)

            pr_info = "\nPull Request Information:\n"
            if pr_title:
                pr_info += f"- PR Title: {pr_title}\n"
            if pr_body:
                pr_info += f"- PR Description: {pr_body[:500]}\n"
            if pr_merged:
                pr_info += f"- Status: Merged\n"
            if pr_messages:
                pr_info += "- PR Comments and Reviews:\n"
                for msg in pr_messages[:5]:
                    pr_info += f"  * {msg[:200]}\n"

        return f"""Analyze the following code changes and generate a detailed release note summary.

Jira Task Context:
- Key: {jira_context.get('key')}
- Summary: {jira_context.get('summary')}
- Description: {jira_context.get('description')[:500]}
{pr_info}
Code Changes (Git Diff):
{diff[:2000]}

Please provide:
1. A detailed business-friendly summary (3-5 sentences) that explains what changed, why it was changed, and the impact. Include specific details from the PR/diff such as library upgrades, API changes, or significant code refactoring.
2. Category: New Feature, Improvement, Defect Fix, Breaking Change, or Deprecation
3. Configuration changes (if any, in YAML format)
4. Database migrations (if any, list SQL changes)
5. DevOps changes (if any)
6. CVE/security issues (if any)

Important: The summary should be descriptive and include specific details about the changes, not just a generic statement.

Respond in JSON format:
{{
    "summary": "Detailed business-friendly summary with specific changes",
    "category": "Category name",
    "confidence": 0.95,
    "configuration_changes": [],
    "database_migrations": [],
    "devops_changes": [],
    "cves": [],
    "api_changes": []
}}
"""

    def _parse_analysis_response(self, content: str) -> Dict:
        import json
        try:
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
        except:
            pass

        return {
            "summary": content[:200],
            "category": "Improvement",
            "confidence": 0.5,
            "configuration_changes": [],
            "database_migrations": [],
            "devops_changes": [],
            "cves": [],
            "api_changes": []
        }

    async def categorize_changes(self, analyses: List[Dict]) -> Dict:
        categories = {
            "new_features": [],
            "improvements": [],
            "defect_fixes": [],
            "breaking_changes": [],
            "deprecations": []
        }

        for analysis in analyses:
            category = analysis.get("category", "Improvement").lower().replace(" ", "_")

            if category == "new_feature":
                categories["new_features"].append(analysis)
            elif category == "improvement":
                categories["improvements"].append(analysis)
            elif category == "defect_fix":
                categories["defect_fixes"].append(analysis)
            elif category == "breaking_change":
                categories["breaking_changes"].append(analysis)
            elif category == "deprecation":
                categories["deprecations"].append(analysis)

        return categories
