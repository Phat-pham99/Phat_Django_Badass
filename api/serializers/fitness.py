import sys
sys.path.append("..")

from phat_fitness.models import TrackGym
from rest_framework import serializers

class TrackGymSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrackGym
        fields = ['id','user','date','start','end','routine']