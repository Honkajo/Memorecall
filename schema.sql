CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE decks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY, 
    deck_id INTEGER NOT NULL, 
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (deck_id) REFERENCES deck (id)
);
