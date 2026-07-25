from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Event, Registration
from app.extensions import db
from datetime import datetime

registrations_bp = Blueprint('registrations', __name__)

@registrations_bp.route('/')
@login_required
def list_registrations():
    user_registrations = Registration.query.filter_by(user_id=current_user.user_id, status='registered').order_by(Registration.registration_date.desc()).all()
    return render_template('my_registrations.html', registrations=user_registrations)

@registrations_bp.route('/register/<int:event_id>', methods=['POST'])
@login_required
def register(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event.event_date < datetime.now().date():
        flash('Cannot register for past events.', 'danger')
        return redirect(url_for('events.view_event', event_id=event_id))
        
    # Check if already registered
    existing_reg = Registration.query.filter_by(user_id=current_user.user_id, event_id=event_id).first()
    
    if existing_reg:
        if existing_reg.status == 'registered':
            flash('You are already registered for this event.', 'warning')
            return redirect(url_for('events.view_event', event_id=event_id))
        elif existing_reg.status == 'cancelled':
            # Reactivate cancelled registration if space available
            registrations_count = Registration.query.filter_by(event_id=event_id, status='registered').count()
            if registrations_count >= event.capacity:
                flash('Sorry, this event is full.', 'danger')
                return redirect(url_for('events.view_event', event_id=event_id))
            
            existing_reg.status = 'registered'
            existing_reg.registration_date = datetime.utcnow()
            try:
                db.session.commit()
                flash('Registration successful!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('events.view_event', event_id=event_id))
            
    # Check capacity
    registrations_count = Registration.query.filter_by(event_id=event_id, status='registered').count()
    if registrations_count >= event.capacity:
        flash('Sorry, this event is full.', 'danger')
        return redirect(url_for('events.view_event', event_id=event_id))
        
    # Create new registration
    new_reg = Registration(user_id=current_user.user_id, event_id=event_id, status='registered')
    db.session.add(new_reg)
    try:
        db.session.commit()
        flash('Registration successful!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during registration. Please try again.', 'danger')
        
    return redirect(url_for('events.view_event', event_id=event_id))

@registrations_bp.route('/cancel/<int:registration_id>', methods=['POST'])
@login_required
def cancel_registration(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    
    # Ensure the user owns the registration
    if registration.user_id != current_user.user_id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('registrations.list_registrations'))
        
    if registration.status == 'cancelled':
        flash('Registration is already cancelled.', 'warning')
    else:
        registration.status = 'cancelled'
        try:
            db.session.commit()
            flash('Registration cancelled successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while cancelling. Please try again.', 'danger')
        
    # Redirect back to where they came from if possible, else my_registrations
    referrer = request.referrer
    if referrer and '/events/' in referrer:
        return redirect(url_for('events.view_event', event_id=registration.event_id))
    
    return redirect(url_for('registrations.list_registrations'))
