from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def index(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.errors:
            all_errors = ""
            for msg in form.errors.values():
                print (msg[0])
                all_errors += str(msg[0]) + "\n"
            messages.error(request, "Unsuccessful registration. Invalid information.\n" + all_errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/campaigns")
    form = NewUserForm()
    return render (request=request, template_name="main/home.html", context={"register_form":form})
