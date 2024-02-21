from django.contrib import admin
from .models import User, Athlete, Venue, Match, MatchInvitation, MatchScore

admin.site.register(User)
admin.site.register(Athlete)
admin.site.register(Venue)
admin.site.register(Match)
admin.site.register(MatchInvitation)
admin.site.register(MatchScore)


