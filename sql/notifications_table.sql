CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id varchar,
    start_dt date default now(),
    end_dt date,
    tags varchar[],
    load_ts timestamp default now()
);

insert into notifications values
(default, 1, default, null, '{"Dove"}', default),
(default, 1, default, null, '{"Feria"}', default)