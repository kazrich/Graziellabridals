from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Inquiry


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
Graziella Bridals Website
"""

        # 🛡️ Safe email logic with feedback
        try:
            send_mail(
                subject=f"New Booking from {full_name}",
                message=full_message,
                from_email=email,
                recipient_list=['graziellab889@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "🎉 Your booking has been sent successfully!")
        except Exception as e:
            messages.error(request, "⚠️ We couldn’t send the booking email. Please try again or contact us directly.")
            print("Email send error:", e)

        return render(request, 'index.html')

    return render(request, 'index.html')



# Contact view
def contact(request):
    name = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message_text = request.POST.get('message')

        # Save to database
        Inquiry.objects.create(
            name=name,
            email=email,
            number=number,
            message=message_text
        )

        # Compose the email
        email_subject = "Question from Contact-us page"
        email_body = f"""
Hello Graziella Bridals,

You’ve received a new message from the Contact Us page:

Name: {name}
Email: {email}
Contact Number: {number}

Message:
{message_text}

Warm regards,
Graziella Bridals Website
"""

        try:
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=email,  # Optional: use a default sender if needed
                recipient_list=['graziellab889@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "💌 Your message has been sent successfully. We'll be in touch soon!")
        except Exception as e:
            messages.error(request, "⚠️ We couldn’t send your message by email. Please try again or contact us directly.")
            print("Email send error:", e)

    return render(request, 'contact.html', {'name': name})




# product views
def product(request):
    return render(request, 'product.html')






