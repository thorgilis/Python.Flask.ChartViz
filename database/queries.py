import os
from typing import Optional, Any, Dict

import pandas as pd
from sqlalchemy import create_engine, text

# Database connection setup
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(current_dir, 'data.db')
    print(f"Database path: {DATABASE_PATH}")
    engine = create_engine(f'sqlite:///{DATABASE_PATH}')
except Exception as e:
    print(f"Error connecting to database: {e}")

def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Execute a given SQL query with optional parameters and return the results as a DataFrame.
    
    Args:
        query: The SQL query string to execute.
        params: Optional dictionary of parameters to bind into the query.

    Returns:
        DataFrame containing the query results.
    """
    try:
        with engine.connect() as conn:
            # Execute the query with parameters (if provided) using SQLAlchemy's text construct
            result = conn.execute(text(query), params or {})
            # Convert results into a DataFrame using fetched rows and column names
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

def get_platforms() -> list:
    """
    Retrieve distinct platforms from the database.
    
    Uses SQLite's json_each() function to extract elements from the 'platforms' JSON array
    stored in the 'steam_games' table.

    Returns:
        A list of platform names.
    """
    query = """
    SELECT DISTINCT json_each.value AS platform
    FROM steam_games,
         json_each(platforms)
    """
    platforms = execute_query(query)
    print(platforms)
    return list(platforms['platform'])

def get_platform_distribution(platform: Optional[str] = None) -> pd.DataFrame:
    """
    Get the distribution of games per platform.
    
    If a platform is specified, filter results to that platform using a parameterized query.
    
    Args:
        platform: Optional platform name to filter by.
    
    Returns:
        DataFrame with a count of games per platform.
    """
    query = """
    SELECT 
        value AS platform,
        COUNT(DISTINCT steam_appid) AS game_count
    FROM steam_games,
         json_each(platforms)
    WHERE 1=1
    {platform_filter}
    GROUP BY value
    ORDER BY game_count DESC
    """
    # Append a platform filter clause if a specific platform is given
    platform_filter = "AND json_each.value = :platform" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    params = {"platform": platform} if platform else None
    return execute_query(final_query, params)

def get_price_distribution(platform: Optional[str] = None) -> pd.DataFrame:
    """
    Compute distribution of game prices by platform.
    
    Steps:
      1. Rounds the initial price to the nearest 5-dollar increment.
      2. Filters out games where the price is 0 or below.
      3. Aggregates data to compute average, minimum, and maximum price per platform.
    
    Args:
        platform: Optional platform name to filter by.
    
    Returns:
        DataFrame with average, minimum, and maximum price per platform.
    """
    query = """
    WITH price_data AS (
        SELECT 
            steam_appid,
            ROUND(CAST("price_initial (USD)" AS FLOAT) / 5.0) * 5 AS rounded_price,
            platforms
        FROM steam_games
        WHERE "price_initial (USD)" > 0
    ),
    price_data_filtered AS (
        SELECT platforms, rounded_price, COUNT(DISTINCT steam_appid) AS game_count
        FROM price_data
        GROUP BY platforms, rounded_price 
        HAVING game_count > 5
    )
    SELECT 
        json_each.value AS platform,
        AVG(rounded_price) AS avg_price,
        MIN(rounded_price) AS min_price,
        MAX(rounded_price) AS max_price
    FROM price_data_filtered,
         json_each(platforms)
    WHERE 1=1
    {platform_filter}
    GROUP BY json_each.value
    ORDER BY game_count DESC
    """
    # Add filter if a platform is provided
    platform_filter = "AND json_each.value = :platform" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    params = {"platform": platform} if platform else None
    return execute_query(final_query, params)

def get_review_distribution(platform: Optional[str] = None) -> pd.DataFrame:
    """
    Retrieve review distribution by category for games.
    
    Excludes rows where review_score_desc contains typical 'user reviews' to avoid outliers.
    
    Args:
        platform: Optional platform name to filter by.
    
    Returns:
        DataFrame with game count for each review category.
    """
    query = """
    SELECT 
        review_score_desc AS review_category,
        COUNT(DISTINCT steam_appid) AS game_count
    FROM steam_games,
         json_each(platforms)
    WHERE review_score_desc NOT LIKE '%user reviews%'
    {platform_filter}
    GROUP BY review_category
    ORDER BY game_count DESC
    """
    platform_filter = "AND json_each.value = :platform" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    params = {"platform": platform} if platform else None
    return execute_query(final_query, params)

def get_top_games(platform: Optional[str] = None) -> pd.DataFrame:
    """
    Retrieve the top 5 games based on metacritic score and review count.
    
    Filters out games with a NULL metacritic score and those with fewer than or equal to 1000 reviews.
    Further filters by platform if provided.
    
    Args:
        platform: Optional platform name to filter by.
    
    Returns:
        DataFrame containing details of the top games.
    """
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
    {platform_filter}
    GROUP BY steam_appid
    ORDER BY metacritic DESC, total_reviews DESC
    LIMIT 5
    """
    platform_filter = "AND json_each.value = :platform" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    params = {"platform": platform} if platform else None
    return execute_query(final_query, params)

def get_price_band_distribution(platform: Optional[str] = None) -> pd.DataFrame:
    """
    Count the number of games that fall into predefined price bands.
    
    Price bands:
      - '0-30'
      - '31-60'
      - '61-90'
      - '91-120'
      - '>120'
    
    Only bands with more than 5 games (per platform) are considered.
    
    Args:
        platform: Optional platform name to filter by.
    
    Returns:
        DataFrame with price bands and corresponding game counts.
    """
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
        FROM steam_games
        WHERE "price_initial (USD)" > 0
    ),
    price_data_filtered AS (
        SELECT 
            platforms,
            price_bracket,
            COUNT(DISTINCT steam_appid) AS game_count
        FROM price_data
        GROUP BY platforms, price_bracket 
        HAVING game_count > 5
    )
    SELECT 
        price_bracket,
        SUM(game_count) AS game_count
    FROM price_data_filtered,
         json_each(platforms)
    WHERE 1=1
    {platform_filter}
    GROUP BY price_bracket
    ORDER BY price_bracket
    """
    platform_filter = "AND json_each.value = :platform" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    params = {"platform": platform} if platform else None
    return execute_query(final_query, params)

# Cleanup connection
engine.dispose()