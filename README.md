# Interactive Games Dashboard

This project is a web application that provides interactive charts based on data from a PostgreSQL database. It allows users to explore various metrics related to video games, including top games, worst games, top free games, and a comparison of free games versus paid games.

## Features

- Interactive charts that visualize game data.
- Filters for platforms to refine the displayed data.
- Responsive design for a better user experience.

## Project Structure

```
interactive-games-dashboard
├── app
│   ├── __init__.py
│   ├── routes.py
│   └── charts.py
├── database
│   ├── __init__.py
│   ├── data.db
│   ├── queries_pgsql.py
│   └── queries.py
├── services
│   ├── __init__.py
│   └── dashboard_service.py
├── static
│   └── css
│       └── style.css
├── templates
│   ├── base.html
│   └── dashboard.html
├── config
│   └── config.py
├── requirements
│   └── requirements.txt
├── docker
│   └── Dockerfile
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd interactive-games-dashboard
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. You can either:
   - Use the sqlite database included in the repo - No changes required
   - Use a postgresql version of the data (not included in the repo) 
      - Change the following reference in services.dashboard_service.py
         from database.queries import
         to
         from database.queries_pgsql import


## Running the Application

### Using Python

To run the application, execute the following command:

```bash
python run.py
```

The application will be accessible at `http://127.0.0.1:5000`.

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t interactive-games-dashboard .
   ```

2. Build the Docker image, with tags:
   ```bash
   docker build --platform=linux/amd64 -t 192.168.0.63:5000/interactive-games-dashboard:latest .
   ```

3. Push It!!
   ```bash
   docker push 192.168.0.63:5000/interactive-games-dashboard:latest
   ```

4. Or..
   ```bash
   docker build --platform=linux/amd64 -t 192.168.0.63:5000/interactive-games-dashboard:sqlite . \
   && docker push 192.168.0.63:5000/interactive-games-dashboard:sqlite
   ```

## Usage

- Navigate to the dashboard to view the interactive charts.
- Use the platform filters to customize the displayed data.

## License

This project is licensed under the MIT License.