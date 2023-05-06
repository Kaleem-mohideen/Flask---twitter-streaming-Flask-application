# twitter-streaming
Create a python web application with flask which will enable any user to view
their Twitter stream within the app and User can search, filter and sort tweets.
The application flow,
1. User sign in with twitter
2. Application fetches users Twitter timeline and save it to the database
3. UI will display the tweets in chronological order from DB
4. Sort & filter based on the date on DB
5. Ability to search tweets on DB
6. Tweets are synced periodically to the database on an interval (crontab is
fine).
