from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(githubdetails)
admin.site.register(appdetails)
admin.site.register(appplans)
admin.site.register(databasedetails)
admin.site.register(dbplans)
admin.site.register(envvariables)