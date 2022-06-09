# Run50
 Running stats app built with Django.
 
## Distinctiveness and Complexity
### What is Run50?
Run50 is a web application built with Django that allows users to track their running stats.
Users can register and login to the site, and they can record their running activities by filling in the form, which can then be edited and deleted.  
Users can edit their profile, in which they can change their username and profile picture.

It provides running insights such as average pace, total distance, number of runs, as well as a graph that shows their performance over time.
It also allows users to follow other users and see their activities as well as comparing it to other people through the leaderboard.

### Why does this project satisfy the requirements?
 - The project is different from CS50W's past projects.
 - The project is built with Django.
   - It uses 3 models, namely *User*, *Activity*, and *Follower*.
 - The project uses JavaScript on its front-end.
 - The project is responsive on both web and mobile.

### What's contained in the file:
- Project files (Django) for the web application
  - /index: Index page that displays user's activities and shows activity statistics
  - /login: Login page
  - /register: Register page
  - /profile/[user_id]: Profile page of a user
  - /activity/[activity_id]: Activity page that shows details of a specific activity
  - /leaderboard: Leaderboard page that shows the top users sorted by distance
  - /feed: Displays activities from the user and the people that the user follows
  - /discover: Lists users that the user doesn't follow, and has recent activities
- `requirements.txt` that includes additional dependencies required for the project

### How to run the application:
- Run the application with the following command:
    ```bash
    python manage.py runserver
    ```
- The application will run on port 8000 and will be hosted on localhost.

