'''

Django module for processing and arranging born digital content.


Note on Permissions
-------------------

Currently, the arrangement app uses Fedora object status to indicate
whether an item is processed or accessioned (i.e., unprocessed), in
order to allow restricting researcher access to unprocessed items.
Processed items will have a Fedora object status of ``Active``;
accessioned items should have a status of ``Inactive``.


The arrangement app currently uses two content models to allow
distinguishing between restricted and unrestricted items (which can be
accessed on the researcher workstation using the rushdie web app).
These two content models are:

* emory-control:ArrangementAccessAllowed-1.0
* emory-control:ArrangementAccessRestricted-1.0

'''

