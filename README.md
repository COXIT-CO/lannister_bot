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
