# Slack Bot Lannister

This system allows workers to create requests to get different bonuses (referral, overtime, etc.). 
All requests should be reviewed by the leads, managers, or the head of company. 

The main goal of this system, make the process of getting bonuses easy and tracked.


Frontend coverage  
[![Coverage Status](https://coveralls.io/repos/github/COXIT-CO/lannister_bot/badge.svg)](https://coveralls.io/github/COXIT-CO/lannister_bot)

Backend coverage
< insert badge here >

# Firing up project:
With docker-compose:

- As simple as ```docker-compose up --build```

With poetry:

```
   poetry env use python3.10
   poetry shell
   cd backend/ & python3 manage.py runserver 8001
   cd ../frontend & python3 manage.py runserver
```

With PIP:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd backend/ & python3 manage.py runserver 8001
cd ../frontend & python3 manage.py runserver
```
# Usage 
To use api you need:
- 

# Architecture

Apllictions is devided into two parts: backend and frontend. Backend part is an API on DRF that provides all commands and comunicatin between clinet DB and other parts. As a client (frontend part) we have slack bot, that implements UI and sends requests to our API. 

https://app.dbdesigner.net/designer/schema/0-lannister-14e34c18-3905-4f6e-a628-e6908163826d 

https://academy-api-docs.stoplight.io/docs/api-design/


# TechStack 

- Django
- DRF
- Slack API
- Terraform
- 

# Deployment

# 