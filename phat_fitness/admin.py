from django.contrib import admin
from .models.gym_track import GymTrack

# Register your models here.
class GymTrackAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'start', 'end', 'duration', 'routine')
    search_fields = ('user', 'date', 'routine')
    list_filter = ('user', 'date', 'routine')
    ordering = ('-date',)

admin.site.register(GymTrack, GymTrackAdmin)