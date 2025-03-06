import pandas as pd
from sqlalchemy import create_engine, text
from pandas import DataFrame
from typing import Optional, Dict, Any

# Setup database connection engine.
try:
    DATABASE_URL = ''
    engine = create_engine(DATABASE_URL)
except Exception as e:
    # Log the error if the engine cannot be initialized.
    print(f"Error connecting to database: {e}")

def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> DataFrame:
    """
    Execute a SQL query and return the results as a Pandas DataFrame.
    
    Parameters:
        query (str): The SQL query to execute.
        params (Optional[Dict[str, Any]]): Optional parameters for the query.
    
    Returns:
        DataFrame: Query results as a DataFrame; empty DataFrame on error.
    """
    try:
        with engine.connect() as conn:
            # Execute the query with the passed parameters (if any)
            result = conn.execute(text(query), params or {})
            # Fetch all rows and use result keys as DataFrame columns.
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

def get_platforms() -> list:
    """
    Retrieve a distinct list of platforms from the 'steam_games_parsed' table.
    
    Returns:
        list: A list of unique platforms.
    """
    query = """
    SELECT DISTINCT unnest(platforms) as platform
    FROM steam_games_parsed
    GROUP BY unnest(platforms)
    """
    platforms = execute_query(query)
    # Convert the 'platform' column into a list.
    return list(platforms['platform'])

def get_platform_distribution(platform: Optional[str] = None) -> DataFrame:
    """
    Retrieve the distribution of games per platform.
    
    Parameters:
        platform (Optional[str]): Filter results by this platform, if specified.
    
    Returns:
        DataFrame: Contains 'platform' and the corresponding game count.
    """
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
    # Construct filter clause if platform is provided.
    platform_filter = "AND (:platform IS NULL OR platform = :platform)" if platform else ""
    final_query = query.format(platform_filter=platform_filter)
    query_params = {"platform": platform} if platform else None
    return execute_query(final_query, query_params)

def get_price_distribution(platform: Optional[str] = None) -> DataFrame:
    """
    Retrieve average, minimum, and maximum prices per platform based on a price band.
    
    Parameters:
        platform (Optional[str]): Filter results by this platform, if specified.
    
    Returns:
        DataFrame: Contains price distribution stats for each platform.
    """
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
    query_params = {"platform": platform} if platform else None
    return execute_query(final_query, query_params)

def get_review_distribution(platform: Optional[str] = None) -> DataFrame:
    """
    Retrieve the distribution of games by review category.
    
    Parameters:
        platform (Optional[str]): Filter results by this platform, if specified.
    
    Returns:
        DataFrame: Contains review categories and the corresponding game counts.
    """
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
    query_params = {"platform": platform} if platform else None
    return execute_query(final_query, query_params)

def get_top_games(platform: Optional[str] = None) -> DataFrame:
    """
    Retrieve top-rated games with metacritic scores and high review counts.
    
    Parameters:
        platform (Optional[str]): Filter results by this platform, if specified.
    
    Returns:
        DataFrame: Contains top 5 games meeting the criteria.
    """
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
    query_params = {"platform": platform} if platform else None
    return execute_query(final_query, query_params)

def get_number_games_per_price_band(platform: Optional[str] = None) -> DataFrame:
    """
    Get the number of games per price band.
    
    Price bands are defined as:
        - '0-30'
        - '31-60'
        - '61-90'
        - '91-120'
        - '>120'
    
    Parameters:
        platform (Optional[str]): Filter results by this platform, if specified.
    
    Returns:
        DataFrame: Contains price brackets and the corresponding game counts.
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
    query_params = {"platform": platform} if platform else None
    return execute_query(final_query, query_params)

# Cleanup connection resources when the script finishes to ensure no open connections.
engine.dispose()