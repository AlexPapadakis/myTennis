from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time,TIMESTAMP, CheckConstraint, func,DECIMAL, create_engine,ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship


Base = declarative_base()

# Define models for your tables
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    real_name = Column(String(50))
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    phone = Column(String(20))
    birthday = Column(Date)
    address = Column(String(255))
    city = Column(String(100))
    postal_code = Column(String(20))
    photo_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    

class Athlete(Base):
    __tablename__ = 'Athlete'

    user_id = Column(Integer,  ForeignKey('User.id'), primary_key=True)
    handedness = Column(String(20))
    height = Column(DECIMAL(5, 2))
    weight = Column(DECIMAL(5, 2))
    backhand_type = Column(String(20))
    skill_level = Column(String(20))
    points = Column(Integer)
    
    user = relationship("User")
    __table_args__ = (
        CheckConstraint("handedness IN ('Right-handed', 'Left-handed')"),
        CheckConstraint("backhand_type IN ('One-handed', 'Two-handed')"),
        CheckConstraint("skill_level IN ('Beginner', 'Intermediate', 'Advanced')")
    )

    def __repr__(self):
        return f"<Athlete(user_id={self.user_id}, handedness='{self.handedness}', height={self.height}, weight={self.weight}, backhand_type='{self.backhand_type}', skill_level='{self.skill_level}', points={self.points})>"


class Venue(Base):
    __tablename__ = 'Venue'

    venue_id = Column(Integer, primary_key=True, autoincrement=True)
    venue_name = Column(String(100))
    venue_city = Column(String(100))
    venue_address = Column(String(100))
    surface_type = Column(String(10), CheckConstraint("surface_type IN ('Hard', 'Grass', 'Clay')"))
    google_maps_url = Column(String(255))
    photo_url = Column(String(255))
    
    def __repr__(self):
        return f"<Venue(venue_id={self.venue_id}, venue_name='{self.venue_name}', venue_city='{self.venue_city}', venue_address='{self.venue_address}', surface_type='{self.surface_type}', google_maps_url='{self.google_maps_url}', photo_url='{self.photo_url}')>"

class Match(Base):
    __tablename__ = 'Match'

    match_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    venue_id = Column(Integer, ForeignKey('Venue.venue_id'))
    state = Column(String(20))
    winner_id = Column(Integer, ForeignKey('Athlete.user_id'))
    player1_id = Column(Integer, ForeignKey('Athlete.user_id'))
    player2_id = Column(Integer, ForeignKey('Athlete.user_id'))

    venue = relationship("Venue")
    winner = relationship("Athlete", foreign_keys=[winner_id])
    player1 = relationship("Athlete", foreign_keys=[player1_id])
    player2 = relationship("Athlete", foreign_keys=[player2_id])
    
    __table_args__ = (
    CheckConstraint("state IN ('Upcoming', 'Completed')"),
    )
    def __repr__(self):
        return f"<Match(match_id={self.match_id}, date={self.date}, venue_id={self.venue_id}, state='{self.state}', winner_id={self.winner_id}, player1_id={self.player1_id}, player2_id={self.player2_id})>"
    

class MatchScore(Base):
    __tablename__ = 'Match_Score'

    match_id = Column(Integer, ForeignKey('Match.match_id'), primary_key=True)
    athlete_user_id = Column(Integer, ForeignKey('Athlete.user_id'), primary_key=True)
    set_number = Column(Integer, primary_key=True)
    games_won = Column(Integer)

    match = relationship("Match")
    athlete = relationship("Athlete")

    __table_args__ = (
        PrimaryKeyConstraint('match_id', 'set_number', 'athlete_user_id'),
    )
    
    def __repr__(self):
        return f"<MatchScore(match_id={self.match_id}, athlete_user_id={self.athlete_user_id}, set_number={self.set_number}, games_won={self.games_won})>"
    
class MatchInvitation(Base):
    __tablename__ = 'Match_Invitation'

    invitation_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('Athlete.user_id'))
    recipient_id = Column(Integer, ForeignKey('Athlete.user_id'))
    status = Column(String(20))
    invitation_date = Column(TIMESTAMP)
    scheduled_date = Column(Date)
    scheduled_time = Column(Time)
    venue_id = Column(Integer, ForeignKey('Venue.venue_id'))

    sender = relationship("Athlete", foreign_keys=[sender_id])
    recipient = relationship("Athlete", foreign_keys=[recipient_id])
    venue = relationship("Venue")
    
    __table_args__ = (
        CheckConstraint("status IN ('Pending', 'Accepted', 'Completed')"),
    )
    
    def __repr__(self):
        return f"<MatchInvitation(invitation_id={self.invitation_id}, sender_id={self.sender_id}, recipient_id={self.recipient_id}, status='{self.status}', invitation_date={self.invitation_date}, scheduled_date={self.scheduled_date}, scheduled_time={self.scheduled_time}, venue_id={self.venue_id})>"
    
    
    
class Roles(Base):
    __tablename__ = 'Roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True)
    description = Column(String(255))
    
    def __repr__(self):
        return f"<Roles(id={self.id}, name='{self.name}', description='{self.description}')>"
    
    
class UserRoles(Base):
    __tablename__ = 'User_Roles'

    user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('Roles.id'), primary_key=True)
    
    user = relationship("User")
    role = relationship("Roles")
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'role_id'),
    )
    
    def __repr__(self):
        return f"<UserRoles(user_id={self.user_id}, role_id={self.role_id})>"