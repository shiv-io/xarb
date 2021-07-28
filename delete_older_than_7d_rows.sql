delete from wazirx_ticker where at < current_date - interval '7 days';
delete from cb_ticker where created_at < current_date - interval '7 days';
