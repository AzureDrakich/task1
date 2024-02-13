CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(30),
    password CHARACTER VARYING(32)
);
CREATE TABLE IF NOT EXISTS article
(
    id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(30),
    article CHARACTER VARYING(30),
    date date,
    user_id INTEGER,
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments
(
    id SERIAL PRIMARY KEY,
    article_id INTEGER,
    date date,
    comment text,
    FOREIGN KEY (article_id) REFERENCES article (id) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat
(
    id SERIAL PRIMARY KEY,
    usr_id INTEGER,
    sender CHARACTER VARYING(30),
    receiver CHARACTER VARYING(30),
    usr_pass CHARACTER VARYING(32),
    msg text,
    FOREIGN KEY (usr_id) REFERENCES users (id) ON DELETE CASCADE
);