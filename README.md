# Event Management System

## Project Overview
A robust, web-based platform for organizing, managing, and registering for events. Built with Flask, SQLAlchemy, and Bootstrap, this system streamlines the event management process for both administrators and participants, offering a seamless user experience.

## Features
- **User Authentication**: Secure registration and login functionality.
- **Interactive Dashboard**: A comprehensive overview of system statistics (Total Users, Total Events, Total Registrations, Active Events).
- **Event Management**: Full CRUD operations to create, read, update, and delete events with details like date, time, venue, organizer, and capacity.
- **Event Registration**: Users can register for events, view their upcoming registrations, and cancel them if needed.
- **Search & Filtering**: Easily find events by searching titles, or filtering by venue, organizer, and specific dates.
- **Responsive UI**: A polished, modern interface built with Bootstrap 5 and Bootstrap Icons, fully responsive for desktop and mobile devices.
- **Robust Error Handling**: Graceful error handling for database operations and form submissions, ensuring application stability.

## Technologies Used
- **Backend**: Python 3, Flask, Flask-Login
- **Database**: PostgreSQL / SQLite (via Flask-SQLAlchemy and psycopg)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Environment Management**: python-dotenv

## Project Structure
```text
event_management_system/
│
├── app/                        # Main application package
│   ├── routes/                 # Blueprint modules for routing
│   │   ├── auth.py             # Authentication routes
│   │   ├── dashboard.py        # Dashboard routes
│   │   ├── events.py           # Event management routes
│   │   └── registrations.py    # Registration management routes
│   ├── templates/              # HTML templates (Jinja2)
│   ├── __init__.py             # App factory and blueprint registration
│   ├── extensions.py           # Flask extensions (db, login_manager)
│   └── models.py               # SQLAlchemy database models
│
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── config.py                   # Application configuration
├── create_db.py                # Script to initialize the database
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── test_crud.py                # Automated testing script
```

## Installation Instructions

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git (optional, for cloning)

### Steps
1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   git clone <repository_url>
   cd event_management_system
   ```

2. **Create and activate a virtual environment**:
   - Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variable Setup
This project uses `.env` files to securely load configuration variables.

1. Create a file named `.env` in the root directory.
2. Copy the contents of `.env.example` into `.env`.
3. Replace the placeholder values with your actual configuration:
   ```env
   # Example .env configuration
   SUPABASE_DB_URL=postgresql://username:password@localhost:5432/event_db
   SECRET_KEY=your_secure_random_secret_key
   ```
   *(Note: The application will raise an error if `SECRET_KEY` is not provided).*

## Database Setup
Run the database creation script to set up the database tables (this uses the connection string defined in your `.env`):
```bash
python create_db.py
```

## Running the Application
Start the Flask development server:
```bash
python run.py
```
The application will be accessible at `http://127.0.0.1:5000`.

## Usage Guide
1. **Register/Login**: Start by registering a new account or logging in with an existing one.
2. **Dashboard**: Upon login, you will land on the Dashboard, viewing high-level system metrics.
3. **Browse Events**: Navigate to the "Events" page to view all available events. Use the search bar or filters to find specific events.
4. **Create Event**: Click "Create Event" in the navigation bar to add a new event to the system.
5. **Register for Event**: On an event's details page, click "Register Now" to secure your spot.
6. **My Registrations**: View and manage all your event registrations in the "My Registrations" section.

## Screenshots
*(Add screenshots of the application here once deployed)*
- **Dashboard**: `![Dashboard UI](link-to-image)`
- **Event Listings**: `![Events UI](link-to-image)`
- **Registration Flow**: `![Registration UI](link-to-image)`

## Future Improvements
- **Pagination**: Add pagination to the events list for better scalability.
- **Admin Roles**: Introduce a strict 'Admin' role to restrict event creation and deletion.
- **Email Notifications**: Integrate a mailing service (like SendGrid) for registration confirmations.
- **API Endpoints**: Build a RESTful API to support mobile applications.

## License
MIT License. See `LICENSE` for more information.
