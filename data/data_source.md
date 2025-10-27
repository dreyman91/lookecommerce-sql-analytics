### Source
- **Provider:** Kaggle
- **Project:** `bigquery-public-data`
- **Dataset:** `thelook_ecommerce`
- **Access Date:** October 25, 2025
- **Access Method:** CSV downloaded from Kaggle Site

### Tables Obtained

| Table Name           | Rows   | Columns | Date Range               |
|----------------------|--------|---------|--------------------------|
| users                | 10,000 | 15      | 2019-01-02 to 2024-01-16 |
| products             | 29120  | 9       | All catalog items        |
| orders               | 125226 | 9       | 2019-01-06 to 2024-01-17 |
| order_items          | 181759 | 10      | 2019-01-06 to 2024-01-21 |
| inventory_items      | 490705 | 12      | All inventory            |
| events               | 50,000 | 13      | Last 3 Months            |
| distribution_centers | 10     | 4       | All centers              |

### Sampling Strategy
- Limited to recent date ranges for performance
- Maintained referential integrity (all orders have corresponding users)
- Events sampled from last 3 months for relevance

### Data Quality Notes
- Initial assessment pending (see Phase 3.2)
- No preprocessing applied at this stage
- Raw data preserved in `data/raw/`

### License
Public domain data provided by Kaggle for educational purposes.