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
  - 958 missing values in 'city' column (0,96%)
- **Severity:** Low
- **Action Required:** to be decided

### Products Table
- **Issues Found:** 
    - 2 missing values in the 'name' column
    - 24 missing values in the 'brand' column
- **Severity:** Low
- **Action Required:** to be decided

### Orders Table
- **Issues Found:**
  - 112696 missing values found in the 'returned_at' column
  - 43765 missing values found in the 'shipped_at' column
  - 81342 missing values found in the 'delivered_at' column
- **Severity:** Medium
- **Action Required:** Investigate, 'returned_at' could be missing lots of values  because items were not returned.

### Order_Items Table
- **Issues Found:**
  - 163527 missing values found in the 'returned_at' column
  - 43765 missing values found in the 'shipped_at' column
  - 117918 missing values found in the 'delivered_at' column
- **Severity:** Medium
- **Action Required:** Investigate

---
### Inventory_Items Table
- **Issues Found:**
  - 308946 missing values found in the 'sold_at' column
  - 29 missing values found in the 'product_name' column
  - 401 missing values found in the 'product_brand' column
- **Severity:** Small
- **Action Required:** Investigate

---
### Events Table
- **Issues Found:**
  - 1125671 missing values found in the 'user_id' column
  - 23080 missing values found in the 'city' column
- **Severity:** Small
- **Action Required:** Investigate

---
### Distribution_Centers Table
- **Issues Found:**
    - No Issues

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

---

## Recommendations

1. **Critical Issues (Must Fix):**
   - Investigate missing values
   - Fix date inconsistencies (delivered before shipped)
   - Remove users with age < 18

2. **Medium Priority:**
   - Standardize text fields (trim whitespace, proper case)

3. **Low Priority:**
   - Document expected missing values (e.g., delivered_at for pending orders)
   - Add data validation rules for future ingestion

---

## Decision

**Proceed to Phase 3.3 (Data Cleaning)
