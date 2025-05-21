import sys
sys.path.append("..")

from phat_investment.models.track_investment import TrackInvestment
from rest_framework import serializers

class TrackInvestmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrackInvestment
        fields = ['id','date','acbs','mio','dragon','idle_cash','crypto','total'] #Gotta make SSI hidden for now