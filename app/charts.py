import altair
import pandas as pd

def platform_distribution(df):
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X('game_count:Q', title='Number of Games'),
        y=altair.Y('platform:N', title='Platform', sort='-x'),
        color=altair.Color('platform:N', legend=None),
        tooltip=['platform', 'game_count']
    ).properties(
        title='Distribution of Games by Platform',
        width='container',
        height='container',
        autosize={
            "type": "fit",
            "contains": "padding"
        }
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    return chart

def price_distribution(df):
    base = altair.Chart(df).encode(
        y=altair.Y('platform:N', title='Platform', sort='-x')
    )
    
    bars = base.mark_bar().encode(
        x=altair.X('avg_price:Q', title='Average Price (USD)'),
        color=altair.Color('platform:N', legend=None),
        tooltip=['platform', 'avg_price', 'min_price', 'max_price']
    )
    
    error_bars = base.mark_errorbar().encode(
        x='min_price:Q',
        x2='max_price:Q'
    )
    
    chart = (bars + error_bars).properties(
        title='Price Distribution by Platform',
        width='container',
        height='container',
        autosize={
            "type": "fit",
            "contains": "padding"
        }
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    return chart

def review_score_distribution(df, category_col='review_category', count_col='game_count',
                              ordering=None, color_mapping=None):
    # If an ordering isn’t provided, order the categories by descending total counts
    if ordering is None:
        ordering = list(df.sort_values(count_col, ascending=False)[category_col].unique())
    
    # If no color mapping is provided, generate a color palette using a default categorical scheme.
    if color_mapping is None:
        default_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                          '#bcbd22', '#17becf']
        color_mapping = {cat: default_colors[i % len(default_colors)]
                         for i, cat in enumerate(ordering)}
    
    # Create the chart
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X(f'{count_col}:Q', title='Number of Games'),
        y=altair.Y(f'{category_col}:N', 
                   title='Review Category',
                   sort=ordering),
        color=altair.Color(f'{category_col}:N', 
                           scale=altair.Scale(
                               domain=list(color_mapping.keys()),
                               range=list(color_mapping.values())
                           ),
                           legend=None),
        tooltip=[category_col, count_col]
    ).properties(
        title='Distribution of Review Scores',
        width='container',
        height='container',
        autosize={
            "type": "fit",
            "contains": "padding"
        }
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    return chart

def top_games(df):
    """
    Create a bar chart showing top 5 games by review score using Altair
    """
    chart = altair.Chart(df).mark_bar().encode(
        x=altair.X('name:N', 
                   title='Game Name',
                   sort='-y',
                   axis=altair.Axis(labelAngle=-45)),
        y=altair.Y('metacritic:Q', 
                   title='Review Score'),
        color=altair.value('#1f77b4'),
        tooltip=['name', 
                altair.Tooltip('metacritic:Q', format='.2f')]
    ).properties(
        title='Top 5 Games by Review Score',
        width='container',
        height='container',
        autosize={
            "type": "fit",
            "contains": "padding"
        }
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        anchor='middle'
    )
    
    return chart