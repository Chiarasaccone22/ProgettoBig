DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    titolo TEXT,
    info TEXT
);

INSERT INTO posts(titolo, info) VALUES ('Lava il gatto', 'Lucidare accuratamente il pelo');
INSERT INTO posts(titolo, info) VALUES ('mangia il cane', 'Lucidare accuratamente il peloooooooooooo');
INSERT INTO posts(titolo, info) VALUES ('vulcano', 'scappa');
INSERT INTO posts(titolo, info) VALUES ('mucca', 'dai da mangiare');

SELECT * FROM posts;