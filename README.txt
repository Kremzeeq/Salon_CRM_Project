<h1 align="center">
  <img src="src/static/img/salon_crm_app.jpg" alt="Salon CRM Logo" />
</h1>

This **Salon CRM** app is a appointment booking platform, structured as a Django and REST API application.
This application explores using Django admin features and SQLite engine to create a fully functional application which 
could be used by an independent hairdresser. 

- This prototype allows the user to firstly set up their various services in the system 
	- e.g. a "Cut and Blowdry", how much it costs and how long it takes. 
- Customers can be added in the system with personal details, prior to scheduling an appointment
- Booking an appointment allows the user to select multiple services requested
- Once this in confirmed, a quote can be provided to the customer
- An appointment summary report provides a breakdown on number of appointments, income and free timeslots per day.

 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


<h2 align="center">
  <img src="src/static/img/salon_crm_wordcloud.png" alt="Salon CRM Wordcloud" />
</h2>


 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Salon CRM Project Set-Up**

- Module pre-requisites are in requirements.txt
- Opening the project in PyCharm should prompt for modules from the requirements.txt to be installed
- Alternatively, use "python -m pip install -r requirements.txt" in the command line in the same directory as the requirements.txt file.
- Should there be trouble upgrading pip in the venv (e.g. to ver. 19.03.3) try:
	python -m pip install -U --force-reinstall pip

## Perform migrations

- Migrating django models is neccessary prior to accessing the CRM system in the browser(src\salon_crm_project\salon_crm_base hyperlink)
- This enables initial tables in a SQLite database are created e.g. for auth_user and user defined models: Customer, Appointment and Service Service and 
- In the terminal, under src/salon_crm_project where the django manage.py file is based, type:
	- python manage.py makemigrations
	- python manage.py migrate

<h2 align="center">
  <img src="src/static/img/first_migration.png" alt="First migration using django" />
</h2>

- Now initial tables have been created admin login credentials can be set up with the following:
	- python manage.py createsuperuser
- Simply follow steps for setting up your credentials

## Accessing the Salon CRM system in the browser

- Type the following:
	- python manage.py runserver
	

## Changes required in Python Code

src\models\users\user_constants.py

| Location                                          | Guidance                                                                                       |
|:--------------------------------------------------|:-----------------------------------------------------------------------------------------------|
| src/config.py                                     | Substitute ADMINS frozenset email with a preferred email                                       |
| src/run.py                                        | Type a port number as per preferences                                                          |
| src/models/users/user_constants.py                | Substitute variables for URL, AUTH_URL, API_KEY, FROM which can be obtained via Mailgun        |
|                                                   | Mailgun Link: https://www.mailgun.com/                                                         |
| src/common.database.py                            | uri for Database is defaulted to "mongodb://127.0.0.1:27017" for your local machine            |
|                                                   | This can be changed according to your preferences                                              |
| src/init_DB_collection_presets.py                 | Substitute "youremail@youremail.com" with a preferred email you have access to                 |
|                                                   | NB. This will be authenticated. Please see **Email Authenication** for setting up a password   |
|:--------------------------------------------------|:-----------------------------------------------------------------------------------------------|

## MongoDB Set-Up

- Mongo DB Community Edition 4.0 was installed for this project
- Manual for installing MongoDB on Linux, macOS and Windows is available here:

https://docs.mongodb.com/manual/administration/install-community/

## Initiating Sample data in MongoDB

- Once MongoDB has been configured to preferences, ensure **mongod**, the MongoDB daemon, has been typed into the command line. 
- Python script in the following location can be run:

src\init_DB_collection_presets.py

- This will populate the MongoDB MediaBudgie database with data for the user, currency, country and product collections.
- These collections are prerequisites required for running the MediaBudgie app.py file
- Please note the preset file can be changed according to preferences
- e.g. at the moment the presets only place focus on European countries

## Email Authenication

- Once a preferred email has been set up in the MongoDB database, run the following python script:

src\send_authentication_email.py

- This will prompt for an authentication email to be sent to the email account with an authenication code.
- This will direct the user to an authenication page where the code may be entered
- Thereafter, a password may be set on the registration page
- Logging into the website will redirect to the **Annual Budgeting Portal**
- Please ensure the app.py file is running so the URI can be accessed

**Demo**

MediaBudgieDemo.pptx in GitHub provides a prototype of the application and similuates a business user journey for setting up central budgets
-Please view business user journey for the Media Budgie Application here:


