=================
Partner
=================

A Django app to create partners.


Quick start
-----------
1. Install artd_location and add to your INSTALLED_APPS like this:
    
        INSTALLED_APPS = [
            ...
            'artd_location',
        ]

2. Run ``python manage.py migrate`` to create the cities models.

3. run ``python manage.py create_countries`` to create the countries.

4. run ``python manage.py create_regions`` to create the regions.

5. run ``python manage.py create_cities`` to create the cities.

6. Add "artd_partner" to your INSTALLED_APPS setting like this:
    
        INSTALLED_APPS = [
            ...
            'artd_partner',
        ]

7. Run ``python manage.py migrate`` to create the Partner models.

3. Start the development server and visit http://127.0.0.1:8000/admin/