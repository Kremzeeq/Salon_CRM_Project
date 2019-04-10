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
	

**Demo**

MediaBudgieDemo.pptx in GitHub provides a prototype of the application and similuates a business user journey for setting up central budgets
-Please view business user journey for the Media Budgie Application here:


