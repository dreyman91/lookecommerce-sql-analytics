import pandas as pd
import numpy as np

BIGINT_MIN = -9223372036854775808
BIGINT_MAX = 9223372036854775807


def debug_all_columns_detailed(csv_path):
    """Check EVERY column for overflow issues"""

    df = pd.read_csv(
        csv_path,
        na_values=['', ' ', 'NULL', 'null', 'None', 'nan'],
        keep_default_na=True
    )

    print("=" * 100)
    print(f"Debugging: {csv_path}")
    print("=" * 100)

    for col in df.columns:
        print(f"\n📊 Column: {col}")
        print(f"   Data type: {df[col].dtype}")
        print(f"   Unique values: {df[col].nunique()}")
        print(f"   Null count: {df[col].isna().sum():,}")

        # Try to convert to numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_vals = df[col]
        else:
            numeric_vals = pd.to_numeric(df[col], errors='coerce')

        # Get stats
        min_val = numeric_vals.min()
        max_val = numeric_vals.max()

        print(f"   Min: {min_val}")
        print(f"   Max: {max_val}")

        # Check range
        if pd.notna(min_val) and pd.notna(max_val):
            if min_val < BIGINT_MIN or max_val > BIGINT_MAX:
                print(f"   ❌ OUT OF BIGINT RANGE!")
                # Show problem rows
                problem_mask = (numeric_vals < BIGINT_MIN) | (numeric_vals > BIGINT_MAX)
                problem_rows = df[problem_mask][[col]]
                print(f"      Problem values: {problem_rows[col].unique()[:5]}")
            else:
                print(f"   ✓ Within range")


# Run it
debug_all_columns_detailed("data/processed/events_cleaned.csv")
