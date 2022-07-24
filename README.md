# Home Sweet Home Loan Calculator

## Table of Contents
* [Overview](#Overview)
* [Web App](#Web-App)
* [Pages and Features](#Pages-and-Features)
* [Up Next](#Up-Next)

## Overview
### Description
The program allows users to calculate a mortgage payment for a prospective home purchase, learn more about the true cost of their home loan, and see the effects of different home loan options. Additionally, users can view a schedule of payments and see the effect of making additional payments on their mortgage.  

## Web App
### Heroku Link
The application is hosted on Heroku. Use the following link to view the project.

https://home-loan-calculator.herokuapp.com/

* Note that Heroku puts the app to sleep after 30 minutes of inactivity. Visiting the site will load the app from sleep, which results in noticeable lag for the first visit. Subsequent visits will not require booting the app. There are ways to mitigate this, and in production, the app would be run on a higher service tier.

### Framework
The app is implemented using Python, Flask, Jinja for templating, and Bootstrap for styling. Data for the app is stored using JSON. 

## Pages and Features
### Home
The home page provides information about each of the main pages for the web application.

### Payment Calculator
Users can select information about their loan, calculate their monthly payment, and see a summary of information related to the true cost of the loan, such as total interest and total payments. Additionally, users can see an amortization schedule for the selected inputs. On the Amortization Schedule page, users have the option of going back to the calculation page to edit their loan info, as well as viewing the schedule of payments. Users can input an additional payment per month and calculate the effect paying down their mortgage has on the schedule of payments as well as on the cost of the loan. 

### Current Rates (in progress)
The page allows users to see mortgage interest rates for various types of fixed-rate home loans. The next release will utilize a microservice to update daily rates. See the Next Up section below for more details.

### FAQs
Provides basic information and answers to common questions related to mortgages and mortgage rates.

## Up Next
In the next release, a microservice will be implemented that utilizes web-scraping to update mortgage interest rates automatically (sourced from Bankrate.com). Using a microservices architecture, the application will communicate to the microservice via a message broker such as RabbitMQ. Expected release is some time in August.    
