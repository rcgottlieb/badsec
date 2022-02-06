# Using RESTFul APIs with Python

## Requirements
- git (version 2.32.0 (Apple Git-132) used)
- Pyhon3.9 (version 3.9.10 used on macOS 12.2)
- Docker to run the container conaining the RESTFul server (version 4.4.2 (73305) Docker Deskop used)
- An image or url to a conainer running a RESTful server
- Note: This project illustrates some native Python3 modules related to RESTFul development

## How to run this
- After you clone this repository in the terminal of your choice, run the following command:
``` $ docker run --rm -p 8888:8888 adhocteam/noclist```
- In another terminal or tab, from the project directory type:
``` $ python3 badsec.py
```
- You should expect to see output of several userid's of users from the server as a list of dictionaries as such:
```
["9757263792576857988", "7789651288773276582", "16283886502782682407", "...etc"]
```
