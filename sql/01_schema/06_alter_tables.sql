--

ALTER TABLE core.users
    ADD COLUMN IF NOT EXISTS state TEXT,
    ADD COLUMN IF NOT EXISTS street_address TEXT,
    ADD COLUMN IF NOT EXISTS city TEXT,
    ADD COLUMN IF NOT EXISTS postal_code TEXT,
    add column  if not exists latitude  numeric(10, 7) not null,
    add column  if not exists longitude numeric(10, 7) not null,
    ADD COLUMN IF NOT EXISTS phone TEXT;
