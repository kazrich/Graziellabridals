from django.contrib import admin
from .models import UserRegistration, UserLogin, PasswordRecovery, ClientProfile, UserLogin

admin.site.register(UserRegistration)

@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'success')
    list_filter = ('success', 'timestamp')
    ordering = ('-timestamp',)
admin.site.register(PasswordRecovery)
admin.site.register(ClientProfile)


admin.site.unregister(ClientProfile)




