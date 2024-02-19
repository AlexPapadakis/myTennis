# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Athlete(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    handedness = models.CharField(max_length=12, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    backhand_type = models.CharField(max_length=10, blank=True, null=True)
    skill_level = models.CharField(max_length=12, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'athlete'


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    venue = models.ForeignKey('Venue', models.DO_NOTHING, blank=True, null=True)
    state = models.CharField(max_length=9, blank=True, null=True)
    winner = models.ForeignKey(Athlete, models.DO_NOTHING, blank=True, null=True)
    player1 = models.ForeignKey(Athlete, models.DO_NOTHING, related_name='match_player1_set', blank=True, null=True)
    player2 = models.ForeignKey(Athlete, models.DO_NOTHING, related_name='match_player2_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match'


class MatchInvitation(models.Model):
    invitation_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Athlete, models.DO_NOTHING, blank=True, null=True)
    recipient = models.ForeignKey(Athlete, models.DO_NOTHING, related_name='matchinvitation_recipient_set', blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    invitation_date = models.DateTimeField(blank=True, null=True)
    scheduled_date = models.DateField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)
    venue = models.ForeignKey('Venue', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_invitation'


class MatchScore(models.Model):
    match = models.OneToOneField(Match, models.DO_NOTHING, primary_key=True)  # The composite primary key (match_id, set_number, athlete_user_id) found, that is not supported. The first column is selected.
    athlete_user = models.ForeignKey(Athlete, models.DO_NOTHING)
    set_number = models.IntegerField()
    games_won = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_score'
        unique_together = (('match', 'set_number', 'athlete_user'),)


class User(models.Model):
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    real_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Venue(models.Model):
    venue_id = models.AutoField(primary_key=True)
    venue_name = models.CharField(max_length=100, blank=True, null=True)
    venue_city = models.CharField(max_length=100, blank=True, null=True)
    venue_address = models.CharField(max_length=100, blank=True, null=True)
    surface_type = models.CharField(max_length=5, blank=True, null=True)
    google_maps_url = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'venue'
