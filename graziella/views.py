# graziella/views.py
from accounts.models import UserRegistration  # adjust import if needed
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect

# 🏠 Home view
def home(request):
    profile = None
    user_id = request.session.get('user_id')

    if user_id:
        try:
            profile = UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            profile = None

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

    return render(request, 'index.html', {'profile': profile})
# 📬 Contact view
def contact(request):
    profile = None
    user_id = request.session.get('user_id')

    # 🧠 Retrieve user profile if logged in
    if user_id:
        try:
            profile = UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            profile = None

    name = None  # Used for thank-you message in template

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        number = request.POST.get('number', '').strip()
        message_text = request.POST.get('message', '').strip()

        # 💌 Compose email
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

        # ✉️ Send email
        try:
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['graziellab889@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "💌 Your message has been sent successfully. We'll be in touch soon!")
        except Exception as e:
            messages.error(request, "⚠️ We couldn’t send your message by email.")
            print("Email send error:", e)  # This should show the real issue

    return render(request, 'contact.html', {
        'name': name,
        'profile': profile,
        'help_text': "Reach out for guidance, opportunities or assistance — we’re here for you."
    })


# 👗 Product view
def product(request):
    profile = None
    user_id = request.session.get('user_id')

    if user_id:
        try:
            profile = UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            profile = None

    return render(request, 'product.html', {'profile': profile})

# 👗 About-us view
def about_us(request):
    profile = None
    user_id = request.session.get('user_id')

    if user_id:
        try:
            profile = UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            profile = None

    return render(request, 'about-us.html', {'profile': profile})



def ask_popup(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        contact = request.POST.get('contact', '').strip()
        question_type = request.POST.get('questionType', '').strip()
        message_text = request.POST.get('message', '').strip()

        subject = f"Popup Inquiry: {question_type}"
        body = f"""
Hello Graziella Bridals,

You’ve received a new popup inquiry:

Name: {name}
Email: {email or 'Not provided'}
Contact: {contact}
Question Type: {question_type}

Message:
{message_text}

Warm regards,
Graziella Bridals Website
"""

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['graziellab889@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "💌 Your question has been sent successfully. We'll respond shortly.")
        except Exception as e:
            messages.error(request, "⚠️ We couldn’t send your message. Please try again.")
            print("Popup email error:", e)

        return redirect('home')  # Or wherever you want to land after submission