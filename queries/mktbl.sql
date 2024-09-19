-- DROP TABLE IF EXISTS pages;
-- CREATE TABLE IF NOT EXISTS pages(
--     slug PRIMARY KEY,
--     html TEXT,
--     ts DATETIME DEFAULT CURRENT_TIMESTAMP
-- );
-- select * from sqlite_master;

select * from pages where slug like '/deck%' limit 1;
-- delete from pages where slug like '/deck%';
