Change Log
----------

..
   All enhancements and patches to learner_pathway_progress will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

[1.3.4]- 2023-06-16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Added management command to update existing LearnerPathwayProgress table.

[1.3.3]- 2022-10-07
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Added a data migration to delete data for LearnerEnterprisePathwayMembership and LearnerPathwayProgress table.

[1.3.2]- 2022-09-07
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Added enterprise with learner pathway membership.

[1.3.1]- 2022-09-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Removed default attribute from `LearnerPathwayProgress.learner_pathway_uuid` field. This field must be provided at the time of instance creation.

[1.3.0]- 2022-08-11
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Added endpoint for LearnerPathwayProgress model.

[1.2.3]- 2022-07-14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Update the pathway progress type.

[1.2.2]- 2022-07-05
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Added waffle flag on the top of signals code.

[1.2.1]- 2022-06-20
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Update signal to accept CourseLocator as course_key.

[1.2.0]- 2022-06-10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Add management command and signal to update learner pathway progress and membership.

[1.1.0] - 2022-06-02
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* entry point for app
* app_label in model

Changed
_______

* Plugin app configuration


[1.0.1] - 2022-06-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* Version in __init__.py

Changed
_______

* name of package in setup.py file


[1.0.0] - 2022-06-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Basic skeleton of the app.
* LearnerPathwayMembership model.

Changed
_______

* main branch from `main` to `master`
