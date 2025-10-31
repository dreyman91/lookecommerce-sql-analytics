"""
===================
ETL PIPELINE - Load Cleaned Data to PsSQL
===================
This Script:
1. Establishes DB connection using environment variables
2. Loads CSV files in dependenncy  order (respecting foreign keys)
3. Uses batch inserts for performance
4. Validates row counts after each load
5. Provides detailed logging and error handling

Database Connection:
- Host: localhost
- Port: 5433
- Database: lookecommerce
- User/Password: from environment or config
"""

# ============================================
# DATABASE CONNECTION
# ============================================


import os
import sys
import psycopg2
import pandas as pd
from psycopg2 import extras, sql
from datetime import datetime


def get_connection():
    """
    Create PostgresSQL database connection
    :return:
        connection object if successful, None otherwise
    """
    try:
        DB_CONFIG = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5433')),
            'database': os.getenv('DB_DATABASE', 'lookecommerce'),
            'user': os.getenv('DB_USER', 'ecom_analyst'),
            'password': os.getenv('DB_PASSWORD', 'SecurePass2024!'),
            'options': '-c search_path=core,public'
        }
        print(
            f"Connecting to PostgresSQL database :{DB_CONFIG['database']} on {DB_CONFIG['host']}...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SET search_path TO core, public;")
        conn.commit()

        print("✅ Database connection established (using schema: core)")
        return conn
    except Exception as e:
        print(f'Failed to connect to PostgresSQL database: {e}')
        return None


# ============================================
# TABLE OPERATIONS
# ============================================

def truncate_table(conn, table_name):
    """
    Truncate table before loading data
    """

    try:
        cursor = conn.cursor()
        cursor.execute(f'TRUNCATE TABLE {table_name} CASCADE ;')
        conn.commit()
        print(f'Truncated table {table_name}')
    except Exception as e:
        print(f'Failed to truncate table {table_name}: {e}')
        conn.rollback()


def get_row_count(conn, table_name):
    """
    Get current row count in table
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {table_name} ;')
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"Error counting rows in {table_name}: {e}")
        return 0


def load_csv_to_table(conn, csv_path, table_name, column_mapping=None, schema='core'):
    """
    Load CSV file into database table using efficient batch insert

    Process:
    1. Read CSV file into Pandas Dataframe
    2. MAP CSV columns to database columns
    3. Convert Dataframe to list of tuples
    4. Execute batch INSERT
    5. Commit transaction
    6. Verify row count
    :param schema:
    :param conn:
    :param csv_path:
    :param table_name:
    :param column_mapping:
    :return: number of rows loaded, or 0 if error.
    """

    print(f"\n Loading : {schema}.{table_name}")
    print(f"\n Source: {csv_path}")

    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"\n File does not exist in {csv_path} ")
        return 0

    try:
        df = pd.read_csv(csv_path)
        print(f"\n   Rows in CSV: {len(df):,}")

        if column_mapping is not None:
            df = df.rename(columns=column_mapping)

        integer_columns = ['id', 'user_id', 'sequence_number']  # Adjust for your table

        for col in integer_columns:
            if col in df.columns:
                # Convert float64 → Int64 (nullable integer)
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

        # Convert NaN to None for PostgreSQL NULL
        df = df.astype(object).where(pd.notna(df), None)

        # Get column names and create placeholders
        columns = list(df.columns)
        columns_str = ','.join(columns)
        placeholders = ','.join(['%s'] * len(columns))

        # Create INSERT statement
        insert_query = f"""
            INSERT INTO {schema}.{table_name} ({columns_str})
            VALUES ({placeholders})
        """

        # Convert dataframe to list of tuples
        data = [tuple(x) for x in df.values]

        # In load_data.py, line 145 (BEFORE execute_batch call):

        # Print first row being inserted
        print("\n🔍 Debugging - First row values:")
        data_sample = data[0]  # Assuming 'data' is your list of tuples/lists
        for i, val in enumerate(data_sample):
            col_name = df.columns[i] if i < len(df.columns) else f"col_{i}"
            print(f"  {col_name}: {val} (type: {type(val).__name__})")

        # Check if ANY value exceeds bigint limits
        BIGINT_MAX = 9223372036854775807
        for row_idx, row in enumerate(data):
            for col_idx, val in enumerate(row):
                if isinstance(val, (int, float)) and (val > BIGINT_MAX or val < -BIGINT_MAX):
                    col_name = df.columns[col_idx] if col_idx < len(df.columns) else f"col_{col_idx}"
                    print(f"❌ Row {row_idx}, Column '{col_name}': {val} EXCEEDS BIGINT_MAX!")

        # Execute batch insert for performance
        cursor = conn.cursor()
        extras.execute_batch(
            cursor,
            insert_query,
            data,
            page_size=1000
        )
        conn.commit()

        # Verify insertion
        row_count = get_row_count(conn, table_name, )
        print(f"\n   Successfully loaded {row_count:,} rows into {table_name}")

        return row_count
    except Exception as e:
        print(f"   Error loading {table_name}: {e}")
        print(f"  Error Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return 0


# ============================================
# VALIDATION
# ============================================

def validate_referential_integrity(conn, schema='core'):
    """
    Validate foreign key relationships after loading all data

    Checks:
    - Orders reference valid users
    - Order items reference valid orders and products
    - Inventory items reference valid products

    Returns:
        True if all checks pass, False otherwise
    """
    print(f"\n Validating referential integrity...")

    validation_queries = {
        'Orders without users': """
            SELECT COUNT(*) FROM core.orders o 
            LEFT JOIN core.users u ON o.user_id = u.user_id
            WHERE u.user_id IS NULL;
        """,
        'Order Items without orders': """
            SELECT COUNT(*) FROM core.order_items oi
            LEFT JOIN core.orders o ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """,
        'Order items without products': """
            SELECT COUNT(*) FROM core.order_items oi
            LEFT JOIN core.products p 
                ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL;
        """,
        'Order items without users': """
          SELECT COUNT(*) FROM core.order_items oi
            LEFT JOIN core.users u 
                ON oi.user_id = u.user_id
            WHERE u.user_id IS NULL;
        """,
        'Inventory items without products': """
            SELECT COUNT(*) FROM core.inventory_items ii
            LEFT JOIN core.products p 
                ON ii.product_id = p.product_id
            WHERE p.product_id IS NULL;
        """
    }

    all_passed = True
    cursor = conn.cursor()

    for check_name, query in validation_queries.items():
        try:
            cursor.execute(query)
            count = cursor.fetchone()[0]

            if count == 0:
                print(f"\n  {check_name}: PASS")
            else:
                print(f"\n  {check_name}: FAIL ({count} orphaned records")
                all_passed = False

        except Exception as e:
            print(f"\n  Error checking {check_name}: {e}")
            all_passed = False
    return all_passed


# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Main ETl pipeline  execution
    
    Load order (respects foreign key dependencies)
    1. distribution_centers (none) 
    2. users (none)
    3. products (none)
    4. inventory_items (depends on products, distribution_centers)
    5. orders (depends on users)
    6. order_items (depends on orders, users, products, inventory_items)
    7, events  (depends on users)
    :return:
    """

    print("=" * 70)
    print("ETL PIPELINE - THE LOOK E-COMMERCE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)

    # Connect to database
    conn = get_connection()
    if not conn:
        print("Failed to connect to PostgresSQL database. Exiting...")
        sys.exit(1)

    # Define load sequence
    load_sequence = [
        {
            'csv': 'data/processed/distribution_centers_cleaned.csv',
            'table': 'distribution_centers',
            'mapping': {
                'id': 'center_id'
            }
        },
        {
            'csv': 'data/processed/users_cleaned.csv',
            'table': 'users',
            'mapping': {
                'id': 'user_id'
            }
        },
        {
            'csv': 'data/processed/products_cleaned.csv',
            'table': 'products',
            'mapping': {
                'id': 'product_id'
            }
        },
        {
            'csv': 'data/processed/inventory_items_cleaned.csv',
            'table': 'inventory_items',
            'mapping': {
                'id': 'inventory_item_id'
            }
        },
        {
            'csv': 'data/processed/orders_cleaned.csv',
            'table': 'orders',
            'mapping': None
        },
        {
            'csv': 'data/processed/order_items_cleaned.csv',
            'table': 'order_items',
            'mapping': {
                'id': 'order_item_id'
            }
        },
        {
            'csv': 'data/processed/events_cleaned.csv',
            'table': 'events',
            'mapping': {
                'id': 'event_id'
            }
        }
    ]

    """
        print("\n  TRUNCATING TABLES (all existing data will be deleted)...")
        for item in reversed(load_sequence):  # Reverse order to respect FK constraints
            truncate_table(conn, item['table'])
        """

    # Load each table
    total_rows_loaded = 0
    load_summary = []

    for item in load_sequence:
        rows_loaded = load_csv_to_table(
            conn,
            item['csv'],
            item['table'],
            item['mapping']
        )
        total_rows_loaded += rows_loaded

        load_summary.append({
            'table': item['table'],
            'rows_loaded': rows_loaded
        })

    # Validate referential integrity
    integrity_passed = validate_referential_integrity(conn)

    # Close connection
    conn.close()

    # Final Summary
    print("\n" + "=" * 70)
    print("ETL PIPELINE COMPLETE")
    print("=" * 70)

    print("\n LOAD SUMMARY:")
    for item in load_summary:
        print(f"{item['table']:20s}: {item['rows_loaded']:,} rows")

    print(f"\n   {'TOTAL':20s}: {total_rows_loaded:,} rows")

    print("\n   DATA INTEGRITY:")
    if integrity_passed:
        print("   All referential integrity checks passed")
    else:
        print("   Some referential integrity checks failed")
        print("   review validation output")

    print("=" * 70)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Exit code
    if integrity_passed:
        print("\n   ETL PIPELINE COMPLETE SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n   ETL PIPELINE COMPLETE SUCCESSFULLY WITH WARNINGS!")
        sys.exit(1)


if __name__ == "__main__":
    main()
