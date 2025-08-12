from django.contrib import admin
from django.contrib.auth.models import Group, User



admin.site.site_header = 'Graziell Bridals'                    # default: "Django Administration"
admin.site.index_title = ' Areas'                 # default: "Site administration"
admin.site.site_title = 'Graziella Bridals'  # default: "Django site admin"

#unregister Groups
admin.site.unregister(Group)


#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    #only display username and email
    fields=["username", "email"]

#unregister User
admin.site.unregister(User)
#register User
admin.site.register(User, UserAdmin)