place to play
==============
this is a django application that enables you to use https://www.placetopay.com/ payment processor in Colombia.

- from hash integration (form POST).
- from webservice API [TO DO].


how to install
----------------
1. install django
2. clone the project
3. important: setup settings.py configs with your p2p account data
4. python manange.py runserver
5. go to localhost:8000
6. if want to get status from pending transactions: python manage.py p2p_complete_pending_transactions

requirements
----------------
pip install suds (to consume placetopay soap webservice in order to update the PENDING transactions)

