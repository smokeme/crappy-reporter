from .models import Report, Issues
from django.http import HttpResponse
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import openai
import os


def askAi(inputtype, input):
    openai.api_key = "OPENAI_API_KEY"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="I'm writing a pentesting report, please fix this {} to look more professional,:\n\n{}".format(
            inputtype,
            input),
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text


def fix_report(request, report_id):
    if not request.user.is_authenticated:
        return HttpResponse('<script> window.location.href = "/admin/"; </script>')
    report = Report.objects.get(id=report_id)
    issues = Issues.objects.filter(report=report)
    for issue in issues:
        issue.description = askAi("description", issue.description)
        issue.recommendation = askAi("recommendation", issue.recommendation)
        issue.save()
    # After fixing the report, Go back to the report page in django admin
    return HttpResponse('<script> window.location.href = "/admin/main/issues/?report__id__exact='+str(report_id)+'"; </script>')


def generate_report(request, report_id):
    try:
        if not request.user.is_authenticated:
            return HttpResponse('<script> window.location.href = "/admin/"; </script>')
        report = Report.objects.get(id=report_id)
        issues = Issues.objects.filter(report=report)
        doc = DocxTemplate("template.docx")
        context = {
            'project': report.name,
            'issues': issues,
            'issues_count': len(issues),
            'high': len(issues.filter(risk='high')),
            'medium': len(issues.filter(risk='medium')),
            'low': len(issues.filter(risk='low')),
            'critical': len(issues.filter(risk='critical')),
            'year': report.updated_at.year,
            'month': report.updated_at.month,
            'month_name': report.updated_at.strftime('%B'),
            'day': report.updated_at.day,
        }
        docx_images = {}
        for issue in issues:
            if issue.proof:
                docx_images[issue.id] = InlineImage(
                    doc, issue.proof.path, width=Mm(150))
        context['docx_images'] = docx_images

        doc.render(context)
        doc.save("generated.docx")

        with open('generated.docx', 'rb') as fh:
            response = HttpResponse(fh.read(
            ), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename('generated.docx')
        return response
    except Exception as e:
        return HttpResponse('<script> window.location.href = "/admin/main/report/"; </script>')
