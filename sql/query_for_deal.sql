SELECT
    start_dt,
    source,
    item,
    value,
    details

FROM
    deal_items

WHERE
    end_dt > current_date
    {ITEM_DETAILS}