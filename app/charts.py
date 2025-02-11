import altair
import numpy as np

def base_chart_props(chart, title):
    """
    Applies common properties to all charts.
    """
    return chart.properties(
        title=title,
        width='container',
        height='container',
        autosize={"type": "fit", "contains": "padding"}
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

def platform_distribution(df):
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'game_count:Q'
            ,title='Number of Games'
        ),
        y=altair.Y(
            'platform:N'
            ,title='Platform'
            ,sort='-x'
        ),
        color=altair.Color(
            'platform:N'
            ,legend=None
            ,scale=altair.Scale(scheme='magma')
        ),
        tooltip=[
            altair.Tooltip('platform:N', title='Platform'),
            altair.Tooltip('game_count:Q', format=',', title='Number of Games')
        ]
    )
    return base_chart_props(chart, 'Distribution of Games by Platform')

def price_distribution(df):
    base = altair.Chart(df).encode(
        y=altair.Y(
            'platform:N',
            title='Platform',
            sort='-x'
        )
    )
    
    bars = base.mark_bar().encode(
        x=altair.X(
            'avg_price:Q',
            title='Average Price (USD)'
        ),
        color=altair.Color(
            'platform:N'
            ,legend=None
            ,scale=altair.Scale(scheme='magma')
        ),
        tooltip=[
            altair.Tooltip('platform:N', title='Platform'),
            altair.Tooltip('avg_price:Q', format='$,.2f', title='Average Price'),
            altair.Tooltip('min_price:Q', format='$,.2f', title='Min Price'),
            altair.Tooltip('max_price:Q', format='$,.2f', title='Max Price')
        ]
    )
    
    error_bars = base.mark_errorbar().encode(
        x=altair.X(
            'min_price:Q'
            ,title='Average Price (USD)'
        ),
        x2='max_price:Q'
    )
    
    chart = bars + error_bars
    return base_chart_props(chart, 'Price Distribution by Platform')

def review_score_distribution(df):
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'game_count:Q'
            ,title='Number of Games'
        ),
        y=altair.Y(
            'review_category:N'
            ,title='Review Category'
            ,sort='-x'
        ),
        color=altair.Color(
            'game_count:N'
            ,legend=None
            ,scale=altair.Scale(scheme='category10') # ,scale=altair.Scale(scheme='viridis')
        ),
        tooltip=[
            altair.Tooltip('review_category:N', title='Review Category'),
            altair.Tooltip('game_count:Q', format=',', title='Number of Games')
        ]
    )
    return base_chart_props(chart, 'Distribution of Review Scores')

def top_games(df):
    """
    Create a bar chart showing top 5 games by review score using Altair
    """
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'name:N'
            ,title='Game Name'
            ,sort='-y'
            ,axis=altair.Axis(labelAngle=-45)
        ),
        y=altair.Y(
            'metacritic:Q'
            ,title='Review Score'
        ),
        color=altair.Color(
            'name:N'
            ,legend=None
            ,scale=altair.Scale(scheme='category10') # ,scale=altair.Scale(scheme='viridis')
        ), 
        tooltip=[
            altair.Tooltip('name:N', title='Game Name'),
            altair.Tooltip('metacritic:Q', format=',', title='Metacritic'), 
            altair.Tooltip('review_score:Q', format=',', title='User Review Score'), 
            altair.Tooltip('total_reviews:Q', format=',', title='Total User Reviews')
        ]
    )
    
    return base_chart_props(chart, 'Top 5 Games by Review Score').configure_title(anchor='middle')

def price_bracket(df):
    df['log_value'] = df['game_count'].apply(lambda x: np.log10(x))

    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(
            'price_bracket:N',
            title='Price Band',
            sort='x'
        ),
        y=altair.Y(
            'log_value:Q',
            title='Number of Games',
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