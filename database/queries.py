import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URL

# 1. Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Platform Distribution
platform_query = """
SELECT 
    unnest(platforms) as platform,
    COUNT(*) as game_count
FROM steam_games_parsed
GROUP BY unnest(platforms)
ORDER BY game_count DESC
"""

# Price Distribution by Platform
price_platform_query = """
with cte as 
(
SELECT 
    ROUND(sgp."price_initial (USD)" / 5.0) * 5 AS rounded_price,
    COUNT(DISTINCT sgp.steam_appid) AS app_count
    ,platforms
FROM steam_games_parsed sgp
GROUP BY rounded_price,platforms
HAVING COUNT(DISTINCT sgp.steam_appid) > 5
)
SELECT 
    unnest(platforms) as platform,
    AVG(rounded_price) as avg_price,
    MIN(rounded_price) as min_price,
    MAX(rounded_price) as max_price
FROM cte
GROUP BY unnest(platforms)
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
        FROM steam_games_parsed
        WHERE review_score_desc !~ 'user reviews'
            AND :platform = ANY(platforms)
        GROUP BY review_category
        ORDER BY game_count DESC
        """
        params = {"platform": platform}
    else:
        query = """
        SELECT 
            review_score_desc AS review_category,
            COUNT(DISTINCT steam_appid) AS game_count
        FROM steam_games_parsed
        WHERE review_score_desc !~ 'user reviews'
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
        FROM steam_games_parsed
        WHERE metacritic IS NOT NULL
            AND total_reviews > 1000
            AND :platform = ANY(platforms)
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
        FROM steam_games_parsed
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