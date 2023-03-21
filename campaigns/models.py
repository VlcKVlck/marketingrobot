from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, primary_key=True)


class EmailTemplate(models.Model):
    name = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    body = models.TextField()
    date_created = models.DateTimeField(default=None)

class Emails(models.Model):
    email_address = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='email')
    email_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(default=None)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)

