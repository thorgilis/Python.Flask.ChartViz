from database.queries import (
    get_platform_distribution,
    get_price_distribution,
    get_review_distribution,
    get_top_games,
    get_platforms,
    get_number_games_per_price_band,
)
from ..charts import (
    platform_distribution,
    price_distribution,
    review_score_distribution,
    top_games,
    price_bracket,
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
    df_price_band = get_number_games_per_price_band(selected_platform)
    
    # Generate all charts
    platform_chart = platform_distribution(df_platform)
    price_chart = price_distribution(df_price)
    review_chart = review_score_distribution(df_reviews)
    top_games_chart = top_games(df_top)
    price_bracket_chart = price_bracket(df_price_band)
    
    # Convert charts to dictionaries for Vega-Lite
    charts = {
        'platform_chart': platform_chart.to_dict(),
        'price_chart': price_chart.to_dict(),
        'review_chart': review_chart.to_dict(),
        'top_games': top_games_chart.to_dict(),
        'price_box': price_bracket_chart.to_dict()
    }
    
    return valid_platforms, selected_platform, charts