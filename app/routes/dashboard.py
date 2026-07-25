from flask import Blueprint, render_template
from flask_login import login_required
from app.models import User, Event, Registration
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Gather summary statistics
    total_users = User.query.count()
    total_events = Event.query.count()
    total_registrations = Registration.query.count()
    
    # Active events (events in the future)
    active_events = Event.query.filter(Event.event_date >= datetime.now().date()).count()

    return render_template('dashboard.html', 
                           total_users=total_users, 
                           total_events=total_events, 
                           total_registrations=total_registrations, 
                           active_events=active_events)
