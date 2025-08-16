# graziella/admin.py

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite
from accounts.models import UserLogin, PasswordRecovery, ClientProfile,UserRegistration,WishlistItem
from .models import Appointment, Inquiry  # ✅ Real models
from django.contrib import admin
admin.site.unregister(Group)

# ----------------------------------------
# 🌸 Custom Admin Site Branding
# ----------------------------------------

class GraziellaAdminSite(AdminSite):
    site_header = 'Graziella Bridals'
    site_title = 'Graziella Admin'
    index_title = 'Grazilla Dashboard panel'

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = 'admin/css/custom.css'
        return context

admin_site = GraziellaAdminSite(name='graziella_admin')

# ----------------------------------------
# 👤 Custom User Admin
# ----------------------------------------

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "email"]
    list_display = ["username", "email", "is_staff", "is_superuser"]
    search_fields = ["username", "email"]

# ----------------------------------------
# 📅 Appointment Admin
# ----------------------------------------

@admin.register(Appointment, site=admin_site)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "appointment_date", "appointment_time", "email", "phone", "submitted_at")
    list_filter = ("appointment_date", "timezone")
    search_fields = ("full_name", "email", "phone")
    ordering = ("-submitted_at",)

# ----------------------------------------
# 📩 Inquiry Admin
# ----------------------------------------

@admin.register(Inquiry, site=admin_site)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "number")
    search_fields = ("name", "email", "number")
    ordering = ("-id",)

# ----------------------------------------
# ✅ Register User and Cleanup
# ----------------------------------------

admin_site.register(User, UserAdmin)
admin_site.register(UserLogin)
admin_site.register(PasswordRecovery)
admin_site.register(ClientProfile)
admin_site.register(UserRegistration)
admin_site.register(WishlistItem)


# ----------------------------------------
# 🚫 Unregister Unused Models
# ----------------------------------------




