### Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Installation

Clone the repository:

```bash
git clone https://github.com/mdhussain7/social_network.git
cd your-repo-name
```

# Django Project with Docker and MySQL

This is a Django project containerized using Docker and integrated with MySQL as the database.

## Features

- Django web application
- MySQL database
- Docker containerization

### Application running process

Run the command docker-compose up --build -d
Start triggering the API's using Postman

if you want to run and debug it then use:
  - docker build --no-cache -t social_network_app .
  - docker run -it -p 8001:8001 -v /home/lenovo/Documents/NewProject/supermat/:/rest/social_network_app social_network_app bash   
         **specifies the local path:** /home/lenovo/Documents/NewProject/social_network_app/ 
         **specifies the image name:**  social_network_app
  - Run the manage command of the Djangoi runserver : python manage.py runserver 0:8001

### Postman Collection:
https://grey-resonance-202196.postman.co/workspace/New-Team-Workspace~15091669-be89-49c9-8e96-8e6cf6542efa/collection/30020323-70c627ce-ad5d-4b74-aa33-d50138e76f78?action=share&creator=30020323
