import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv(r"C:\Vasu\Guvi\Choco Crunch Analysis\openfood_chocolates_cleaned.csv")

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

## Insert into product_info
product_data = list(
    df[["product_code", "product_name", "brand"]]
    .itertuples(index=False, name=None)
)

cursor.executemany("""
    INSERT INTO product_info (product_code, product_name, brand)
    VALUES (%s, %s, %s)
""", product_data)

conn.commit()

## Insert into nutrient_info

nutrient_data = list(
    df[[
        "product_code",
        "energy-kcal_value",
        "energy-kj_value",
        "carbohydrates_value",
        "sugars_value",
        "fat_value",
        "saturated-fat_value",
        "proteins_value",
        "fiber_value",
        "salt_value",
        "sodium_value",
        "fruits-vegetables-nuts-estimate-from-ingredients_100g",
        "nutrition-score-fr",
        "nova-group"
    ]].itertuples(index=False, name=None)
)

cursor.executemany("""
    INSERT INTO nutrient_info (
        product_code,
        energy_kcal_value,
        energy_kj_value,
        carbohydrates_value,
        sugars_value,
        fat_value,
        saturated_fat_value,
        proteins_value,
        fiber_value,
        salt_value,
        sodium_value,
        fruits_veg_nuts_100g,
        nutrition_score_fr,
        nova_group
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", nutrient_data)

conn.commit()

## Insert into derived_metrics

derived_data = list(
    df[[
        "product_code",
        "sugar_to_carb_ratio",
        "calorie_category",
        "sugar_category",
        "is_ultra_processed"
    ]].itertuples(index=False, name=None)
)

cursor.executemany("""
    INSERT INTO derived_metrics (
        product_code,
        sugar_to_carb_ratio,
        calorie_category,
        sugar_category,
        is_ultra_processed
    )
    VALUES (%s, %s, %s, %s, %s)
""", derived_data)

conn.commit()

