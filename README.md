Django Live Calculator
======================

Illustrates a "live calculator which logs sessions" using Channels (Django 1.9+). This is a page that shows a series
of short-form logs in descending date order, with new ones appearing at the
top as they're logged.

The site supports multiple calculators at once, and clients only listen for new
logs on the calculator they're currently viewing.

When you view a calculator page, we open a WebSocket to Django, and the consumer
there adds it to a Group based on the calculator slug it used in the URL of the
socket. Then, in the ``save()`` method of the ``Log`` model, we send notifications
onto that Group that all currently connected clients pick up on, and insert
the new log at the top of the page.


Installation
------------

Manual installation
~~~~~~~~~~~~~~~~~~~~~~

Make a new virtualenv for the project, and run::

    pip install -r requirements.txt

Then, you'll need Redis running locally; the settings are configured to
point to ``localhost``, port ``6379``, but you can change this in the
``CHANNEL_LAYERS`` setting in ``settings.py``.

Finally, run::

    python manage.py migrate
    python manage.py runserver

Docker installation
~~~~~~~~~~~~~~~~~~~~~~

Run the app::

    docker-compose up

The app will now be running on: {your-docker-ip}:8000

* You will need to prefix ``python manage.py`` commands with: ``docker-compose run --rm web``. e.g.: ``docker-compose run --rm web python manage.py createsuperuser``

Finally, run::

    docker-compose run --rm web python manage.py migrate

Usage
-----

Make yourself a superuser account::

    python manage.py createsuperuser

Then, log into http://localhost:8000/admin/ and make a new Calculator object.

Open a new window, go to http://localhost:8000/, and click on your new calculator
to see its logs page.

Now, in the admin, make some new Logs against your calculator or perform calculations, and watch them appear
in your new window. Edit them, and they'll update themselves live on the page too.


Further Reading
---------------

You can find the Channels documentation at http://channels.readthedocs.org
