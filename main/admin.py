from django.contrib import admin

from .models import *

admin.site.register(Project)

admin.site.register(ProjectEmployee)

admin.site.register(SocialNetwork)

admin.site.register(Team)

admin.site.register(AppUser)

admin.site.register(TimeEntry)

admin.site.register(Social)

admin.site.register(Role)

admin.site.register(HistoryAdvance)

admin.site.register(HistoryWorker)

admin.site.register(HistoryProject)

admin.site.register(AuthData)
