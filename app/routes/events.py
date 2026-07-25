from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Event, Registration
from app.extensions import db
from datetime import datetime

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
def list_events():
    query = Event.query
    
    search = request.args.get('search', '').strip()
    venue = request.args.get('venue', '').strip()
    organizer = request.args.get('organizer', '').strip()
    date_str = request.args.get('date', '').strip()

    if search:
        query = query.filter(Event.event_name.ilike(f'%{search}%'))
    if venue:
        query = query.filter(Event.venue.ilike(f'%{venue}%'))
    if organizer:
        query = query.filter(Event.organizer.ilike(f'%{organizer}%'))
    if date_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(Event.event_date == filter_date)
        except ValueError:
            pass # Ignore invalid date format in search

    events = query.order_by(Event.event_date.asc(), Event.event_time.asc()).all()
    return render_template('events.html', events=events)

@events_bp.route('/<int:event_id>')
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    registrations_count = Registration.query.filter_by(event_id=event_id, status='registered').count()
    available_seats = event.capacity - registrations_count
    is_full = available_seats <= 0
    is_past = event.event_date < datetime.now().date()
    
    registration = None
    is_registered = False
    if current_user.is_authenticated:
        registration = Registration.query.filter_by(user_id=current_user.user_id, event_id=event_id, status='registered').first()
        is_registered = registration is not None

    return render_template('event_details.html', 
                           event=event, 
                           registrations_count=registrations_count,
                           available_seats=available_seats,
                           is_full=is_full,
                           is_past=is_past,
                           is_registered=is_registered,
                           registration=registration)

@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        event_type = request.form.get('event_type', '').strip()
        description = request.form.get('description', '').strip()
        venue = request.form.get('venue', '').strip()
        organizer = request.form.get('organizer', '').strip()
        capacity = request.form.get('capacity', type=int)
        event_date_str = request.form.get('event_date')
        event_time_str = request.form.get('event_time')

        # Validation
        if not title or not event_type or not venue or not organizer or not capacity or not event_date_str or not event_time_str:
            flash('All required fields must be filled.', 'danger')
            return redirect(url_for('events.create_event'))

        if len(title) > 150:
            flash('Title cannot exceed 150 characters.', 'danger')
            return redirect(url_for('events.create_event'))

        if len(description) > 500:
            flash('Description cannot exceed 500 characters.', 'danger')
            return redirect(url_for('events.create_event'))

        if capacity <= 0:
            flash('Capacity must be greater than 0.', 'danger')
            return redirect(url_for('events.create_event'))

        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            event_time = datetime.strptime(event_time_str, '%H:%M').time()
        except ValueError:
            flash('Invalid date or time format.', 'danger')
            return redirect(url_for('events.create_event'))

        if event_date < datetime.now().date():
            flash('Event date cannot be in the past.', 'danger')
            return redirect(url_for('events.create_event'))

        new_event = Event(
            event_name=title, # Schema still uses event_name
            event_type=event_type,
            description=description,
            venue=venue,
            organizer=organizer,
            capacity=capacity,
            event_date=event_date,
            event_time=event_time
        )
        db.session.add(new_event)
        try:
            db.session.commit()
            flash('Event Created Successfully', 'success')
            return redirect(url_for('events.list_events'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the event. Please try again.', 'danger')
            return redirect(url_for('events.create_event'))

    return render_template('create_event.html')

@events_bp.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        event_type = request.form.get('event_type', '').strip()
        description = request.form.get('description', '').strip()
        venue = request.form.get('venue', '').strip()
        organizer = request.form.get('organizer', '').strip()
        capacity = request.form.get('capacity', type=int)
        event_date_str = request.form.get('event_date')
        event_time_str = request.form.get('event_time')

        # Validation
        if not title or not event_type or not venue or not organizer or not capacity or not event_date_str or not event_time_str:
            flash('All required fields must be filled.', 'danger')
            return redirect(url_for('events.edit_event', event_id=event.event_id))

        if len(title) > 150:
            flash('Title cannot exceed 150 characters.', 'danger')
            return redirect(url_for('events.edit_event', event_id=event.event_id))

        if len(description) > 500:
            flash('Description cannot exceed 500 characters.', 'danger')
            return redirect(url_for('events.edit_event', event_id=event.event_id))

        if capacity <= 0:
            flash('Capacity must be greater than 0.', 'danger')
            return redirect(url_for('events.edit_event', event_id=event.event_id))

        try:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            event_time = datetime.strptime(event_time_str, '%H:%M').time()
            # Depending on browser support, sometimes time comes with seconds like %H:%M:%S
        except ValueError:
            try:
                event_time = datetime.strptime(event_time_str, '%H:%M:%S').time()
            except ValueError:
                flash('Invalid date or time format.', 'danger')
                return redirect(url_for('events.edit_event', event_id=event.event_id))

        if event_date < datetime.now().date():
            flash('Event date cannot be in the past.', 'danger')
            return redirect(url_for('events.edit_event', event_id=event.event_id))

        event.event_name = title
        event.event_type = event_type
        event.description = description
        event.venue = venue
        event.organizer = organizer
        event.capacity = capacity
        event.event_date = event_date
        event.event_time = event_time
        
        try:
            db.session.commit()
            flash('Event Updated Successfully', 'success')
            return redirect(url_for('events.view_event', event_id=event.event_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the event. Please try again.', 'danger')
            return redirect(url_for('events.edit_event', event_id=event.event_id))

    return render_template('edit_event.html', event=event)

@events_bp.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event Deleted Successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the event. It might have active registrations.', 'danger')
    return redirect(url_for('events.list_events'))
