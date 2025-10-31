"""
Data Cleaning and Transformation Script
Cleans raw CSV files and prepares them for database ingestion.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import re

EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')


def clean_users(df):
    """
    Clean users table

    Business Rules:
    - Users must be 18+ years old
    - Email must be valid format
    - No duplicate emails

    Transformations:
    - Fill missing cities with 'Unknown'
    - Standardize country names (title case)
    - Trim whitespace from text fields
    """
    print("\n Cleaning users table...")
    original_rows = len(df)

    # Remove duplicates based on emails
    df = df.drop_duplicates(subset=['email'], keep='first')

    # validate age (Business rule: must be 18+)
    df = df[df['age'] >= 18]

    # Handle missing cities
    df['city'] = df['city'].fillna('Unknown')

    # Standardize text fields
    df['first_name'] = df['first_name'].str.strip().str.title()
    df['last_name'] = df['last_name'].str.strip().str.title()
    df['country'] = df['country'].str.strip().str.title()
    df['city'] = df['city'].str.strip()

    # Validate email
    df = df[df['email'].apply(lambda x: bool(EMAIL_RE.match(str(x))) if pd.notna(x) else False)]

    # Convert timestamps
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

    # Remove rows with invalid 'created_at'
    df = df[df['created_at'].notna()]

    # Convert numeric columns to Int64 (nullable integer)
    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')

    # Convert NaN to None
    df = df.where(pd.notna(df), None)

    clean_rows = len(df)
    print(f"   Original: {original_rows:,} rows")
    print(f"   Cleaned: {clean_rows:,} rows")
    print(
        f"   Removed: {original_rows - clean_rows:,} rows "
        f"({((original_rows - clean_rows) / original_rows * 100):.2f}%)")

    return df


def clean_products(df):
    """
    Business Rules:
    - Cost must be >= 0
    - Retail price must be >= cost
    - Product name is required

    Transformations:
    - Fill missing brand with 'Generic'
    - Fill missing name with 'Unknown Product'
    - Standardize category names
    """
    print("\n Cleaning PRODUCTS table...")
    original_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates(subset=['id'], keep='first')

    # Price validation
    df = df[df['cost'] >= 0]
    df = df[df['retail_price'] >= df['cost']]

    # Handle missing data
    df['name'] = df['name'].fillna('Unknown Product')
    df['brand'] = df['brand'].fillna('Generic')
    df['category'] = df['category'].fillna('Uncategorized')

    # Standardize text fields
    df['name'] = df['name'].str.strip()
    df['brand'] = df['brand'].str.strip()
    df['category'] = df['category'].str.strip().str.title()
    df['department'] = df['department'].str.strip()

    # Convert numeric columns to Int64
    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')

    # Convert NaN to None
    df = df.where(pd.notna(df), None)

    clean_rows = len(df)
    print(f"   Original: {original_rows:,} rows")
    print(f"   Cleaned: {clean_rows:,} rows")
    print(f"   Removed: {original_rows - clean_rows:,} rows "
          f"({((original_rows - clean_rows) / original_rows * 100):.2f}%")
    return df


def clean_orders(df):
    """
    Clean orders table

    Business Rules:
    - Valid status values only
    - Date logic: created_at <= shipped_at <= delivered_at
    - Returned orders must have returned_at

    Transformations:
    - Convert all timestamp columns
    - Validate date sequences
    - Keep NULLs for pending/cancelled orders (legitimate)
    """
    print("\n   Cleaning ORDERS table...")
    original_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates(subset=['order_id'], keep='first')

    # Convert timestamps
    timestamp_cols = ['created_at', 'shipped_at', 'delivered_at', 'returned_at']
    for col in timestamp_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # validate status values
    valid_statuses = ['Completed', 'Cancelled', 'Processing', 'Shipped', 'Returned']
    df = df[df['status'].isin(valid_statuses)]

    # Business logic validation: delivered >= shipped >= created
    # Only check if values are not null

    df = df[
        (df['shipped_at'].isna()) |
        (df['created_at'].isna()) |
        (df['shipped_at'] >= df['created_at'])
        ]

    df = df[
        (df['delivered_at'].isna()) |
        (df['shipped_at'].isna()) |
        (df['delivered_at'] >= df['shipped_at'])
        ]
    # Convert numeric columns to Int64
    df['order_id'] = pd.to_numeric(df['order_id'], errors='coerce').astype('Int64')
    df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce').astype('Int64')

    clean_rows = len(df)
    print(f"   Original: {original_rows:,} rows")
    print(f"   Cleaned: {clean_rows:,} rows")
    print(f"   Removed: {original_rows - clean_rows:,} rows "
          f"({((original_rows - clean_rows) / original_rows * 100):.2f}%)")
    return df


def clean_order_items(df):
    """
    Clean order_items table

    Business Rules:
    - Sale price must be >= 0
    - Must link to valid orders and products

    Transformations:
    - Convert timestamps
    - Validate date logic
    - Keep NULLs for in-transit items (legitimate)
    """
    print("\n🧹 Cleaning ORDER_ITEMS table...")
    original_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates(subset=['id'], keep='first')

    # Price validation
    df = df[df['sale_price'] >= 0]

    # Convert timestamps
    timestamp_cols = ['created_at', 'shipped_at', 'delivered_at', 'returned_at']
    for col in timestamp_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Validate status
    valid_statuses = ['Complete', 'Cancelled', 'Processing', 'Shipped', 'Returned']
    df = df[df['status'].isin(valid_statuses)]

    # Convert numeric columns to Int64
    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
    df['order_id'] = pd.to_numeric(df['order_id'], errors='coerce').astype('Int64')
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int64')

    # Convert NaN to None
    df = df.where(pd.notna(df), None)

    clean_rows = len(df)
    print(f"   Original: {original_rows:,} rows")
    print(f"   Cleaned: {clean_rows:,} rows")
    print(
        f"   Removed: {original_rows - clean_rows:,} rows "
        f"({((original_rows - clean_rows) / original_rows * 100):.2f}%)")

    return df


def clean_inventory_items(df):
    """
    Clean inventory_items table

    Business Rules:
    - Cost must be >= 0
    - sold_at must be >= created_at if present

    Transformations:
    - Convert timestamps
    - Handle missing brand/name (inherit from products)
    - Keep NULL sold_at (unsold inventory - legitimate)
    """
    print("\n🧹 Cleaning INVENTORY_ITEMS table...")
    original_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates(subset=['id'], keep='first')

    # Price validation
    df = df[df['cost'] >= 0]
    df = df[df['product_retail_price'] >= 0]

    # Convert timestamps
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['sold_at'] = pd.to_datetime(df['sold_at'], errors='coerce')

    # Date logic: sold_at >= created_at (if sold)
    df = df[
        (df['sold_at'].isna()) |
        (df['sold_at'] >= df['created_at'])
        ]

    # Handle missing product info
    df['product_name'] = df['product_name'].fillna('Unknown Product')
    df['product_brand'] = df['product_brand'].fillna('Generic')

    # Convert numeric columns to Int64
    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int64')

    # Convert NaN to None
    df = df.where(pd.notna(df), None)

    clean_rows = len(df)
    print(f"   Original: {original_rows:,} rows")
    print(f"   Cleaned: {clean_rows:,} rows")
    print(
        f"   Removed: {original_rows - clean_rows:,} rows "
        f"({((original_rows - clean_rows) / original_rows * 100):.2f}%)")

    return df


def clean_events(df):
    """
    Clean events table

    Business Rules:
    - Event type must be valid
    - user_id can be NULL (anonymous users browsing - legitimate)

    Transformations:
    - Convert timestamps
    - Standardize event types
    - Fill missing cities
    """
    print("\n Cleaning EVENTS table...")
    original_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates(subset=['id'], keep='first')

    # Convert timestamps
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

    # Remove invalid timestamps
    df = df[df['created_at'].notna()]

    # Handle missing cities
    df['city'] = df['city'].fillna('Unknown')

    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
    df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce').astype('Int64')
    df['sequence_number'] = pd.to_numeric(df['sequence_number'], errors='coerce').astype('Int64')

    # Only replace spaces, not all empty strings (since cities might be intentionally empty after fillna)
    df = df.replace('  +', '', regex=True)
    df = df.where(pd.notna(df), None)

    # Note: user_id NULLs are legitimate (anonymous browsing)
    # Keep them for web analytics

    clean_rows = len(df)
    print(f"   Original: {original_rows:,} rows")
    print(f"   Cleaned: {clean_rows:,} rows")
    print(
        f"   Removed: {original_rows - clean_rows:,} rows "
        f"({((original_rows - clean_rows) / original_rows * 100):.2f}%)")

    return df


def clean_distribution_centers(df):
    """
    Clean distribution_centers table

    Business Rules:
    - All fields required (small reference table)

    Transformations:
    - Standardize location names
    """
    print("\n🧹 Cleaning DISTRIBUTION_CENTERS table...")
    original_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates(subset=['id'], keep='first')

    # Standardize names
    df['name'] = df['name'].str.strip()

    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')

    # Convert NaN to None
    df = df.where(pd.notna(df), None)

    clean_rows = len(df)
    print(f"   Original: {original_rows:,} rows")
    print(f"   Cleaned: {clean_rows:,} rows")
    print(f"   No cleaning needed - reference table")

    return df


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Process:
    1.  Load raw CSV files
    2. Apply cleaning functions
    3. Save cleaned files
    4. Generate cleaning report
    """

    print("=" * 70)
    print("DATA CLEANING PIPELINE - THE LOOK E-COMMERCE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Define file mappings
    files_to_clean = {
        'users.csv': clean_users,
        'products.csv': clean_products,
        'orders.csv': clean_orders,
        'order_items.csv': clean_order_items,
        'inventory_items.csv': clean_inventory_items,
        'events.csv': clean_events,
        'distribution_centers.csv': clean_distribution_centers
    }

    # Output dir
    os.makedirs('data/processed', exist_ok=True)

    # Track result
    cleaning_summary = []

    # Process each file
    for filename, cleaning_func in files_to_clean.items():
        raw_path = f"data/raw/{filename}"
        cleaned_path = f"data/processed/{filename.replace('.csv', '_cleaned.csv')}"

        # Check if file exists
        if not os.path.exists(raw_path):
            print(f"   Raw CSV file '{raw_path}' does not exist, skipping...")
            continue

        # Load raw data
        df_raw = pd.read_csv(
            raw_path,
            na_values=['', ' ', 'NULL', 'null', 'None', 'nan'],  # Treat these as NULL
            keep_default_na=True
        )
        original_rows = len(df_raw)

        # Apply cleaning
        df_clean = cleaning_func(df_raw)
        clean_rows = len(df_clean)

        # Save cleaned data
        df_clean.to_csv(
            cleaned_path,
            index=False,
            na_rep='',  # Write None as empty string in CSV
            quoting=1  # QUOTE_ALL to preserve empty cells
        )
        print(f"   Cleaned CSV file '{cleaned_path}' created...")

        # Record results
        cleaning_summary.append({
            'table': filename.replace('.csv', ''),
            'original_rows': original_rows,
            'clean_rows': clean_rows,
            'removed_rows': original_rows - clean_rows,
            'removed_percent': round((original_rows - clean_rows) / original_rows * 100, 2) if original_rows > 0 else 0
        })
    os.makedirs("data/violations", exist_ok=True)

    # Load back the cleaned files we just wrote (or keep in memory)
    users_path = "data/processed/users_cleaned.csv"
    orders_path = "data/processed/orders_cleaned.csv"
    prods_path = "data/processed/products_cleaned.csv"
    oitems_path = "data/processed/order_items_cleaned.csv"
    events_path = "data/processed/events_cleaned.csv"

    # Only run RI checks if the files exist
    if all(os.path.exists(p) for p in [users_path, orders_path]):
        users_df = pd.read_csv(users_path)
        orders_df = pd.read_csv(orders_path)

        # ---- ORDERS ↔ USERS (drop orphan orders) ----
        mask_valid_user = orders_df["user_id"].isin(users_df["id"])
        orphan_orders_df = orders_df.loc[~mask_valid_user, ["order_id", "user_id"]]
        if not orphan_orders_df.empty:
            orphan_orders_df.to_csv("data/violations/orphan_orders.csv", index=False)
            print(f"⚠️  Dropping {len(orphan_orders_df):,} orders without users "
                  f"(details: data/violations/orphan_orders.csv)")
        orders_df = orders_df.loc[mask_valid_user].copy()

        # Save the filtered orders back
        orders_df.to_csv(orders_path, index=False, na_rep='', quoting=1)

        # Update summary to reflect new count
        for row in cleaning_summary:
            if row["table"] == "orders":
                row["clean_rows_after_RI"] = len(orders_df)

    # ---- ORDER_ITEMS ↔ ORDERS & PRODUCTS (drop orphans) ----
    if all(os.path.exists(p) for p in [orders_path, prods_path, oitems_path]):
        orders_df = pd.read_csv(orders_path)
        prods_df = pd.read_csv(prods_path)
        oitems_df = pd.read_csv(oitems_path)

        # order_items referencing existing orders
        mask_order_ok = oitems_df["order_id"].isin(orders_df["order_id"])
        oi_missing_orders = oitems_df.loc[~mask_order_ok, ["id", "order_id", "product_id"]]
        if not oi_missing_orders.empty:
            oi_missing_orders.to_csv("data/violations/oi_missing_orders.csv", index=False)
            print(f"  Dropping {len(oi_missing_orders):,} order_items without parent orders "
                  f"(details: data/violations/oi_missing_orders.csv)")

        # order_items referencing existing products
        mask_product_ok = oitems_df["product_id"].isin(prods_df["id"])
        oi_missing_products = oitems_df.loc[~mask_product_ok, ["id", "order_id", "product_id"]]
        if not oi_missing_products.empty:
            oi_missing_products.to_csv("data/violations/oi_missing_products.csv", index=False)
            print(f"  Dropping {len(oi_missing_products):,} order_items without products "
                  f"(details: data/violations/oi_missing_products.csv)")

        # keep only fully valid order_items
        oitems_df = oitems_df.loc[mask_order_ok & mask_product_ok].copy()
        oitems_df.to_csv(oitems_path, index=False, na_rep='', quoting=1)

        for row in cleaning_summary:
            if row["table"] == "order_items":
                row["clean_rows_after_RI"] = len(oitems_df)

        if all(os.path.exists(p) for p in [users_path, events_path]):
            users_df = pd.read_csv(users_path)
            events_df = pd.read_csv(events_path)

            # Get valid user IDs
            valid_user_ids = set(users_df['id'].dropna().unique())

            # Keep: NULL user_id (anonymous) OR user_id in valid users
            mask_valid = events_df["user_id"].isna() | events_df["user_id"].isin(valid_user_ids)

            orphan_events_df = events_df.loc[~mask_valid, ["id", "user_id", "created_at"]]
            if not orphan_events_df.empty:
                orphan_events_df.to_csv("data/violations/orphan_events.csv", index=False)
                print(f"⚠️  Dropping {len(orphan_events_df):,} events with non-existent users")

            events_df = events_df.loc[mask_valid].copy()
            events_df.to_csv(events_path, index=False, na_rep='', quoting=1)

            for row in cleaning_summary:
                if row["table"] == "events":
                    row["clean_rows_after_RI"] = len(events_df)

    # print a tiny RI summary
    print("\n" + "-" * 70)
    print("REFERENTIAL INTEGRITY (Drop policy) - Summary")
    print("-" * 70)
    if os.path.exists("data/violations/orphan_orders.csv"):
        print("Orphan orders listed in data/violations/orphan_orders.csv")
    if os.path.exists("data/violations/oi_missing_orders.csv"):
        print("Order items missing orders: data/violations/oi_missing_orders.csv")
    if os.path.exists("data/violations/oi_missing_products.csv"):
        print("Order items missing products: data/violations/oi_missing_products.csv")
    if os.path.exists("data/violations/orphan_events.csv"):
        print("Orphan events listed in data/violations/orphan_events.csv")

    # Generate summary report
    print("=" * 70)
    print("DATA CLEANING SUMMARY")
    print("=" * 70)

    summary_df = pd.DataFrame(cleaning_summary)
    print(summary_df.to_string(index=False))

    # Save summary
    summary_df.to_csv('data/data_cleaning_summary', index=False)
    print(f"\n Cleaning Summary saved to data/data_cleaning_summary.csv")

    # statistics
    total_original = summary_df['original_rows'].sum()
    total_clean = summary_df['clean_rows'].sum()
    total_removed = summary_df['removed_rows'].sum()

    print("\n" + "=" * 70)
    print("FINAL STATISTICS")
    print("=" * 70)
    print(f"Total Original Records: {total_original:,}")
    print(f"Total Cleaned Records: {total_clean:,}")
    print(f"Total Removed Records: {total_removed:,} ({(total_removed / total_original * 100):.2f}%)")
    print(f"\n Data cleaning complete! Clean files ready in data/processed/")


if __name__ == '__main__':
    main()
