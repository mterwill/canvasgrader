# canvasgrader

## Usage:
1. Generate a new Access Token at `https://<canvas-installation>/profile/settings`
1. Grab your course ID from the web interface: `https://<canvas-installation>/courses/<course-id>`
1. Choose a [key] by which you want to identify students

```python
>>> from canvasgrader import CanvasGrader
>>> canvas_grader = CanvasGrader(api_key=api_key, base_uri='umich.instructure.com',
                                 course_id=85425, id_key='sis_login_id')
>>> assignment_id = canvas_grader.create_assignment(name='Homework 01',
                                                    points_possible=4)
>>> canvas_grader.grade_assignment(assignment_id, {
        'mterwil': 4,
    })
```

[key]: https://canvas.instructure.com/doc/api/file.object_ids.html
