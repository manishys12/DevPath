# EdgeRoute - Interactive Learning Roadmap Platform


EdgeRoute (formerly DevPath) is a Flask-based web application that provides interactive learning roadmaps for various technology paths. Users can track their progress through roadmaps, participate in discussions, and manage their learning journey.

## Features

- **Interactive Roadmaps**: Explore detailed learning paths for various technologies
- **Progress Tracking**: Mark topics as completed and track your learning progress
- **User Profiles**: Personalized profiles showing your progress and activity
- **Discussion**: Comment on roadmap topics to share insights or ask questions
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Multiple Deployment Options**: Deploy on traditional servers, Docker, Heroku, or Render

## Demo

You can view a live demo of EdgeRoute at 

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/manish12ys/EdgeRoute.git
   cd EdgeRoute
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Create a .env file with the following variables
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secure-secret-key
   ```

5. Initialize the database:
   ```bash
   python run.py
   ```

## Usage

1. Start the development server:
   ```bash
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

## Deployment

EdgeRoute can be deployed in various environments:

- **Traditional Server**: Deploy with Nginx, Gunicorn, and PostgreSQL
- **Docker**: Use the provided Dockerfile and docker-compose.yml
- **Heroku**: Deploy with the included Procfile
- **Render**: One-click deployment with the render.yaml blueprint

For detailed deployment instructions, see the [DEPLOYMENT.md](DEPLOYMENT.md) file.

## Project Structure

```
EdgeRoute/
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
├── wsgi.py                 # WSGI entry point for production
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── render.yaml             # Render deployment configuration
└── run.py                  # Development server entry point
```

## Development

### Adding New Roadmaps

1. Create a new JSON file in the `roadmap_data` directory
2. Add the roadmap metadata to `roadmap_data/roadmaps.json`
3. Import the roadmap using the admin interface

### Database Migrations

When making changes to the database models:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Render](https://render.com/) for hosting

## Contact

Manish Yepuri - [@manish12ys](https://github.com/manish12ys)

Project Link: [https://github.com/manish12ys/EdgeRoute](https://github.com/manish12ys/EdgeRoute)
