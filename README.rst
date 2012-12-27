activebuys
----------

Codebase for activebuys.com.


Known Issues
------------

1. accounts.Account inherits auth.models.User, so when you syncdb and migrate, and are prompted to create a superuser, the User you create won't be able to authenticate, since no corresponding accounts.Account was created for the new User.  To create an admin user:::

    >>> from apps.accounts.models import Account
    >>> a = Account.objects.create(username='admin',first_name='admin',is_superuser=True,is_staff=True,is_active=True)
    >>> a.set_password('adminpassword')
    >>> a.save()

2. /deals/ will show a 404 if no active, "home page" deals are present

3. There is a bug in Postgres GIS support for Django 1.3.2.  A Patch is available at bin/postgis-adapter-2.patch that will need to be applied to the django package, until it is included in a potential 1.3.3 security release.  See https://code.djangoproject.com/ticket/16778

4. "Export" link in deals.Deal changelist does not work properly

5. Purchase process chokes for Deals with no 'nonprofit' value

6. In Locations list, zipcode form submission returns to current page, but loses filter (GET) parameters

7. When running the test suite, psycopg2 versions 2.4.2 and higher will raise `psycopg2.ProgrammingError: autocommit cannot be used inside a transaction
`. psycopg2 2.4.1 must be used until this bug is properly fixed: http://psycopg.lighthouseapp.com/projects/62710/tickets/53  See also https://code.djangoproject.com/ticket/16250

8. The password reset link seems to be valid for an infinite number of uses.

9. The CompanyAddress geocode_address() method does not handle a full range of Exceptions.

Deployment
----------

The fabric.py file is configured for a staging and production version of the site, hosted at Rackspace.

The first parameter should be 'staging' or 'production', followed by other commands.

For instance, to deploy to production and restart the server:::

    $ fab production deploy restart