delete from wazirx_ticker where at < current_date - interval '14 days';
delete from cb_ticker where created_at < current_date - interval '14 days';
