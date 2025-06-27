from django.contrib import admin
from .models.track_gym import TrackGym

# Register your models here.
class TrackGymAdmin(admin.ModelAdmin):
    list_display = ('date', 'user',  'start', 'end', 'duration', 'routine')
    search_fields = ('date', 'user', 'routine')
    list_filter = ('date', 'user',  'routine')
    ordering = ('-date',)

admin.site.register(TrackGym, TrackGymAdmin)