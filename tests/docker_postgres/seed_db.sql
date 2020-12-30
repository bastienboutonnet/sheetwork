CREATE SCHEMA sheetwork_test_schema;

CREATE TABLE sheetwork_test_schema.test (id serial PRIMARY KEY, answer integer, question varchar);

INSERT INTO sheetwork_test_schema.test VALUES
    (1, 11, 'hello hello world'),
    (2, 42, 'what is the meaning of life?')
    ;
