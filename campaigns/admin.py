from django.contrib import admin
from .models import Customer, EmailTemplate, Emails

admin.site.register(Customer)
admin.site.register(EmailTemplate)
admin.site.register(Emails)
