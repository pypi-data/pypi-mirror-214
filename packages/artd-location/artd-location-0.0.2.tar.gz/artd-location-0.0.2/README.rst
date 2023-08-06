=================
Loications
=================

A Django app to create locations.


Quick start
-----------

1. Add "artd_location" to your INSTALLED_APPS setting like this:
    
        INSTALLED_APPS = [
            ...
            'artd_location',
        ]

2. Run ``python manage.py migrate`` to create the location models.

3. Run ``python manage.py create_countries`` to create create countries

4. Run ``python manage.py create_regions`` to create create regions

5. Run ``python manage.py create_cities`` to create create cities

6. Start the development server and visit http://127.0.0.1:8000/admin/