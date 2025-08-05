from django.db import models

class Appointment(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    date_of_event = models.DateField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    timezone = models.CharField(max_length=50, default='Africa/Kampala')
    message = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.appointment_date} at {self.appointment_time}"
    

class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return f"Inquiry from {self.name}"

