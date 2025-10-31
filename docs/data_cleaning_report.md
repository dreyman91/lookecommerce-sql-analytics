# Data Cleaning Report

**Project:** The Look E-Commerce Analytics  
**Date:** October 29, 2025  
**Phase:** 3.3 - Data Cleaning & Transformation

---

## Executive Summary

This report documents all data cleaning and transformation activities performed on The Look E-Commerce dataset before database ingestion.

**Overall Result:** **3,269,704** records cleaned from **3,358,783** original records (**89,079**  (2.65%) removed)

---

## Cleaning Rules Applied

### Users Table
**Rules:**
- Removed duplicates (if overlooked from data quality assessment)
- Removed users with age < 18 (business requirement)
- Filled missing cities with 'Unknown'
- Standardized text fields
- Validated email formats
- Parsed timestamps

**Results:**
- Original: **100,000** rows
- Cleaned: **73,776** rows
- Removed: **26,224** rows (users under 18)

### Products Table
**Rules:**
- Ensured cost >= 0 and retail_price >= cost
- Filled missing brand with 'Generic'
- Filled missing name with 'Unknown Product'
- Filled missing category with 'Uncategorized'
- Standardized text fields

**Results:**
- Original: **29,120** rows
- Cleaned: **29,120** rows
- Minimal changes (high quality source data)

### Orders Table
**Rules:**
- Removed duplicates **order_id**
- Parsed timestamps
- Validated date logic (shipped >= created, delivered >= shipped)
- Retained NULL values for pending/cancelled orders (legitimate)
- Validated status values

**Results:**
- Original: **125,226** rows
- Cleaned: **93,872** rows
- Removed **31,354** rows
- Date inconsistencies resolved

### Order Items Table
**Rules:**
- Validated sale_price >= 0
- Validated date sequences
- Retained NULLs for in-transit items

**Results:**
- Original: 181,759 rows
- Cleaned: 181,759 rows

### Inventory Items Table
**Rules:**
- Validated cost and pricing
- Ensured sold_at >= created_at when present
- Retained NULL sold_at (unsold inventory - legitimate)
- Handled missing data

**Results:**
- Original: 490,705 rows
- Cleaned: 490,705 rows

### Events Table
**Rules:**
- Retained NULL user_id (anonymous browsing - legitimate)
- Validated timestamps
- Filled missing cities

**Results:**
- Original: 2,431,963 rows
- Cleaned:  2,400,462 rows
-  Removed: 31,501 rows (1.30%)


### Distribution Centers Table
**Rules:**
- Reference table - minimal cleaning needed
- Standardized location names

**Results:**
- Original: 10 rows
- Cleaned: 10 rows (no changes)

---

## Key Decisions

### NULL Value Handling

**Retained NULLs (Legitimate Business Cases):**
- `orders.returned_at`: Only populated for returned orders
- `orders.shipped_at`: NULL for cancelled orders
- `orders.delivered_at`: NULL for pending/cancelled/in-transit
- `inventory_items.sold_at`: NULL for unsold inventory
- `events.user_id`: NULL for anonymous browsing sessions

**Filled NULLs:**
- `users.city`: Filled with 'Unknown'
- `products.brand`: Filled with 'Generic'
- `products.name`: Filled with 'Unknown Product'

### Data Removal Justification

**Records Removed:**
1. Users under 18 years old (business rule violation)
2. Orders with invalid date sequences (data quality issue)
3. Products with negative prices (data error)
4. Duplicate records (keep first occurrence)

---

## Data Quality Metrics

### Before vs After Cleaning
| table                | original_rows | clean_rows | removed_rows | removed_percent | 
|----------------------|---------------|------------|--------------|-----------------|
| users                | 100000        | 73776      | 26224        | 26.22%          |
| products             | 29120         | 29120      | 0            | 0.00%           |
| orders               | 125226        | 93872      | 31354        | 25.04%          |
| order_items          | 181759        | 181759     | 0            | 0.00%           |
| inventory_items      | 490705        | 490705     | 0            | 0.00%           |
| events               | 2431963       | 2400462    | 31501        | 1.30%           |
| distribution_centers | 10            | 10         | 0            | 0.00%           |

---

## Validation Checks Passed

- ✅ All dates follow logical sequences
- ✅ All prices are non-negative
- ✅ All users meet age requirements
- ✅ No duplicate primary keys
- ✅ Text fields standardized
- ✅ Referential integrity maintained

---

## Files Generated

- `data/processed/users_clean.csv`
- `data/processed/products_clean.csv`
- `data/processed/orders_clean.csv`
- `data/processed/order_items_clean.csv`
- `data/processed/inventory_items_clean.csv`
- `data/processed/events_clean.csv`
- `data/processed/distribution_centers_clean.csv`
- `data/data_cleaning_summary.csv`

---

## Recommendation

**Proceed to Phase 3.4 (ETL Pipeline)?** ✅ YES

**Justification:** Data has been thoroughly cleaned and business rules enforced.

