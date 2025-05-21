from django.contrib import admin
from .models.track_gym import TrackGym

# Register your models here.
class TrackGymAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'start', 'end', 'duration', 'routine')
    search_fields = ('user', 'date', 'routine')
    list_filter = ('user', 'date', 'routine')
    ordering = ('-date',)

admin.site.register(TrackGym, TrackGymAdmin)