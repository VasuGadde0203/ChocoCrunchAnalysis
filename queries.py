product_queries = {
    "Count products per brand": """
        SELECT brand, COUNT(*) as product_count
        FROM product_info
        GROUP BY brand
    """,

    "Count unique products per brand": """
        SELECT brand, COUNT(DISTINCT product_code) as unique_products
        FROM product_info
        GROUP BY brand
    """,

    "Top 5 brands by product count": """
        SELECT brand, COUNT(*) as product_count
        FROM product_info
        GROUP BY brand
        ORDER BY product_count DESC
        LIMIT 5
    """,

    "Missing product name": """
        SELECT *
        FROM product_info
        WHERE product_name IS NULL OR product_name = ''
    """,

    "Number of unique brands": """
        SELECT COUNT(DISTINCT brand) as unique_brands
        FROM product_info
    """,

    "Products code starting with 3": """
        SELECT *
        FROM product_info
        WHERE product_code LIKE '3%'
    """
}

nutrient_queries = {
    "Top 10 highest calories": """
        SELECT product_code, energy_kcal_value
        FROM nutrient_info
        ORDER BY energy_kcal_value DESC
        LIMIT 10
    """,

    "Average sugar per nova group": """
        SELECT nova_group, AVG(sugars_value) as avg_sugar
        FROM nutrient_info
        GROUP BY nova_group
    """,

    "Fat > 20g count": """
        SELECT COUNT(*) as high_fat_count
        FROM nutrient_info
        WHERE fat_value > 20
    """,

    "Average carbs per product": """
        SELECT product_code, AVG(carbohydrates_value) as avg_carb
        FROM nutrient_info
        GROUP BY product_code
    """,

    "Sodium > 1g": """
        SELECT *
        FROM nutrient_info
        WHERE sodium_value > 1
    """,

    "Non-zero fruits content": """
        SELECT COUNT(*) as fruits_count
        FROM nutrient_info
        WHERE fruits_veg_nuts_100g > 0
    """,

    "Calories > 500": """
        SELECT *
        FROM nutrient_info
        WHERE energy_kcal_value > 500
    """
}

derived_queries = {
    "Count per calorie category": """
        SELECT calorie_category, COUNT(*) as count
        FROM derived_metrics
        GROUP BY calorie_category
    """,

    "High Sugar count": """
        SELECT COUNT(*) as high_sugar
        FROM derived_metrics
        WHERE sugar_category = 'High Sugar'
    """,

    "Avg ratio for High Calorie": """
        SELECT AVG(sugar_to_carb_ratio) as avg_ratio
        FROM derived_metrics
        WHERE calorie_category = 'High Calorie'
    """,

    "High Calorie & High Sugar": """
        SELECT *
        FROM derived_metrics
        WHERE calorie_category = 'High Calorie'
        AND sugar_category = 'High Sugar'
    """,

    "Ultra processed count": """
        SELECT COUNT(*) as ultra_processed
        FROM derived_metrics
        WHERE is_ultra_processed = 'Yes'
    """,

    "Ratio > 0.7": """
        SELECT *
        FROM derived_metrics
        WHERE sugar_to_carb_ratio > 0.7
    """,

    "Avg ratio per calorie category": """
        SELECT calorie_category, AVG(sugar_to_carb_ratio) as avg_ratio
        FROM derived_metrics
        GROUP BY calorie_category
    """
}

join_queries = {
    "Top 5 brands with High Calorie": """
        SELECT p.brand, COUNT(*) as count
        FROM product_info p
        JOIN derived_metrics d ON p.product_code = d.product_code
        WHERE d.calorie_category = 'High Calorie'
        GROUP BY p.brand
        ORDER BY count DESC
        LIMIT 5
    """,

    "Average calories per category": """
        SELECT d.calorie_category, AVG(n.energy_kcal_value) as avg_cal
        FROM derived_metrics d
        JOIN nutrient_info n ON d.product_code = n.product_code
        GROUP BY d.calorie_category
    """,

    "Ultra processed per brand": """
        SELECT p.brand, COUNT(*) as count
        FROM product_info p
        JOIN derived_metrics d ON p.product_code = d.product_code
        WHERE d.is_ultra_processed = 'Yes'
        GROUP BY p.brand
    """
}