# Python-RESTful-API
Developing RESTful APIs using Python Flask Framework and MySQL Database for Passport Requests System

## Envirement settings:
With the following command line : ``pip install -r requirements.txt``

## Setting up MySQL DataBase:
### 1. Install [XAMPP](https://www.apachefriends.org/download.html)
### 2. Start Apache & MySQL Servers
### 3. Import ``DataBase.sql``

## Setting up SMS API using Twilio:
### 1. Create [Twilio Account](https://www.twilio.com)
### 2. Copy and past your **account sid**, **auth_token**, **twilio_number** into ``keys.py``

## System Design:
This is a RESTful application, using 3 REST APIs:
- ``CivilState``: Returns Whether the entered Informations are True or False
- ``CriminalRecord``: Returns the criminal record of the person (Good/Bad)
- ``SafetyState``: Returns the Safety state of the person (Wanted/Unwanted)

> ``server.py`` Flask application, GET the form information and calls the 3 previous APIs to handle the passport request, and send SMS to the person using Twilio API.
