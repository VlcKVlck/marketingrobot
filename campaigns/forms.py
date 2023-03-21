import datetime
from django import forms
from campaigns.models import EmailTemplate, Emails
from datetime import datetime

class NewTemplate(forms.Form):
	template_name = forms.CharField(required=True)
	email_subject_line = forms.CharField(required=True)
	email_body = forms.CharField(widget=forms.Textarea(), required=True)

	class Meta:
		model = EmailTemplate
		fields = ["name", "subject", "body", "date_created"]
		labels = {'name': "template_name", 
	    "subject": "email_subject_line",
		"body": "email_body", "date_created": "date_created"}

	def save(self, commit=True):
		template = EmailTemplate()
		template.name = self.cleaned_data['template_name']
		template.subject = self.cleaned_data['email_subject_line']
		template.body = self.cleaned_data['email_body']
		template.date_created = datetime.now()
		if commit:
			template.save()
		return template
	
class NewEmail(forms.Form):
	class Meta:
		model = Emails
		fields =["id"]
		labels = {"id": "id"}

	def save(self, commit=True):
		email = Emails()
		email.email_template = self.cleaned_data['id']
	pass
	
