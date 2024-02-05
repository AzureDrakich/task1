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
    date date,
    person_id INTEGER,
    FOREIGN KEY (id) REFERENCES person (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments
(
    id SERIAL PRIMARY KEY,
    article_id INTEGER,
    date date,
    comment text,
    FOREIGN KEY (article_id) REFERENCES article (id) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES person (id) ON DELETE CASCADE
);