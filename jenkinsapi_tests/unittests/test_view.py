import mock
import unittest

from jenkinsapi.view import View

class TestView(unittest.TestCase):

    DATA = {'description': 'Important Shizz',
            'jobs': [{'color': 'blue',
                      'name': 'foo',
                      'url': 'http://halob:8080/job/foo/'},
           {'color': 'red',
            'name': 'test_jenkinsapi',
            'url': 'http://halob:8080/job/test_jenkinsapi/'}],
            'name': 'FodFanFo',
            'property': [],
            'url': 'http://halob:8080/view/FodFanFo/'}

    @mock.patch.object(View, '_poll')
    def setUp(self, _poll):
        _poll.return_value = self.DATA

        # def __init__(self, url, name, jenkins_obj)
        self.J = mock.MagicMock()  # Jenkins object
        self.v = View('http://localhost:800/view/FodFanFo', 'FodFanFo', self.J)

    def testRepr(self):
        # Can we produce a repr string for this object
        self.assertEquals(repr(self.v), '<jenkinsapi.view.View FodFanFo>')

    def testStr(self):
        # Can we produce a repr string for this object
        self.assertEquals(str(self.v), 'FodFanFo')

    def testName(self):
        with self.assertRaises(AttributeError):
            self.v.id()
        self.assertEquals(self.v.name, 'FodFanFo')

    def test_get_job_dict(self):
        jobs = self.v.get_job_dict()
        self.assertTrue(isinstance(jobs, dict))
        self.assertTrue(len(jobs)==2)
        self.assertTrue(jobs.get('foo'))
        self.assertTrue(jobs.get('foo')=='http://halob:8080/job/foo/')

    def test_length(self):
        self.assertTrue(len(self.v)==2)

    def test_job_in_view(self):
        self.assertTrue(self.v['foo'])

if __name__ == '__main__':
    unittest.main()
