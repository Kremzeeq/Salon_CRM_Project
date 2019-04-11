<h1 align="center">
  <img src="https://github.com/Kremzeeq/Salon_CRM_Project/blob/master/static/img/salon_crm_app.jpg" alt="Salon CRM Logo" />
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

 ---------------------------------------------------------------------------------------------------------------------------------------

**Salon CRM Project Set-Up**

- Module pre-requisites are in requirements.txt
- Opening the project in PyCharm should prompt for modules from the requirements.txt to be installed
- Alternatively, use the following command within the same directory as the requirements.txt file:
	- python -m pip install -r requirements.txt
- Should there be any problems upgrading pip in the venv (e.g. to ver. 19.03.3) try:
	- python -m pip install -U --force-reinstall pip

## Perform migrations

- Migrating django models is neccessary prior to accessing the CRM system in the browser(src\salon_crm_project\salon_crm_base hyperlink)
- This enables initial tables in a SQLite database are created e.g. for auth_user and user defined models: Customer, Appointment and Service
- In the terminal, under src/salon_crm_project where the django manage.py file is based, type:
	- python manage.py makemigrations
	- python manage.py migrate
- The first migration shoud look similar to below:

<h2 align="center">
  <img src="https://github.com/Kremzeeq/Salon_CRM_Project/blob/master/static/img/first_migration.png" alt="First migration using django" />
</h2>

- Now initial tables have been created admin login credentials can be set up with the following:
	- python manage.py createsuperuser
- Simply follow steps for setting up your credentials

## Accessing the Salon CRM system in the browser

- Type the following:
	- python manage.py runserver
	
- The CRM system would be available via the <a href="http://127.0.0.1:8000/admin">admin</a>
	

**Application Overview Pdf: User Journeys**

A <a href="https://github.com/Kremzeeq/Salon_CRM_Project/blob/master/Salon_CRM_app_overview.pdf">Salon CRM app overview is available in pdf on GitHub</a> to provide guidance on using the application, in terms of basic user journeys.

## Know Issues

- Additional Features for development:
	- Appointment Detail View to provide warning to end user if appointment start time conflicts with another appointment
	- Appointment Summary Report to provide filter to view appointments e.g. by date


