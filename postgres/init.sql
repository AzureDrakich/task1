CREATE TABLE IF NOT EXISTS person
(
    id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(30),
    password CHARACTER VARYING(30)
);
CREATE TABLE IF NOT EXISTS article
(
    id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(30),
    article CHARACTER VARYING(30),
    date CHARACTER VARYING(30),
    person_id INTEGER
);