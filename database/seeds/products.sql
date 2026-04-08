-- Gelaender product catalogue seed
-- Run once against a freshly migrated database.
-- Prices marked TBD should be updated before the shop goes live.

INSERT INTO products (sku, name, description, variant, category, price_cents, stock, is_active, image_path, weight_grams)
VALUES
  ('cap-steel-blue',  'Gelaender Cap',     'Limited first-run cap.',         'Steel Blue', 'apparel', 2600, 0, true, NULL, 200),
  ('tee-black',       'Gelaender T-Shirt', 'First-run release shirt.',        'Black',      'apparel', 3200, 0, true, NULL, 250),
  ('tee-white',       'Gelaender T-Shirt', 'First-run release shirt.',        'White',      'apparel', 3200, 0, true, NULL, 250),
  ('ep-vinyl',        'EP (Vinyl)',         'Debut EP on black vinyl. TBD.',   'Vinyl',      'music',      1, 0, false, NULL, 200),  -- price TBD, is_active false until ready
  ('ep-tape',         'EP (Cassette)',      'Debut EP on cassette tape. TBD.', 'Tape',       'music',      1, 0, false, NULL, 80)    -- price TBD, is_active false until ready
ON CONFLICT (sku) DO NOTHING;
