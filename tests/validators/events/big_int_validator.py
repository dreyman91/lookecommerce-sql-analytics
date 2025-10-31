"""
CSV Bigint Validator - Detects numeric values out of PostgreSQL bigint range
Standalone test script for validating processed CSV files before database insertion
"""

import csv
import pandas as pd
import pytest
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

# PostgreSQL bigint range constants
BIGINT_MIN = -9223372036854775808
BIGINT_MAX = 9223372036854775807


class BigintValidator:
    """Validator class for detecting out-of-range bigint values in CSV files"""

    def __init__(self, csv_path: str, numeric_columns: List[str] = None):
        """
        Initialize validator

        Args:
            csv_path: Path to CSV file to validate
            numeric_columns: List of column names that should be bigint.
                           If None, will auto-detect numeric columns
        """
        self.csv_path = Path(csv_path)
        self.numeric_columns = numeric_columns
        self.violations = []
        self.stats = {}

    def validate(self) -> Tuple[bool, List[Dict]]:
        """
        Main validation method

        Returns:
            Tuple of (is_valid, violations_list)
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        # Read CSV with pandas for better type inference
        try:
            df = pd.read_csv(self.csv_path, low_memory=False)
        except Exception as e:
            raise ValueError(f"Failed to read CSV: {e}")

        # Auto-detect numeric columns if not specified
        if self.numeric_columns is None:
            self.numeric_columns = self._detect_numeric_columns(df)

        # Validate each numeric column
        for col in self.numeric_columns:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in CSV")
                continue

            self._validate_column(df, col)

        # Generate statistics
        self._generate_stats(df)

        return len(self.violations) == 0, self.violations

    def _detect_numeric_columns(self, df: pd.DataFrame) -> List[str]:
        """Auto-detect columns containing numeric data"""
        numeric_cols = []

        for col in df.columns:
            # Try to convert to numeric
            try:
                pd.to_numeric(df[col], errors='coerce')
                # Check if column has any numeric-like values
                if df[col].dtype in ['int64', 'float64'] or \
                        pd.to_numeric(df[col], errors='coerce').notna().any():
                    numeric_cols.append(col)
            except:
                continue

        return numeric_cols

    def _validate_column(self, df: pd.DataFrame, col: str):
        """Validate a single column for bigint range"""
        # Convert column to numeric, coercing errors
        numeric_series = pd.to_numeric(df[col], errors='coerce')

        # Check for values outside bigint range
        for idx, value in enumerate(numeric_series):
            if pd.isna(value):
                # Check if original value was non-numeric
                original_value = df[col].iloc[idx]
                if pd.notna(original_value) and str(original_value).strip():
                    self.violations.append({
                        'row': idx + 2,  # +2 because of 0-index and header
                        'column': col,
                        'value': original_value,
                        'error_type': 'NON_NUMERIC',
                        'message': f'Non-numeric value in numeric column'
                    })
                continue

            # Check if value is within bigint range
            if value < BIGINT_MIN:
                self.violations.append({
                    'row': idx + 2,
                    'column': col,
                    'value': value,
                    'error_type': 'UNDERFLOW',
                    'message': f'Value {value} < BIGINT_MIN ({BIGINT_MIN})'
                })
            elif value > BIGINT_MAX:
                self.violations.append({
                    'row': idx + 2,
                    'column': col,
                    'value': value,
                    'error_type': 'OVERFLOW',
                    'message': f'Value {value} > BIGINT_MAX ({BIGINT_MAX})'
                })

            # Additional check for float values that might lose precision
            if isinstance(value, float) and value != int(value):
                self.violations.append({
                    'row': idx + 2,
                    'column': col,
                    'value': value,
                    'error_type': 'PRECISION_LOSS',
                    'message': f'Float value {value} will lose precision when converted to bigint'
                })

    def _generate_stats(self, df: pd.DataFrame):
        """Generate statistics about numeric columns"""
        for col in self.numeric_columns:
            if col not in df.columns:
                continue

            numeric_series = pd.to_numeric(df[col], errors='coerce')

            self.stats[col] = {
                'min': numeric_series.min(),
                'max': numeric_series.max(),
                'mean': numeric_series.mean(),
                'null_count': numeric_series.isna().sum(),
                'total_count': len(numeric_series),
                'within_bigint_range': (
                        (numeric_series >= BIGINT_MIN) &
                        (numeric_series <= BIGINT_MAX)
                ).sum()
            }

    def print_report(self):
        """Print a detailed validation report"""
        print("=" * 80)
        print("BIGINT VALIDATION REPORT")
        print("=" * 80)
        print(f"File: {self.csv_path}")
        print(f"Total Violations: {len(self.violations)}")
        print()

        if self.violations:
            print("VIOLATIONS FOUND:")
            print("-" * 80)
            for v in self.violations[:20]:  # Show first 20
                print(f"Row {v['row']} | Column: {v['column']} | "
                      f"Type: {v['error_type']}")
                print(f"  Value: {v['value']}")
                print(f"  Message: {v['message']}")
                print()

            if len(self.violations) > 20:
                print(f"... and {len(self.violations) - 20} more violations")
        else:
            print("✓ No violations found - All values within bigint range")

        print()
        print("COLUMN STATISTICS:")
        print("-" * 80)
        for col, stats in self.stats.items():
            print(f"{col}:")
            print(f"  Min: {stats['min']}")
            print(f"  Max: {stats['max']}")
            print(f"  Mean: {stats['mean']:.2f}")
            print(f"  Null Count: {stats['null_count']}")
            print(f"  Values in Range: {stats['within_bigint_range']}/{stats['total_count']}")
            print()


# Pytest test functions
def test_csv_bigint_validation():
    """Pytest test case for CSV bigint validation"""
    # Replace with your actual CSV path and columns
    csv_path = "data/processed/events_cleaned.csv"  # Always change to the CSV that needs to be checked
    numeric_columns = ['id', 'user_id', 'sequence_number'] # Specify your columns / Auto Detect columns

    validator = BigintValidator(csv_path, numeric_columns)
    is_valid, violations = validator.validate()

    # Print report for debugging
    validator.print_report()

    # Assert no violations
    assert is_valid, f"Found {len(violations)} bigint violations in CSV"


def test_specific_columns_bigint_range():
    """Test specific columns individually"""
    csv_path = "data/processed/events_cleaned.csv"

    df = pd.read_csv(csv_path)

    # Test each column that should be bigint
    columns_to_test = ['id', 'user_id', 'sequence_number']

    for col in columns_to_test:
        if col in df.columns:
            numeric_series = pd.to_numeric(df[col], errors='coerce')

            # Check min value
            min_val = numeric_series.min()
            assert min_val >= BIGINT_MIN, \
                f"Column {col}: min value {min_val} below BIGINT_MIN"

            # Check max value
            max_val = numeric_series.max()
            assert max_val <= BIGINT_MAX, \
                f"Column {col}: max value {max_val} above BIGINT_MAX"


def test_no_non_numeric_values():
    """Test that numeric columns don't contain non-numeric values"""
    csv_path = "data/processed/events_cleaned.csv"
    numeric_columns = ['id', 'user_id', 'sequence_number']

    df = pd.read_csv(csv_path)

    for col in numeric_columns:
        if col in df.columns:
            # Try to convert to numeric
            numeric_series = pd.to_numeric(df[col], errors='coerce')

            # Count NaN values after conversion
            nan_count = numeric_series.isna().sum()
            original_nan_count = df[col].isna().sum()

            # If more NaNs after conversion, there were non-numeric values
            assert nan_count == original_nan_count, \
                f"Column {col} contains non-numeric values"


# Standalone execution
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate CSV file for PostgreSQL bigint compatibility'
    )
    parser.add_argument('csv_file', help='Path to CSV file')
    parser.add_argument(
        '--columns',
        nargs='+',
        help='Numeric column names (auto-detect if not specified)'
    )
    parser.add_argument(
        '--fail-fast',
        action='store_true',
        help='Exit on first violation'
    )

    args = parser.parse_args()

    validator = BigintValidator(args.csv_file, args.columns)

    try:
        is_valid, violations = validator.validate()
        validator.print_report()

        # Exit with appropriate code
        sys.exit(0 if is_valid else 1)

    except Exception as e:
        print(f"Error during validation: {e}", file=sys.stderr)
        sys.exit(2)
