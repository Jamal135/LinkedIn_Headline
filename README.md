# LinkedIn Headline Automatic Updater

***
# About:
---
If you use this, LinkedIn may decide you are a bot and permanently ban your account. So... it is worth the risk to network in a new a cool way! This repository is just a modification of my Instagram Bio Updater to update my LinkedIn headline.

Currently the headline is updated with some cool text from the function below. Really you could make this put just about anything in your headline by modifying this function below to return a different string. The code will test every minute or so if new text doesn't match current text, if this evaluates as true it will update your headline. 

```python
def build_text():
    ''' Returns: Built LinkedIn headline string. '''
    current_time = datetime.now(pytz.timezone('Australia/Queensland'))
    hour = current_time.strftime("%I %p").replace(" ", "").lower().lstrip('0')
    day = calendar.day_name[current_time.weekday()]
    return f"Feels like {hour} on a {day} to me..."
```
Hey if you found this repository... you should do something cool with this!

Creation Date: 30/10/2022

***
# Setup:
---
Regardless of if you are running this code on a server or just for fun on your PC for a bit, first you need to create a env file in the project directory. If you fork this repository, don't commit this env file unless you want others to know your LinkedIn login.

```
USER=your username
PASS=your password
URL=your LinkedIn profile URL
```
If you aren't putting this on a server, then just run the Python file with the requirements installed and you will see the automated browser pop up and hopefully work! If you are putting this on a server, it is probably better to use Docker. In order to have this work within a Docker container first SSH into your server. From here you only need to type the following commands:

```
1: git pull https://github.com/Jamal135/LinkedIn_Headline       # Download the repository.
2: cd LinkedIn_Headline                                         # Enter the right directory.
# Create your .env file!
3: docker-compose up -d                                         # Start the program.
```

The up command makes the code start (building a container if none already exists) and the -d argument detaches it from the terminal. Here are some other useful commands that may help as well!

```
docker-compose down                                         # Kill the container gracefully.
docker-compose build                                        # Rebuild container if you make changes.   
docker ps -a                                                # See Docker stuff.
docker logs --follow linkedin_headline_linkedin_headline_1  # Follow code logs (^C to exit).
```

If the code is breaking through Docker, you can uncomment the port in the docker-compose.yml file. Then build and put the container up, navigate to that port in a browser (ip:4444), click sessions, and click the camera icon to see what is happening. WARNING: This is not behind authentication, anyone who goes to this port can fully control your LinkedIn account through the Selenium session. So make sure to comment this out again after testing and kill the Docker container used for testing.

Do note, you may also need to tell LinkedIn your new login is not suspicious before everything works.

***
# Future:
---
I have no idea when this code might be permanently broken by LinkedIn changes... just kidding LinkedIn never gets updated. None the less I will work to fix bugs and make small improvements as I see fit.

***
# License:
---
MIT License.
