# Data Quality Assessment Report

**Project:** The Look E-Commerce Analytics  
**Date:** [27.10.2025]  
**Analyst:** [Adegun Oluwadamilare]

---

## Executive Summary

This report documents the data quality assessment performed on 7 raw CSV files from The Look E-Commerce dataset before database ingestion.

**Overall Assessment:** [NEEDS CLEANING]

---

## Quality Metrics Summary

| Table                | Rows    | Columns | Missing Values | Duplicates | Quality Score |
|----------------------|---------|---------|----------------|------------|---------------|
| users                | 100000  | 15      | 958            | 0          | 99.94%        |
| products             | 29120   | 9       | 26             | 0          | 99.99%        |
| orders               | 125226  | 9       | 237803         | 0          | 78.9%         |
| order_items          | 181759  | 11      | 344923         | 0          | 82.75%        |
| inventory_items      | 490705  | 12      | 309376         | 0          | 94.75%        |
| events               | 2431963 | 13      | 1148751        | 0          | 96.37%        |
| distribution_centers | 10      | 4       | 0              | 0          | 100%          |

**Average Quality Score:**  93.24%

---

## Detailed Findings

### Users Table
- **Issues Found:**
  - 120 missing values in 'age' column (0,96%)
- **Severity:** Low
- **Action Required:** Remove duplicates, decide on handling missing ages

### Products Table
- **Issues Found:** None
- **Status:** ✅ Ready for loading

### Orders Table
- **Issues Found:**
  - 450 missing values in 'delivered_at' (2.25% - expected for in-transit orders)
  - 12 duplicate order_ids (data quality issue)
- **Severity:** Medium
- **Action Required:** Investigate and remove duplicate order_ids

[Continue for each table...]

---

## Data Type Validation

- ✅ All date columns parseable to timestamp
- ✅ All price columns are numeric
- ✅ All ID columns are integers
- ⚠️  Some text fields contain special characters (need cleaning)

---

## Business Logic Validation

- ✅ All prices are non-negative
- ✅ Order dates are within expected range (2019-2024)
- ⚠️  Found 15 orders where `delivered_at < shipped_at` (data inconsistency)
- ⚠️  Found 8 users with age < 18 (violates business rule)

---

## Recommendations

1. **Critical Issues (Must Fix):**
   - Remove duplicate order_ids in orders table
   - Fix date inconsistencies (delivered before shipped)
   - Remove users with age < 18

2. **Medium Priority:**
   - Remove duplicate emails in users table
   - Standardize text fields (trim whitespace, proper case)

3. **Low Priority:**
   - Document expected missing values (e.g., delivered_at for pending orders)
   - Add data validation rules for future ingestion

---

## Decision

**Proceed to Phase 3.3 (Data Cleaning)?** [YES / NO]

**Justification:** Data quality score of 98.9% is acceptable, but identified issues must be addressed before loading to maintain database integrity.

---

## Next Steps

1. Create data cleaning script addressing all critical issues
2. Re-run quality assessment on cleaned data
3. Proceed to ETL pipeline if quality >= 95%
