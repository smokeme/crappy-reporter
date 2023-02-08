from django.contrib import admin
from .models import Report, Issues
from django.utils.html import format_html
from django import forms


class IssuesForm(forms.ModelForm):
    class Meta:
        model = Issues
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['report'].widget = forms.HiddenInput()


class IssuesInlineForm(forms.ModelForm):
    class Meta:
        model = Issues
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['report'].widget = forms.HiddenInput()


class IssuesInline(admin.TabularInline):
    model = Issues
    form = IssuesInlineForm
    extra = 1
    template = 'issue_copy.html'


class ReportAdmin(admin.ModelAdmin):
    inlines = [IssuesInline]
    list_display = ('name', 'created_at', 'updated_at',
                    'generate_report', 'fix_report')
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']

    def fix_report(self, obj):
        return format_html(f'<a href="/fix_report/{obj.id}">Fix Report</a>')
    fix_report.allow_tags = True
    fix_report.short_description = 'Fix Report'

    def generate_report(self, obj):
        return format_html(f'<a href="/generate/{obj.id}">Generate Report</a>')
    generate_report.allow_tags = True
    generate_report.short_description = 'Generate Report'


admin.site.register(Report, ReportAdmin)


class IssuesAdmin(admin.ModelAdmin):
    form = IssuesForm

    def save_model(self, request, obj, form, change):
        if 'copy_from' in request.POST:
            source_issue = Issues.objects.get(pk=request.POST['copy_from'])
            obj.description = source_issue.description
            obj.recommendation = source_issue.recommendation
        super().save_model(request, obj, form, change)

    # list_display = ('report', 'number', 'issue', 'description',
    #                 'recommendation', 'risk', 'status', 'proof', 'created_at', 'updated_at')
    # list_filter = ['created_at', 'updated_at', 'risk', 'status']
    # search_fields = ['issue', 'description', 'recommendation']


admin.site.register(Issues, IssuesAdmin)
