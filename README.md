# Home Sweet Home Loan Calculator

## Table of Contents
* [Overview](#Overview)
* [Web App](#Web-App)
* [Pages and Features](#Pages-and-Features)
* [Microservice](#Microservice)

## Overview
### Description
The program allows users to calculate a mortgage payment for a prospective home purchase, learn more about the true cost of their home loan, and see the effects of different home loan options. Additionally, users can view a schedule of payments and see the effect of making additional payments on their mortgage.  

## Web App
### Heroku Link
The application was hosted on Heroku. RIP Heroku free tier. If I get time I plan on migrating the project. I plan on spiking a few free-tier providers to see which I like best. 

<!--- 
https://home-loan-calculator.herokuapp.com/
* Note that Heroku puts the app to sleep after 30 minutes of inactivity. Visiting the site will load the app from sleep, which results in noticeable lag for the first visit. Subsequent visits will not require booting the app. There are ways to mitigate this, and in production, the app would be run on a higher service tier.
--->

### Framework
The app is implemented using Python, Flask, Jinja for templating, and Bootstrap for styling. Data for the app is stored using JSON.
The app also features a microservices architecture which is implemented using RabbitMQ as a message broker. For puroses of deploying on Heroku, this is done using CloudAMQP(RabbitMQ as a Service). 

## Pages and Features
### Home
The home page provides information about each of the main pages for the web application.

### Payment Calculator
Users can select information about their loan, calculate their monthly payment, and see a summary of information related to the true cost of the loan, such as total interest and total payments. Additionally, users can see an amortization schedule for the selected inputs. On the Amortization Schedule page, users have the option of going back to the calculation page to edit their loan info, as well as viewing the schedule of payments. Users can input an additional payment per month and calculate the effect paying down their mortgage has on the schedule of payments as well as on the cost of the loan. 

### Current Rates
The page allows users to see mortgage interest rates for various types of fixed-rate home loans. Rates are updated daily using a microservices architecture. The microservice pulls rates from Bankrate.com using the Beautiful Soup library (i.e. web scraping). The application sends requests to the microservice via a message broker (RabbitMQ), which also returns the rate data from the microservice. 

### FAQs
Provides basic information and answers to common questions related to mortgages and mortgage rates.

## Microservice
The app utilizes a microservice to update the interest rates used in virtually all of the calculations. The microservice uses web-scraping to retrieve the average daily mortgage interest rates, which are sourced from Bankrate.com. Using a microservices architecture, the application communicates to the microservice via a message broker(RabbitMQ). For deployment on Heroku, RabbitMQ is implemented through CloudAMQP, and the Python library Pika.         
