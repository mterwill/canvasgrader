"""Simple interface with the Canvas grading API."""

import os
import requests

class CanvasGrader(object):
    """Simple interface with the Canvas grading API.
    Currently provides ability to create assignments and upload grades.
    """

    def __init__(self, base_uri, course_id, id_key=None, api_key=None):
        self.base_uri = base_uri
        self.course_id = course_id
        self.id_key = id_key

        if api_key == None:
            # Check the user's home directory for an api key
            path = os.path.expanduser('~/.canvasgrader')
            if not os.path.isfile(path):
                raise RuntimeError('Provide an API key in ~/.canvasgrader or as an argument')

            # If there is one, make sure it's secure
            if int(oct(os.stat(path).st_mode)[-3:]) > 600:
                raise RuntimeError('Tighten privileges on ~/.canvasgrader to 600 or less')

            with open(path) as f:
                api_key = f.read().strip()

        self.session = requests.Session()
        self.session.headers = {'Authorization': 'Bearer {}'.format(api_key)}

    def create_assignment(self, name, points_possible, published=True):
        """Create an assignment and return its id."""

        response = self.session.post(self.build_url('/assignments'), data={
            'assignment[name]': name,
            'assignment[points_possible]': points_possible,
            'assignment[published]': published,
        })

        response.raise_for_status() # throw error on bad request

        return response.json()['id']

    def grade_assignment(self, assignment_id, grades=None, comments=None):
        """Post grades for a given assignment id.

        grades is a dictionary which holds grades for the given assignment_id.
        Keys for the grades dictionary should identify a student by the
        corresponding self.id_key value.

        Note that as Canvas processes these grades as a deferred job you will
        not see an error returned by the API for bad keys.
        """

        def make_id_key(sid):
            id_key = str(sid)
            if self.id_key:
                # canvas expects keys in this format for SIS
                # https://canvas.instructure.com/doc/api/file.object_ids.html
                id_key = "{id_key}:{sid}".format(
                    id_key = self.id_key, sid = sid)
            return id_key


        grades_for_canvas = {}

        if grades:
            for sid, grade in grades.items():
                k = 'grade_data[{id_key}][posted_grade]'.format(
                    id_key=make_id_key(sid))
                grades_for_canvas[k] = grade

        if comments:
            for sid, comment in comments.items():
                k = 'grade_data[{id_key}][text_comment]'.format(
                    id_key=make_id_key(sid))
                grades_for_canvas[k] = comment

        return self.session.post(
            self.build_url('/assignments/{}/submissions/update_grades'.format(assignment_id)),
            data=grades_for_canvas
        ).raise_for_status() # throw error on bad request (e.g. unpublished assignment)

    def build_url(self, path):
        """Build the URL for a canvas API request given instance values."""

        return 'https://{}/api/v1/courses/{}/{}'.format(
            self.base_uri, self.course_id, path.strip('/'))
