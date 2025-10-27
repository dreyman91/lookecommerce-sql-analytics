-- Script to run
-- Get-Content sql/01_schema/01_create_database.sql | docker exec -i lookecommerce-sql-analytics-db-1 psql -U ecom_analyst -d postgres
-- Get-Content sql/01_schema/02_create_schemas.sql  | docker exec -i lookecommerce-sql-analytics-db-1 psql -U ecom_analyst -d lookecommerce
-- Get-Content sql/01_schema/03_create_tables.sql   | docker exec -i lookecommerce-sql-analytics-db-1 psql -U ecom_analyst -d lookecommerce
-- Get-Content sql/01_schema/04_constraints.sql     | docker exec -i lookecommerce-sql-analytics-db-1 psql -U ecom_analyst -d lookecommerce
-- Get-Content sql/01_schema/05_indexes.sql         | docker exec -i lookecommerce-sql-analytics-db-1 psql -U ecom_analyst -d lookecommerce

\set ON_ERROR_STOP on
\cd /app

\i sql/01_schema/00_settings.sql
\i sql/01_schema/01_create_database.sql
\c lookecommerce
\i sql/01_schema/02_create_schemas.sql
\i sql/01_schema/03_create_tables.sql
\i sql/01_schema/04_constraints.sql
\i sql/01_schema/05_indexes.sql
\i sql/01_schema/90_sanity_checks.sql