-- tables exist?
\dt core.*

-- fk overview
select
  tc.table_schema, tc.table_name, kcu.column_name, ccu.table_name as references_table
from information_schema.table_constraints tc
join information_schema.key_column_usage kcu
  on tc.constraint_name = kcu.constraint_name and tc.table_schema = kcu.table_schema
join information_schema.constraint_column_usage ccu
  on ccu.constraint_name = tc.constraint_name and ccu.table_schema = tc.table_schema
where tc.constraint_type = 'foreign key'
  and tc.table_schema = 'core'
order by tc.table_name, kcu.column_name;

-- index overview
select schemaname, tablename, indexname, indexdef
from pg_indexes
where schemaname = 'core'
order by tablename, indexname;