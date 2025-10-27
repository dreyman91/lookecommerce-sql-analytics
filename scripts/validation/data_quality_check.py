"""
Data Quality Assessment Script
Performs standard profiling checks on all CSVs.
"""

import pandas as pd
import os
from datetime import datetime


def check_data_quality(file_path, table_name):
    """
    Performs profiling checks on a single table and print summary.
    """
    print(f"\n{'=' * 70}")
    print(f"QUALITY CHECK: {table_name.upper()}")
    print(f"{'=' * 70}")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist!")
        return None

    # Load data
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # Basic statistics
    print(f"BASIC STATISTICS")
    print(f"   Total Rows: {len(df):,}")
    print(f"   Total Columns: {len(df.columns):,}")
    print(f"   File Size: {os.path.getsize(file_path) / 1024:.2f} KB")

    # Column names
    print(f"\n  COLUMNS ({len(df.columns)}):,")
    for i, col in enumerate(df.columns, 1):
        print(f"   Column {i}. {col}")

    # Missing values analysis
    print(f"\n MISSING VALUES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percent': missing_pct.values
    })

    missing_issues = missing_df[missing_df['Missing_Count'] > 0]
    if len(missing_issues) > 0:
        print(missing_issues.to_string(index=False))
    else:
        print("No missing values found.")

    # Duplicate records
    print(f"\n DUPLICATE RECORDS:")
    duplicates = df.duplicated().sum()
    duplicates_pct = (duplicates / len(df) * 100).round(2)

    if duplicates > 0:
        print(f"  Duplicates Found: {duplicates:,} and {duplicates_pct:.2f}%")
    else:
        print("No duplicates found.")

    # Data types
    print(f"\n   DATA TYPES:")
    data_types = df.dtypes.value_counts()
    for data_types, count in data_types.items():
        print(f"   {data_types}: {count:,} columns")

    # Numerical columns summary
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        print(f"\n  NUMERIC COLUMNS SUMMARY:")
        print(df[numeric_cols].describe().to_string())

    # Sample Data
    print(f"\n   SAMPLE DATA (First 3 rows):")
    print(df.head(3).to_string())

    # Quality score calculation
    total_cells = len(df) * len(df.columns)
    missing_cells = missing.sum()
    quality_score = ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0

    print(f"\n  QUALITY SCORE: {quality_score:.2f}% complete. ")

    # Return Summary
    return {
        'table': table_name,
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': int(missing.sum()),
        'duplicates': int(duplicates),
        'quality_score': round(quality_score, 2)
    }


def main():
    """Main execution"""
    print(f"\n" + '=' * 70)
    print("DATA QUALITY ASSESSMENT - THE LOOK E-COMMERCE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('=' * 70)

    # Define data directory and files
    data_dir = "data/raw"
    files = {
        'users.csv': 'users',
        'products.csv': 'products',
        'orders.csv': 'orders',
        'order_items.csv': 'order_items',
        'inventory_items.csv': 'inventory_items',
        'events.csv': 'events',
        'distribution_centers.csv': 'distribution_centers'
    }

    # Run quality checks
    summary = []
    for file, table in files.items():
        file_path = os.path.join(data_dir, file)
        result = check_data_quality(file_path, table)
        if result:
            summary.append(result)

    # Overall summary
    if summary:
        print(f"\n{'=' * 70}")
        print("OVERALL SUMMARY")
        print(f"{'=' * 70}")

        summary_df = pd.DataFrame(summary)
        print(summary_df.to_string(index=False))

        # Save Summary
        os.makedirs('data', exist_ok=True)
        summary_df.to_csv('data/data_quality_summary.csv', index=False)
        print(f"\n Summary saved to: data/data_quality_summary.csv")

        # Overall assessment
        avg_quality = summary_df['quality_score'].mean()
        total_duplicates = summary_df['duplicates'].sum()

        print(f"\n{'=' * 70}")
        print("FINAL ASSESSMENT")
        print(f"{'=' * 70}")
        print(f"Average quality Score: {avg_quality:.2f}%")
        print(f"Total duplicates found: {total_duplicates:,}")

        if avg_quality >= 95 and total_duplicates < len(summary_df) * 100:
            print(f"\n Data Quality is acceptable")
        else:
            print(f"\n Data Quality is NOT acceptable. Issues detected, Cleaning recommended")
    else:
        print("\ No data files found or processed.")


if __name__ == '__main__':
    main()
