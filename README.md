# Sign Language Recognition Website

## Description
With the current technology, sign language recognition services can already achieve a certain level of accuracy. Nevertheless, most of such services rely on the computing resources of the user's computer for identification. Therefore, I combined the computer vision service of Azure with the Azure App Service and moved all the required computing resources to the cloud so that users can use the sign language recognition service anytime, anywhere.

## Programming Languages
- Frontend: HTML + JavaScript
- Backend: Python + C#


## Prerequisites
- Flask: For the web framework
- Socket.IO: To enable well communication between a client and a server.
- Azure Resources
    - Azure App Service
    - Custom Vision

## Service Architecture

## Demo

```
To test the project on localhost:

1. git clone https://github.com/jonathan-liu-0204/Sign_Language_Recognition.git
2. cd "directory of the cloned repository"
3. python3 -m venv .venv
4. source ./bin/activate
5. pip3 install -r requirements.txt
6. python3 app.py
7. Paste the generated url in your browser and start the website.
8. deactivate (to exit the virtual enviornment)
```

Following screenshot is what you should get after running the website:
![GITHUB](https://imgur.com/YD4KJWE "Screenshot of the Sign Recognition Website")

## Reference

