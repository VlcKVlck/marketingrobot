from django.shortcuts import  render, redirect

from campaigns.models import EmailTemplate
from campaigns.send_emails import send_emails_to_users
from .forms import NewEmail, NewTemplate
from django.contrib import messages



def main_campaigns(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    username =  request.user.first_name if request.user.first_name else request.user.username
    return render(request, 'main_campaigns.html', context={ "username": username})

def new_template(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    if request.method == "POST":
        form = NewTemplate(request.POST)
        if form.errors:
            all_errors = ""
            for msg in form.errors.values():
                all_errors += str(msg[0]) + "\n"
            messages.error(request, "Unsuccessful form submittion. Invalid information.\n" + all_errors)
        if form.is_valid():
            print("valid")
            form.save()
            messages.success(request, "Form saved!" )
            return redirect("/campaigns")
    form = NewTemplate()
    username =  request.user.first_name if request.user.first_name else request.user.username
    return render (request=request, template_name="new_campaign.html", context={"new_campaign_form":form, "username": username})

def success(request):
    messages.success(request, "Emails sent!" )
    return redirect(request, '/campaigns')

def send_campaign_emails(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    campaigns = EmailTemplate.objects.all()
    if request.method == "POST":
        selected_template_id = request.POST['template_id']
        form = NewEmail(request.POST)
        if form.is_valid():
            send_emails_to_users(request, selected_template_id)
            messages.success(request, "Emails sent!" )
            return redirect("/campaigns")
    username =  request.user.first_name if request.user.first_name else request.user.username    
    return render (request=request, template_name="send_campaign_emails.html", context={"templates":campaigns, "username": username})
