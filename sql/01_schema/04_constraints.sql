-- Foreign Keys

-- Inventory_Items -> Products, Distribution_Centers
alter table core.inventory_items
    add constraint  fk_inv_products
    foreign key (product_id) references core.products(product_id)
    on update cascade  on delete restrict;

alter table core.inventory_items
    add constraint fk_inv_center
    foreign key (product_distribution_center_id) references core.distribution_centers(center_id)
    on update cascade on delete set null;

-- orders → users

alter table core.orders
    add constraint  fk_orders_user
    foreign key (user_id) references  core.users(user_id)
    on update cascade on delete restrict;

-- order_items → orders, users, products, inventory_items

alter table core.order_items
  add constraint fk_oi_order
  foreign key (order_id) references core.orders(order_id)
  on update cascade on delete cascade;

alter table core.order_items
  add constraint fk_oi_user
  foreign key (user_id) references core.users(user_id)
  on update cascade on delete restrict;

alter table core.order_items
  add constraint fk_oi_product
  foreign key (product_id) references core.products(product_id)
  on update cascade on delete restrict;

alter table core.order_items
  add constraint fk_oi_inventory
  foreign key (inventory_item_id) references core.inventory_items(inventory_item_id)
  on update cascade on delete set null;

-- events → users (nullable)
alter table core.events
  add constraint fk_events_user
  foreign key (user_id) references core.users(user_id)
  on update cascade on delete set null;