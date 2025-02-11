import altair
import numpy as np
import pandas as pd  # Assuming df is a pandas DataFrame

def base_chart_props(chart: altair.Chart, title: str) -> altair.Chart:
    """
    Applies common properties to all charts.

    Args:
        chart: The Altair chart to configure.
        title: The chart title.
        
    Returns:
        The chart with common properties applied.
    """
    return chart.properties(
        title=title,
        width='container',
        height='container',
        autosize={"type": "fit", "contains": "padding"}  # Adjust chart size to fit container with internal padding
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

def platform_distribution(df: pd.DataFrame) -> altair.Chart:
    """
    Create a bar chart showing distribution of games by platform.
    
    Args:
        df: A pandas DataFrame containing 'game_count' and 'platform' columns.
        
    Returns:
        An Altair Chart object with the common properties applied.
    """
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'game_count:Q',
            title='Number of Games'
        ),
        y=altair.Y(
            'platform:N',
            title='Platform',
            sort='-x'  # Sort descending by game_count
        ),
        color=altair.Color(
            'platform:N',
            legend=None,
            scale=altair.Scale(scheme='magma')  # Use the magma color scheme for consistency
        ),
        tooltip=[
            altair.Tooltip('platform:N', title='Platform'),
            altair.Tooltip('game_count:Q', format=',', title='Number of Games')
        ]
    )
    return base_chart_props(chart, 'Distribution of Games by Platform')

def price_distribution(df: pd.DataFrame) -> altair.Chart:
    """
    Create a chart showing average price and price range by platform.
    
    Args:
        df: A pandas DataFrame containing 'platform', 'avg_price', 'min_price', and 'max_price' columns.
    
    Returns:
        An Altair Chart object with the common properties applied.
    """
    # Base chart defines common Y encoding
    base = altair.Chart(df).encode(
        y=altair.Y(
            'platform:N',
            title='Platform',
            sort='-x'  # Sort platforms descending by x axis value
        )
    )
    
    # Bar chart for average price
    bars = base.mark_bar().encode(
        x=altair.X(
            'avg_price:Q',
            title='Average Price (USD)'
        ),
        color=altair.Color(
            'platform:N',
            legend=None,
            scale=altair.Scale(scheme='magma')
        ),
        tooltip=[
            altair.Tooltip('platform:N', title='Platform'),
            altair.Tooltip('avg_price:Q', format='$,.2f', title='Average Price'),
            altair.Tooltip('min_price:Q', format='$,.2f', title='Min Price'),
            altair.Tooltip('max_price:Q', format='$,.2f', title='Max Price')
        ]
    )
    
    # Error bars to show min and max price range
    error_bars = base.mark_errorbar().encode(
        x=altair.X(
            'min_price:Q',
            title='Average Price (USD)'  # Label matches the bar chart for consistency
        ),
        x2='max_price:Q'  # Defines the end of the error bar
    )
    
    # Combine bar chart and error bars using layering
    chart = bars + error_bars
    return base_chart_props(chart, 'Price Distribution by Platform')

def review_score_distribution(df: pd.DataFrame) -> altair.Chart:
    """
    Create a bar chart showing distribution of games by review category.
    
    Args:
        df: A pandas DataFrame containing 'game_count' and 'review_category' columns.
        
    Returns:
        An Altair Chart object with the common properties applied.
    """
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'game_count:Q',
            title='Number of Games'
        ),
        y=altair.Y(
            'review_category:N',
            title='Review Category',
            sort='-x'  # Sort descending by game_count
        ),
        color=altair.Color(
            'game_count:N',  # Although using game_count for color, this may be adjusted if needed
            legend=None,
            scale=altair.Scale(scheme='category10')  # Use category10 color scheme
        ),
        tooltip=[
            altair.Tooltip('review_category:N', title='Review Category'),
            altair.Tooltip('game_count:Q', format=',', title='Number of Games')
        ]
    )
    return base_chart_props(chart, 'Distribution of Review Scores')

def top_games(df: pd.DataFrame) -> altair.Chart:
    """
    Create a bar chart showing top 5 games by review score.
    
    Args:
        df: A pandas DataFrame containing 'name', 'metacritic', 'review_score', and 'total_reviews'.
        
    Returns:
        An Altair Chart object with the common properties applied.
    """
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'name:N',
            title='Game Name',
            sort='-y',  # Sort bars by y value (review score) in descending order
            axis=altair.Axis(labelAngle=-45)  # Tilt labels for better readability
        ),
        y=altair.Y(
            'metacritic:Q',
            title='Review Score'
        ),
        color=altair.Color(
            'name:N',
            legend=None,
            scale=altair.Scale(scheme='category10')
        ), 
        tooltip=[
            altair.Tooltip('name:N', title='Game Name'),
            altair.Tooltip('metacritic:Q', format=',', title='Metacritic'),
            altair.Tooltip('review_score:Q', format=',', title='User Review Score'),
            altair.Tooltip('total_reviews:Q', format=',', title='Total User Reviews')
        ]
    )
    
    # Configure title to be anchored in the middle.
    return base_chart_props(chart, 'Top 5 Games by Review Score').configure_title(anchor='middle')

def price_bracket(df: pd.DataFrame) -> altair.Chart:
    """
    Create a bar chart showing distribution of games by price bracket on a logarithmic scale.
    
    This function adds a 'log_value' column to the dataframe representing the log10 of game_count.
    
    Args:
        df: A pandas DataFrame containing 'game_count' and 'price_bracket' columns.
        
    Returns:
        An Altair Chart object with the common properties applied.
    """
    # Compute the logarithm of game_count to better visualize the distribution if counts span several orders of magnitude.
    df['log_value'] = df['game_count'].apply(lambda x: np.log10(x))
    
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'price_bracket:N',
            title='Price Band',
            sort='x'  # Sort in natural order of price_bracket values
        ),
        y=altair.Y(
            'log_value:Q',
            title='Number of Games'
        ),
        color=altair.Color(
            'price_bracket:N',
            legend=None,
            scale=altair.Scale(scheme='category10')
        ),
        tooltip=[
            altair.Tooltip('price_bracket:N', title='Price Band (USD)'),
            altair.Tooltip('game_count:Q', format=',', title='Number of Games'),
            altair.Tooltip('log_value:Q', format=',', title='Log Value')
        ]
    )
    return base_chart_props(chart, 'Distribution of Games by Price Band (Log Scale)')