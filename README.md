# Memorecall

## Getting Started
To start the application:
1. Gitclone the repository to your computer: `git clone git@github.com:Honkajo/Memorecall.git
2. Install requirements: `pip install -r requirements.txt`
3. Create a file named `.env` in the root directory of the project.
4. Add the following lines to the `.env` file, replacing placeholders with your actual database URL and secret key:
    ```plaintext
    DATABASE_URL="postgresql://user:password@localhost:5432/databasename"
    SECRET_KEY="setasecretkeyhere"
    ```
5. Sign in to your PostgreSQL database.
6. Create a new database using the provided database URL.
7. Run the schema.sql commands to set up the database schema.
8. Run the app: `flask run`

## Overview
Memorecall is an app meant for students to learn more efficiently using flashcards and spaced repetition. Purpose is to use Leitner system to space cards so that the hardest cards are seen more to save time on learning.
### Current Features
- User can login into their account
- User can register their username and password
- User can create decks and add cards to the decks
- User can see the listing of the decks in the inventory
- User can learn cards from their decks

### Future Enhancements
- User can reset learning phases for the deck to start over
- When cards get to level 6 they do not show in the learning phases anymore
- Users can delete cards and deck from their inventory

### Usage problems
If schema.sql file does not correctly create all the tables, create them manually by using '''plaintext psql ''' command and '''plaintext psql your_database_name < schema.sql '''
