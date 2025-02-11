from database.queries import (
    get_platform_distribution,
    get_price_distribution,
    get_review_distribution,
    get_top_games,
    get_platforms,
    get_price_band_distribution,
)
from app.charts import (
    platform_distribution,
    price_distribution,
    review_score_distribution,
    top_games,
    price_band_distribution,
)

def get_dashboard_data(requested_platform):
    # Get unique platforms
    valid_platforms = get_platforms()

    # Validate platform; if filter is 'All' or invalid, reset to None
    if requested_platform == 'All' or requested_platform not in valid_platforms:
        selected_platform = None
    else:
        selected_platform = requested_platform

    # Get dataframes based on the selected platform
    df_platform = get_platform_distribution()
    df_top = get_top_games(selected_platform)
    df_reviews = get_review_distribution(selected_platform)
    df_price = get_price_distribution(selected_platform)
    df_price_band = get_price_band_distribution(selected_platform)
    
    # Generate all charts
    platform_chart = platform_distribution(df_platform)
    price_chart = price_distribution(df_price)
    review_chart = review_score_distribution(df_reviews)
    top_games_chart = top_games(df_top)
    price_band_chart = price_band_distribution(df_price_band)
    
    # Convert charts to dictionaries for Vega-Lite
    charts = {
        'platform_chart': platform_chart.to_dict(),
        'price_chart': price_chart.to_dict(),
        'review_chart': review_chart.to_dict(),
        'top_games': top_games_chart.to_dict(),
        'price_box': price_band_chart.to_dict()
    }
    
    return valid_platforms, selected_platform, charts