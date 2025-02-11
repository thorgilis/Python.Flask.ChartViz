from flask import Blueprint, render_template, request
from .services.dashboard_service import get_dashboard_data

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Main dashboard page showing all charts"""
    
    # Get carousel_index from the query parameter
    try:
        carousel_index = int(request.args.get('carouselIndex', 0))
    except ValueError:
        carousel_index = 0

    # Get the platform filter from the query parameter
    requested_platform = request.args.get('platform', 'All')
    
    # Use the service to fetch data
    valid_platforms, selected_platform, charts = get_dashboard_data(requested_platform)
    
    return render_template(
        'dashboard.html',
        charts=charts,
        platforms=valid_platforms,
        selected_platform=selected_platform,
        carouselIndex=carousel_index
    )