-- users
create index if not exists idx_users_email         on core.users(email);
create index if not exists idx_users_country       on core.users(country);
create index if not exists idx_users_created_at    on core.users(created_at);

-- products
create index if not exists idx_products_category   on core.products(category);
create index if not exists idx_products_brand      on core.products(brand);
create index if not exists idx_products_department on core.products(department);

-- orders
create index if not exists idx_orders_user_id      on core.orders(user_id);
create index if not exists idx_orders_status       on core.orders(status);
create index if not exists idx_orders_created_at   on core.orders(created_at);

-- order_items
create index if not exists idx_oi_order_id         on core.order_items(order_id);
create index if not exists idx_oi_product_id       on core.order_items(product_id);
create index if not exists idx_oi_created_at       on core.order_items(created_at);
create index if not exists idx_oi_created_product  on core.order_items(created_at, product_id);

-- events
create index if not exists idx_events_user_id      on core.events(user_id);
create index if not exists idx_events_session_id   on core.events(session_id);
create index if not exists idx_events_created_at   on core.events(created_at);
create index if not exists idx_events_event_type   on core.events(event_type);