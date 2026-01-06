from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.models.schemas import SuccessResponse
import markdown
import os
from datetime import datetime
import tempfile

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/{job_id}/markdown", response_model=SuccessResponse)
async def export_markdown(job_id: str):
    from backend.services.job_queue import JobQueue
    job_queue = JobQueue()
    job = await job_queue.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")

    result = job.get("result", {})

    if not result:
        raise HTTPException(status_code=404, detail="No release notes generated")

    return {
        "success": True,
        "data": result,
        "message": "Success"
    }


@router.get("/{job_id}/html")
async def export_html(job_id: str):
    from backend.services.job_queue import JobQueue
    job_queue = JobQueue()
    job = await job_queue.get_job(job_id)

    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not found or not completed")

    result = job.get("result", {})

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Release Notes</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
            h1 { color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }
            h2 { color: #1e3a8a; margin-top: 30px; }
            pre { background: #f1f5f9; padding: 15px; border-radius: 8px; overflow-x: auto; }
            code { background: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
            ul, ol { line-height: 1.8; }
        </style>
    </head>
    <body>
    """

    for service_name, data in result.items():
        html_content += f"<h1>{service_name} Release Notes</h1>"
        html_content += markdown.markdown(data.get("content", ""))

    html_content += """
    </body>
    </html>
    """

    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
    temp_file.write(html_content)
    temp_file.close()

    return FileResponse(
        temp_file.name,
        media_type="text/html",
        filename=f"release_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )


@router.get("/{job_id}/pdf")
async def export_pdf(job_id: str):
    from backend.services.job_queue import JobQueue
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from markdown import markdown

    job_queue = JobQueue()
    job = await job_queue.get_job(job_id)

    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not found or not completed")

    result = job.get("result", {})

    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1e40af',
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#1e3a8a',
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=10,
        alignment=TA_LEFT
    )

    for service_name, data in result.items():
        story.append(Paragraph(service_name + " Release Notes", title_style))
        story.append(Spacer(1, 0.2 * inch))

        content = data.get("content", "")
        lines = content.split('\n')

        for line in lines:
            if line.startswith('#'):
                level = line.count('#')
                text = line.lstrip('#').strip()
                if level == 1:
                    story.append(Paragraph(text, title_style))
                else:
                    story.append(Paragraph(text, heading_style))
            elif line.startswith('- '):
                story.append(Paragraph("• " + line[2:], body_style))
            elif line.startswith('```'):
                continue
            elif line.strip():
                story.append(Paragraph(line, body_style))

        story.append(Spacer(1, 0.3 * inch))

    doc.build(story)

    return FileResponse(
        temp_file.name,
        media_type="application/pdf",
        filename=f"release_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )
