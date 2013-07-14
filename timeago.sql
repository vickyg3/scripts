/*

Licensed under WTFPL: http://www.wtfpl.net/about/

A postgres function that will return a twitter like string for a given
timestamp "2 weeks ago", "2 seconds ago etc.

*/

CREATE OR REPLACE FUNCTION time_ago (ts timestamptz) RETURNS TEXT AS $$
    DECLARE
        diff INTERVAL;
        dif INT;
        method TEXT;
        cnt INT;
        plural TEXT;
    BEGIN 
        diff := current_timestamp - ts;
        dif := EXTRACT(EPOCH FROM diff)::INT;
        IF dif < 60 THEN
            method := 'Second';
            cnt := dif;
        ELSIF dif < (60 * 60) THEN
            method := 'Minute';
            cnt := floor(dif/60);
        ELSIF dif < (60 * 60 * 24) THEN
            method := 'Hour';
            cnt := floor(dif / (60 * 60));
        ELSIF dif < (60 * 60 * 24 * 7) THEN
            method := 'Day';
            cnt := floor(dif / (60 * 60 * 24));
        ELSIF dif < (60 * 60 * 24 * 365) THEN
            method := 'Week';
            cnt := floor(dif / (60 * 60 * 24 * 7));
        ELSE
            method := 'Year';
            cnt := floor(dif / (60 * 60 * 24 * 365));
        END IF;

        IF cnt > 1 THEN
            plural := 's';
        ELSE
            plural := '';
        END IF;

        return CONCAT(cnt, ' ', method, plural,' Ago');
END;
$$ LANGUAGE plpgsql;