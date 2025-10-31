-- INVENTORY_ITEMS → PRODUCTS
ALTER TABLE core.inventory_items
  DROP CONSTRAINT IF EXISTS fk_inv_products;
ALTER TABLE core.inventory_items
  ADD CONSTRAINT fk_inv_products
  FOREIGN KEY (product_id)
  REFERENCES core.products(product_id)
  ON UPDATE CASCADE ON DELETE RESTRICT;

-- INVENTORY_ITEMS → DISTRIBUTION_CENTERS
ALTER TABLE core.inventory_items
  DROP CONSTRAINT IF EXISTS fk_inv_center;
ALTER TABLE core.inventory_items
  ADD CONSTRAINT fk_inv_center
  FOREIGN KEY (product_distribution_center_id)
  REFERENCES core.distribution_centers(center_id)
  ON UPDATE CASCADE ON DELETE SET NULL;

-- ORDERS → USERS
ALTER TABLE core.orders
  DROP CONSTRAINT IF EXISTS fk_orders_user;
ALTER TABLE core.orders
  ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id)
  REFERENCES core.users(user_id)
  ON UPDATE CASCADE ON DELETE RESTRICT;

-- ORDER_ITEMS → ORDERS
ALTER TABLE core.order_items
  DROP CONSTRAINT IF EXISTS fk_oi_order;
ALTER TABLE core.order_items
  ADD CONSTRAINT fk_oi_order
  FOREIGN KEY (order_id)
  REFERENCES core.orders(order_id)
  ON UPDATE CASCADE ON DELETE CASCADE;

-- ORDER_ITEMS → USERS
ALTER TABLE core.order_items
  DROP CONSTRAINT IF EXISTS fk_oi_user;
ALTER TABLE core.order_items
  ADD CONSTRAINT fk_oi_user
  FOREIGN KEY (user_id)
  REFERENCES core.users(user_id)
  ON UPDATE CASCADE ON DELETE RESTRICT;

-- ORDER_ITEMS → PRODUCTS
ALTER TABLE core.order_items
  DROP CONSTRAINT IF EXISTS fk_oi_product;
ALTER TABLE core.order_items
  ADD CONSTRAINT fk_oi_product
  FOREIGN KEY (product_id)
  REFERENCES core.products(product_id)
  ON UPDATE CASCADE ON DELETE RESTRICT;

-- ORDER_ITEMS → INVENTORY_ITEMS
ALTER TABLE core.order_items
  DROP CONSTRAINT IF EXISTS fk_oi_inventory;
ALTER TABLE core.order_items
  ADD CONSTRAINT fk_oi_inventory
  FOREIGN KEY (inventory_item_id)
  REFERENCES core.inventory_items(inventory_item_id)
  ON UPDATE CASCADE ON DELETE SET NULL;

-- EVENTS → USERS (nullable)
ALTER TABLE core.events
  DROP CONSTRAINT IF EXISTS fk_events_user;
ALTER TABLE core.events
  ADD CONSTRAINT fk_events_user
  FOREIGN KEY (user_id)
  REFERENCES core.users(user_id)
  ON UPDATE CASCADE ON DELETE SET NULL;