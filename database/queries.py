import pandas as pd
from sqlalchemy import create_engine, text
import os

# 1. Connect to SQLite
current_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(current_dir, 'data.db')
engine = create_engine(f'sqlite:///{DATABASE_PATH}')

# Platform Distribution
# Note: Using json_each since SQLite stores arrays as JSON strings
platform_query = """
SELECT 
    value as platform,
    COUNT(*) as game_count
FROM steam_games,
json_each(platforms)
GROUP BY value
ORDER BY game_count DESC
"""

# Price Distribution by Platform
price_platform_query = """
WITH cte AS (
    SELECT 
        ROUND(CAST("price_initial (USD)" AS FLOAT) / 5.0) * 5 AS rounded_price,
        COUNT(DISTINCT steam_appid) AS app_count,
        platforms
    FROM steam_games
    GROUP BY rounded_price, platforms
    HAVING COUNT(DISTINCT steam_appid) > 5
)
SELECT 
    json_each.value as platform,
    AVG(rounded_price) as avg_price,
    MIN(rounded_price) as min_price,
    MAX(rounded_price) as max_price
FROM cte, json_each(cte.platforms)
GROUP BY json_each.value
"""

# Create DataFrames
df_platform = pd.read_sql(platform_query, engine)
df_price = pd.read_sql(price_platform_query, engine)

def get_review_dist_by_platform(platform=None):
    if platform != 'All':
        query = """
        SELECT 
            review_score_desc AS review_category,
            COUNT(DISTINCT steam_appid) AS game_count
        FROM steam_games,
        json_each(platforms)
        WHERE review_score_desc NOT LIKE '%user reviews%'
            AND json_each.value = :platform
        GROUP BY review_category
        ORDER BY game_count DESC
        """
        params = {"platform": platform}
    else:
        query = """
        SELECT 
            review_score_desc AS review_category,
            COUNT(DISTINCT steam_appid) AS game_count
        FROM steam_games
        WHERE review_score_desc NOT LIKE '%user reviews%'
        GROUP BY review_category
        ORDER BY game_count DESC
        """
        params = {}

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        return pd.DataFrame(result.fetchall(), columns=result.keys())

def get_top_games_by_platform(platform=None):
    if platform != 'All':
        query = """
        SELECT 
            name,
            review_score,
            total_reviews,
            metacritic,
            "price_initial (USD)"
        FROM steam_games,
        json_each(platforms)
        WHERE metacritic IS NOT NULL
            AND total_reviews > 1000
            AND json_each.value = :platform
        ORDER BY metacritic DESC, total_reviews DESC
        LIMIT 5
        """
        params = {"platform": platform}
    else:
        query = """
        SELECT 
            name,
            review_score,
            total_reviews,
            metacritic,
            "price_initial (USD)"
        FROM steam_games
        WHERE metacritic IS NOT NULL
            AND total_reviews > 1000
        ORDER BY metacritic DESC, total_reviews DESC
        LIMIT 5
        """
        params = {}

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        return pd.DataFrame(result.fetchall(), columns=result.keys())

engine.dispose()