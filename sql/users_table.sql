CREATE TABLE deal_users (
    user_id SERIAL PRIMARY KEY,
    username varchar,
    email varchar,
    load_ts timestamp default null
);

insert into deal_users values (default, 'jheckman', 'jheckman324@gmail.com', default);