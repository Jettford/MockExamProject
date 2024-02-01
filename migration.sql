CREATE TABLE users (
    user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username char(24) NOT NULL,
    password char(64) NOT NULL,
    admin BOOLEAN NOT NULL
);

CREATE TABLE articles(
    article_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title char(64) NOT NULL,
    search_keys TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE advice_triggers(
    trigger_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    lhs char(64) NOT NULL,
    rhs char(64) NOT NULL,
    logic char(3) NOT NULL,
    article_id INT NOT NULL,
    FOREIGN KEY (article_id) REFERENCES articles(article_id)
);