from typing import Dict, Any, List
from datetime import datetime
import json


class ReleaseNotesGenerator:
    def __init__(self):
        self.template = self._get_template()

    def _get_template(self) -> str:
        return """# {service_name} {version} {release_name}

## Version Information
**Release Notes:** {service_name}
**Version:** {version}
**Release Date:** {release_date}
**Author:** {author}

## Task Summary
{task_summary}

## 1. New Features
{new_features}

## 2. Improvements
{improvements}

## 3. Defect Fixes
{defect_fixes}

## 4. Configuration Changes
{configuration_changes}

## 5. Breaking Changes
{breaking_changes}

## 6. Database Migrations
{database_migrations}

## 7. Known Issues
{known_issues}

## 8. DevOps Notes
{devops_notes}

## 9. Support
{support_info}
"""

    def generate(self, service_data: Dict, options: Dict = None) -> str:
        options = options or {}

        return self.template.format(
            service_name=service_data.get("service_name", "Service"),
            version=service_data.get("version", "1.0.0"),
            release_name=options.get("release_name", ""),
            release_date=options.get("release_date", datetime.now().strftime("%d/%m/%Y")),
            author=options.get("author", "Release Manager"),

            task_summary=self._format_task_summary(service_data.get("task_summary", [])),
            new_features=self._format_section(service_data.get("new_features", [])),
            improvements=self._format_section(service_data.get("improvements", [])),
            defect_fixes=self._format_defect_fixes(service_data.get("defect_fixes", [])),
            configuration_changes=self._format_config(service_data.get("configuration_changes", [])),
            breaking_changes=self._format_section(service_data.get("breaking_changes", [])),
            database_migrations=self._format_section(service_data.get("database_migrations", [])),
            known_issues=self._format_known_issues(service_data.get("cves", [])),
            devops_notes=self._format_section(service_data.get("devops_changes", [])),
            support_info="For any issues, visit our support portal"
        )

    def _format_task_summary(self, tasks: List) -> str:
        if not tasks:
            return "None for this release."

        result = []
        for task in tasks:
            if isinstance(task, dict):
                jira_key = task.get("jira_key", "")
                summary = task.get("summary", "")
                if jira_key:
                    result.append(f"- **{jira_key}** {summary}")
                else:
                    result.append(f"- {summary}")
            else:
                result.append(f"- {task}")

        return "\n".join(result)

    def _format_section(self, items: List) -> str:
        if not items:
            return "None for this release."

        result = []
        for item in items:
            if isinstance(item, dict):
                summary = item.get("summary", str(item))
                result.append(f"- {summary}")
            else:
                result.append(f"- {item}")

        return "\n".join(result)

    def _format_defect_fixes(self, fixes: List) -> str:
        if not fixes:
            return "None for this release."

        result = []
        for fix in fixes:
            if isinstance(fix, dict):
                jira_key = fix.get("jira_key", "")
                summary = fix.get("summary", "")
                if jira_key:
                    result.append(f"- **{jira_key}** {summary}")
                else:
                    result.append(f"- {summary}")
            else:
                result.append(f"- {fix}")

        return "\n".join(result)

    def _format_config(self, configs: List) -> str:
        if not configs:
            return "None for this release."

        result = []
        for config in configs:
            if isinstance(config, dict):
                if config.get("type") == "yaml":
                    result.append(f"```yaml\n{config.get('content', '')}\n```")
                elif config.get("type") == "env":
                    result.append(f"```bash\n{config.get('content', '')}\n```")
                else:
                    result.append(f"- {config.get('summary', str(config))}")
            else:
                result.append(f"- {config}")

        return "\n".join(result)

    def _format_known_issues(self, cves: List) -> str:
        if not cves:
            return "None for this release."

        result = []
        for cve in cves:
            if isinstance(cve, dict):
                cve_id = cve.get("cve_id", "")
                description = cve.get("description", "")
                impact = cve.get("impact", "")
                result.append(f"- **{cve_id}** {description}. {impact}")
            else:
                result.append(f"- {cve}")

        return "\n".join(result)

    def generate_for_service(self, analyses: List[Dict], jira_tasks: List[Dict], service_name: str, options: Dict = None) -> str:
        options = options or {}

        service_data = {
            "service_name": service_name,
            "version": options.get("version", "1.0.0"),
            "task_summary": [],
            "new_features": [],
            "improvements": [],
            "defect_fixes": [],
            "breaking_changes": [],
            "deprecations": [],
            "configuration_changes": [],
            "database_migrations": [],
            "devops_changes": [],
            "cves": []
        }

        for analysis in analyses:
            category = analysis.get("category", "Improvement")
            jira_key = analysis.get("jira_key", "")
            jira_summary = analysis.get("jira_summary", "")

            if jira_summary:
                service_data["task_summary"].append({
                    "jira_key": jira_key,
                    "summary": jira_summary
                })

            # LLM'in ürettiği GitHub PR analiz sonucunu ilgili category'ye ekle
            if analysis.get("summary"):
                item = {
                    "summary": analysis["summary"],
                    "jira_key": jira_key
                }
                if category == "New Feature":
                    service_data["new_features"].append(item)
                elif category == "Improvement":
                    service_data["improvements"].append(item)
                elif category == "Defect Fix":
                    service_data["defect_fixes"].append(item)
                elif category == "Breaking Change":
                    service_data["breaking_changes"].append(item)
                elif category == "Deprecation":
                    service_data["deprecations"].append(item)

            if analysis.get("configuration_changes"):
                service_data["configuration_changes"].extend(analysis["configuration_changes"])
            if analysis.get("database_migrations"):
                service_data["database_migrations"].extend(analysis["database_migrations"])
            if analysis.get("devops_changes"):
                service_data["devops_changes"].extend(analysis["devops_changes"])
            if analysis.get("cves"):
                service_data["cves"].extend(analysis["cves"])

            # Jira'dan gelen özel alanları işle
            jira_release_notes = analysis.get("jira_release_notes", "")
            if jira_release_notes and jira_release_notes.strip() and jira_release_notes.lower() not in ["no changes", "none"]:
                rn_item = {
                    "summary": jira_release_notes,
                    "jira_key": jira_key
                }
                if category == "New Feature":
                    service_data["new_features"].append(rn_item)
                elif category == "Defect Fix":
                    service_data["defect_fixes"].append(rn_item)
                else:
                    service_data["improvements"].append(rn_item)

            # API Change, Application Config, Jenkins pipeline successful alanlarını Configuration Changes'e ekle
            api_change = analysis.get("api_change", "")
            if api_change is not None:
                service_data["configuration_changes"].append({
                    "summary": f"API Change: {api_change}",
                    "jira_key": jira_key
                })

            app_config = analysis.get("app_config", "")
            if app_config is not None:
                service_data["configuration_changes"].append({
                    "summary": f"Application Config: {app_config if app_config.strip() else 'No-change'}",
                    "jira_key": jira_key
                })

            jenkins = analysis.get("jenkins_successful", "")
            if jenkins is not None and jenkins.strip():
                jenkins_value = "Yes" if jenkins.lower() in ["yes", "true"] else "No"
                service_data["configuration_changes"].append({
                    "summary": f"Is Jenkins pipeline successful?: {jenkins_value}",
                    "jira_key": jira_key
                })

            jira_config_notes = analysis.get("jira_configuration_notes", "")
            if jira_config_notes and jira_config_notes.strip() and jira_config_notes.lower() not in ["no changes", "none"]:
                service_data["configuration_changes"].append({
                    "summary": jira_config_notes,
                    "type": "text",
                    "jira_key": jira_key
                })

        return self.generate(service_data, options)
