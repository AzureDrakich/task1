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
    sender_id INTEGER,
    receiver_id INTEGER,
    msg text,
    FOREIGN KEY (sender_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users (id) ON DELETE CASCADE
);