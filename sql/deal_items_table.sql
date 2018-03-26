CREATE TABLE deal_items (
    deal_item_id SERIAL PRIMARY KEY,
    source varchar,
    start_dt date,
    end_dt date,
    value varchar,
    item varchar,
    details varchar
);