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
│   └── queries.py
├── static
│   └── css
│       └── style.css
├── templates
│   ├── base.html
│   └── dashboard.html
├── config.py
├── requirements.txt
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

3. Configure the database connection in `config.py`.

## Running the Application

To run the application, execute the following command:

```bash
python run.py
```

The application will be accessible at `http://127.0.0.1:5000`.

## Usage

- Navigate to the dashboard to view the interactive charts.
- Use the platform filters to customize the displayed data.

## License

This project is licensed under the MIT License.