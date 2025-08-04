from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# Home view
def home(request):
    if request.method == "POST":
        full_name = request.POST.get("userName")
        email = request.POST.get("userEmail")
        phone = request.POST.get("userPhone")
        address = request.POST.get("userAddress")
        date_of_event = request.POST.get("eventDate")
        appointment_date = request.POST.get("selectedDateText")
        appointment_time = request.POST.get("selectedTimeText")
        message = request.POST.get("userMessage")

        # Compose the email content
        full_message = f"""
Hello Graziella Bridals,

You have received a new virtual appointment booking:

Name: {full_name}
Email: {email}
Phone: {phone}
Event Date: {date_of_event}
Appointment Date: {appointment_date}
Appointment Time: {appointment_time}
Address: {address}

Message:
{message}

Please follow up with the client for confirmation or changes.

Warm regards,
Graziella Bridal Website
"""

        # Send the email
        send_mail(
            subject=f"New Booking from {full_name}",
            message=full_message,
            from_email=email,
            recipient_list=['graziellab889@gmail.com'],
            fail_silently=False
        )

        return render(request, 'index.html', {
            'full_name': full_name,
            'email': email
        })

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






