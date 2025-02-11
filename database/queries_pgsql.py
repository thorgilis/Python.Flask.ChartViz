import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URL 

# Database connection setup
try:
    if DATABASE_URL is not None:
        engine = create_engine(DATABASE_URL)
except Exception as e:
    print(f"Error connecting to database: {e}")

def execute_query(query, params=None):
    """Execute query and return DataFrame"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

def get_platforms():
    query = """
    SELECT DISTINCT unnest(platforms) as platform
    FROM steam_games_parsed
    group by unnest(platforms)
    """
    platforms = execute_query(query)
    return list(platforms['platform'])

def get_platform_distribution(platform=None):
    query = """
    SELECT 
        platform,
        COUNT(*) AS game_count
    FROM (
        SELECT unnest(platforms) AS platform
        FROM steam_games_parsed
    ) AS p
    WHERE 1=1
    {platform_filter}
    GROUP BY platform
    ORDER BY game_count DESC
    """
    platform_filter = "AND (:platform IS NULL OR platform = :platform)" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    return execute_query(final_query, {"platform": platform} if platform else None)

def get_price_distribution(platform=None):
    query = """
    WITH price_data AS (
        SELECT 
            steam_appid,
            ROUND(CAST("price_initial (USD)" AS FLOAT) / 5.0) * 5 AS rounded_price,
            platforms
        FROM steam_games_parsed
        WHERE "price_initial (USD)" > 0
    ),
    price_data_filtered AS (
        SELECT 
            platforms,
            rounded_price,
            COUNT(DISTINCT steam_appid) AS game_count
        FROM price_data
        GROUP BY platforms, rounded_price 
        HAVING COUNT(DISTINCT steam_appid) > 5
    )
    SELECT 
        platform,
        AVG(rounded_price) AS avg_price,
        MIN(rounded_price) AS min_price,
        MAX(rounded_price) AS max_price
    FROM price_data_filtered,
         unnest(platforms) AS platform
    WHERE 1=1
    {platform_filter}
    GROUP BY platform
    ORDER BY avg_price DESC
    """
    platform_filter = "AND (:platform IS NULL OR platform = :platform)" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    return execute_query(final_query, {"platform": platform} if platform else None)

def get_review_distribution(platform=None):
    query = """
    SELECT 
        review_score_desc AS review_category,
        COUNT(DISTINCT steam_appid) AS game_count
    FROM steam_games_parsed,
         unnest(platforms) AS platform
    WHERE review_score_desc NOT LIKE '%user reviews%'
    {platform_filter}
    GROUP BY review_score_desc
    ORDER BY game_count DESC
    """
    platform_filter = "AND (:platform IS NULL OR platform = :platform)" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    return execute_query(final_query, {"platform": platform} if platform else None)

def get_top_games(platform=None):
    query = """
    SELECT 
        name,
        review_score,
        total_reviews,
        metacritic,
        "price_initial (USD)"
    FROM steam_games_parsed,
         unnest(platforms) AS platform
    WHERE metacritic IS NOT NULL
      AND total_reviews > 1000
    {platform_filter}
    GROUP BY steam_appid, name, review_score, total_reviews, metacritic, "price_initial (USD)"
    ORDER BY metacritic DESC, total_reviews DESC
    LIMIT 5
    """
    platform_filter = "AND (:platform IS NULL OR platform = :platform)" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    return execute_query(final_query, {"platform": platform} if platform else None)

def get_number_games_per_price_band(platform=None):
    query = """
    WITH price_data AS (
        SELECT 
            steam_appid,
            CASE
                WHEN "price_initial (USD)" <= 30 THEN '0-30'
                WHEN "price_initial (USD)" <= 60 THEN '31-60'
                WHEN "price_initial (USD)" <= 90 THEN '61-90'
                WHEN "price_initial (USD)" <= 120 THEN '91-120'
                ELSE '>120'
            END AS price_bracket,
            platforms
        FROM steam_games_parsed
        WHERE "price_initial (USD)" > 0
    ),
    price_data_filtered AS (
        SELECT 
            platforms,
            price_bracket,
            COUNT(DISTINCT steam_appid) AS game_count
        FROM price_data
        GROUP BY platforms, price_bracket 
        HAVING COUNT(DISTINCT steam_appid) > 5
    )
    SELECT 
        price_bracket,
        SUM(game_count) AS game_count
    FROM price_data_filtered,
         unnest(platforms) AS platform
    WHERE 1=1
    {platform_filter}
    GROUP BY price_bracket
    ORDER BY price_bracket
    """
    platform_filter = "AND (:platform IS NULL OR platform = :platform)" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    return execute_query(final_query, {"platform": platform} if platform else None)

# Cleanup connection
engine.dispose()