from flask import Blueprint, render_template, request
from .charts import (platform_distribution, price_distribution, 
                    review_score_distribution, top_games)
from database.queries import (df_platform, df_price,
                            get_top_games_by_platform, get_review_dist_by_platform)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Main dashboard page showing all charts"""
    
    # Get unique platforms for filter dropdown
    valid_platforms = df_platform['platform'].unique().tolist()
    
    # Get platform filter from request, default to 'All'
    selected_platform = request.args.get('platform', 'All')
    if selected_platform != 'All' and selected_platform not in valid_platforms:
        selected_platform = 'All'
    
    # Get carousel_index and attempt to convert to integer
    try:
        carousel_index = int(request.args.get('carouselIndex', 0))
    except ValueError:
        carousel_index = 0

    # Get top games for selected platform
    df_top = get_top_games_by_platform(selected_platform)
    df_reviews = get_review_dist_by_platform(selected_platform)
    
    # Generate all charts
    platform_chart = platform_distribution(df_platform)
    price_chart = price_distribution(df_price)
    review_chart = review_score_distribution(df_reviews)
    top_games_chart = top_games(df_top)
    
    # Convert charts to JSON for Vega-Lite
    charts = {
        'platform_chart': platform_chart.to_dict(),
        'price_chart': price_chart.to_dict(),
        'review_chart': review_chart.to_dict(),
        'top_games': top_games_chart.to_dict()
    }
    
    return render_template('dashboard.html', 
                           charts=charts, 
                           platforms=valid_platforms,
                           selected_platform=selected_platform,
                           carouselIndex=carousel_index)