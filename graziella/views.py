from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# Home view
def home(request):
    return render(request, 'index.html')

# Contact view
def contact(request):
    name = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Handle or save the message here
    return render(request, 'contact.html', {'name': name})

# product views
def product(request):
    return render(request, 'product.html')
