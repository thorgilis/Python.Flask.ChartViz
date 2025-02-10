from flask import Blueprint, render_template, request
from .charts import (platform_distribution,price_distribution
                    ,review_score_distribution,top_games
                    ,price_bracket)
from database.queries import (get_platform_distribution,get_price_distribution
                              ,get_review_distribution,get_top_games,get_platforms
                              ,get_number_games_per_price_band)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Main dashboard page showing all charts"""

    # Get unique platforms for filter dropdown
    valid_platforms = get_platforms()
    
    # Get platform filter from request, default to 'All'
    selected_platform = request.args.get('platform', 'All')
    if selected_platform == 'All' or selected_platform not in valid_platforms:
        selected_platform = None
    
    # Get carousel_index and attempt to convert to integer
    try:
        carousel_index = int(request.args.get('carouselIndex', 0))
    except ValueError:
        carousel_index = 0

    # Get top games for selected platform
    df_platform = get_platform_distribution()
    df_top = get_top_games(selected_platform)
    df_reviews = get_review_distribution(selected_platform)
    df_price = get_price_distribution(selected_platform)
    df_price_band = get_number_games_per_price_band(selected_platform)
    
    # Generate all charts
    platform_chart = platform_distribution(df_platform)
    price_chart = price_distribution(df_price)
    review_chart = review_score_distribution(df_reviews)
    top_games_chart = top_games(df_top)
    price_bracket_chart = price_bracket(df_price_band)
    
    # Convert charts to JSON for Vega-Lite
    charts = {
        'platform_chart': platform_chart.to_dict(),
        'price_chart': price_chart.to_dict(),
        'review_chart': review_chart.to_dict(),
        'top_games': top_games_chart.to_dict(),
        'price_box': price_bracket_chart.to_dict()
    }
    
    return render_template('dashboard.html', 
                           charts=charts, 
                           platforms=valid_platforms,
                           selected_platform=selected_platform,
                           carouselIndex=carousel_index)