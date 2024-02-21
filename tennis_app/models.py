from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    real_name = models.CharField(max_length=50, blank=True, null=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    HANDEDNESS_CHOICES = [
        ('Right-handed', 'Right-handed'),
        ('Left-handed', 'Left-handed')
    ]
    handedness = models.CharField(max_length=13, choices=HANDEDNESS_CHOICES, default='Right-handed')
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    BACKHAND_CHOICES = [
        ('One-handed', 'One-handed'),
        ('Two-handed', 'Two-handed')
    ]
    backhand_type = models.CharField(max_length=11, choices=BACKHAND_CHOICES, blank=True, null=True)
    SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]
    skill_level = models.CharField(max_length=12, choices=SKILL_LEVEL_CHOICES, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class Venue(models.Model):
    venue_name = models.CharField(max_length=100)
    venue_city = models.CharField(max_length=100)
    venue_address = models.CharField(max_length=100)
    SURFACE_CHOICES = [
        ('Hard', 'Hard'),
        ('Grass', 'Grass'),
        ('Clay', 'Clay')
    ]
    surface_type = models.CharField(max_length=5, choices=SURFACE_CHOICES)
    google_maps_url = models.CharField(max_length=255)
    photo_url = models.CharField(max_length=255)

    def __str__(self):
        return self.venue_name   


class Match(models.Model):
    date = models.DateField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    STATE_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed')
    ]
    state = models.CharField(max_length=9, choices=STATE_CHOICES, default='Upcoming')
    winner = models.ForeignKey(Athlete, related_name='winner', on_delete=models.SET_NULL, null=True)
    player1 = models.ForeignKey(Athlete, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Athlete, related_name='player2', on_delete=models.CASCADE)

    def __str__(self):
        return f"Match ID: {self.pk}, Date: {self.date}"



class MatchScore(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    set_number = models.IntegerField()
    games_won = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'set_number', 'athlete'], name='unique_match_score')
        ]

    def __str__(self):
        return f"Match: {self.match}, Set Number: {self.set_number}, Athlete: {self.athlete}"

class MatchInvitation(models.Model):
    sender = models.ForeignKey(Athlete, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Athlete, related_name='received_invitations', on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed')
    ]
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='Pending')
    invitation_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateField(null=True)
    scheduled_time = models.TimeField(null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f"Invitation ID: {self.pk}, Sender: {self.sender}, Recipient: {self.recipient}"

