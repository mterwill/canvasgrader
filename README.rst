canvasgrader
============

This package provides a simple interface with the Canvas grading API to
save you the hassle of dealing with the web gradebook.

Installation
------------

.. code:: bash

    pip install canvasgrader

Usage
-----

1. Generate a new Access Token at
   ``https://<canvas-installation>/profile/settings``
2. Grab your course ID from the web interface:
   ``https://<canvas-installation>/courses/<course-id>``
3. Choose a
   `key <https://canvas.instructure.com/doc/api/file.object_ids.html>`__
   by which you want to identify students

.. code:: python

    >>> from canvasgrader import CanvasGrader
    >>> api_key = 'your access token'
    >>> canvas_grader = CanvasGrader(api_key=api_key, base_uri='umich.instructure.com',
                                     course_id=85425, id_key='sis_login_id')
    >>> assignment_id = canvas_grader.create_assignment(name='Homework 01',
                                                        points_possible=4)
    >>> canvas_grader.grade_assignment(assignment_id, {
            'mterwil': 4,
        })

Alternatively, you may place the API key in a dotfile:

.. code:: bash

    $ echo "my api key" > ~/.canvasgrader
    $ chmod 600 ~/.canvasgrader
