# EdgeRoute - Interactive Learning Roadmap Platform

EdgeRoute (formerly DevPath) is a Flask-based web application that provides interactive learning roadmaps for various technology paths. Users can track their progress through roadmaps, participate in discussions, and manage their learning journey.

## Features

- **Interactive Roadmaps**: Explore detailed learning paths for various technologies
- **Progress Tracking**: Mark topics as completed and track your learning progress
- **User Profiles**: Personalized profiles showing your progress and activity
- **Discussion**: Comment on roadmap topics to share insights or ask questions
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/edgeroute.git
   cd edgeroute
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables (optional):
   ```
   # Create a .env file with the following variables
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   ```

5. Initialize the database:
   ```
   python run.py
   ```

## Usage

1. Start the development server:
   ```
   python run.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Register a new account or log in with the default admin account:
   ```
   Email: admin@example.com
   Password: admin123
   ```

## Project Structure

```
edgeroute/
├── app/                    # Application package
│   ├── api/                # API routes
│   ├── auth/               # Authentication routes
│   ├── errors/             # Error handlers
│   ├── main/               # Main routes
│   ├── roadmap/            # Roadmap routes
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   ├── __init__.py         # Application factory
│   ├── forms.py            # Form classes
│   └── models.py           # Database models
├── roadmap_data/           # JSON files for roadmap content
├── migrations/             # Database migrations
├── config.py               # Configuration settings
├── requirements.txt        # Dependencies
└── run.py                  # Application entry point
```

## Development

### Adding New Roadmaps

1. Create a new JSON file in the `roadmap_data` directory
2. Add the roadmap metadata to `roadmap_data/roadmaps.json`
3. Import the roadmap using the admin interface

### Creating Custom Roadmaps

1. Log in to your account
2. Click on "Create Custom Roadmap" in the navigation menu
3. Fill in the roadmap details and submit
4. Add nodes to your roadmap with titles, descriptions, and resource links
5. Publish your roadmap to make it available to other users

### Database Migrations

When making changes to the database models:

```
flask db migrate -m "Description of changes"
flask db upgrade
```

## Deployment on Render

EdgeRoute can be easily deployed on [Render](https://render.com/) using the included configuration files.

### Prerequisites

1. Create a [Render](https://render.com/) account
2. Create a [Supabase](https://supabase.com/) account and project (for database and authentication)

### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. Connect your GitHub repository to Render
3. Create a new Web Service in Render and select your repository
4. Render will automatically detect the `render.yaml` configuration
5. Set up the required environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string (from Supabase)
   - `SECRET_KEY`: A secure random string
   - `FLASK_APP`: Set to `app`
   - `FLASK_ENV`: Set to `production`
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key
   - `SUPABASE_SERVICE_KEY`: Your Supabase service key
6. Deploy the application

### Updating Your Deployment

Render automatically deploys new changes when you push to your repository's main branch.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
