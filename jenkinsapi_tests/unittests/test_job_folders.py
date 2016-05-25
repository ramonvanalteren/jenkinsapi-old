import mock
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from jenkinsapi.jenkins import JenkinsBase


class TestJobFolders(unittest.TestCase):

    def setUp(self):
        self.jb = JenkinsBase('http://localhost:8080/', poll=False)

    @mock.patch('jenkinsapi.jenkins.JenkinsBase.resolve_job_folders')
    @mock.patch('jenkinsapi.jenkins.JenkinsBase._poll')
    def test_called_in__poll(self, _poll_mock, resolve_job_folders_mock):
        _poll_mock.return_value = {
            'description': "My jobs",
            'jobs': [
                {
                    'name': "Foo",
                    'url': "http://localhost:8080/job/Foo",
                    'color': "blue",
                },
            ],
            'name': "All",
            'property': [],
            'url': "http://localhost:8080/view/All/",
        }

        self.jb.poll()

        resolve_job_folders_mock.assert_called_once_with(
            [
                {
                    'name': "Foo",
                    'url': "http://localhost:8080/job/Foo",
                    'color': "blue",
                },
            ],
        )

    def test_no_folders(self):
        jobs = [
            {
                'name': "Foo",
                'url': "http://localhost:8080/job/Foo",
                'color': "blue",
            },
            {
                'name': "Bar",
                'url': "http://localhost:8080/job/Bar",
                'color': "disabled",
            },
        ]

        self.assertEquals(
            self.jb.resolve_job_folders(jobs),
            [
                {
                    'name': "Foo",
                    'url': "http://localhost:8080/job/Foo",
                    'color': "blue",
                },
                {
                    'name': "Bar",
                    'url': "http://localhost:8080/job/Bar",
                    'color': "disabled",
                },
            ]
        )

    @mock.patch('jenkinsapi.jenkins.JenkinsBase.get_data')
    def test_empty_folder(self, get_data_mock):
        get_data_mock.return_value = {'jobs': []}
        jobs = [
            {
                'name': "Folder1",
                'url': "http://localhost:8080/job/Folder1",
            },
        ]

        self.assertEquals(self.jb.resolve_job_folders(jobs), [])
        get_data_mock.assert_called_once_with(
            'http://localhost:8080/job/Folder1/api/python',
            tree='jobs[name,color]'
        )

    @mock.patch('jenkinsapi.jenkins.JenkinsBase.get_data')
    def test_folder_job_mix(self, get_data_mock):
        get_data_mock.return_value = {'jobs': [
            {
                'name': "Bar",
                'url': "http://localhost:8080/job/Folder1/job/Bar",
                'color': "disabled",
            },
        ]
        }
        jobs = [
            {
                'name': "Foo",
                'url': "http://localhost:8080/job/Foo",
                'color': "blue",
            },
            {
                'name': "Folder1",
                'url': "http://localhost:8080/job/Folder1",
            },
        ]

        self.assertEquals(
            self.jb.resolve_job_folders(jobs),
            [
                {
                    'name': "Foo",
                    'url': "http://localhost:8080/job/Foo",
                    'color': "blue",
                },
                {
                    'name': "Bar",
                    'url': "http://localhost:8080/job/Folder1/job/Bar",
                    'color': "disabled",
                },
            ]
        )
        get_data_mock.assert_called_once_with(
            'http://localhost:8080/job/Folder1/api/python',
            tree='jobs[name,color]'
        )

    @mock.patch('jenkinsapi.jenkins.JenkinsBase.get_data')
    def test_multiple_folders(self, get_data_mock):
        get_data_mock.side_effect = [
            # first call
            {
                'jobs': [
                    {
                        'name': "Foo",
                        'url': "http://localhost:8080/job/Folder1/job/Foo",
                        'color': "disabled",
                    },
                ]
            },

            # second call
            {
                'jobs': [
                    {
                        'name': "Bar",
                        'url': "http://localhost:8080/job/Folder2/job/Bar",
                        'color': "blue",
                    },
                ]
            },
        ]

        jobs = [
            {
                'name': "Folder1",
                'url': "http://localhost:8080/job/Folder1",
            },
            {
                'name': "Folder2",
                'url': "http://localhost:8080/job/Folder2",
            },
        ]

        self.assertEquals(
            self.jb.resolve_job_folders(jobs),
            [
                {
                    'name': "Foo",
                    'url': "http://localhost:8080/job/Folder1/job/Foo",
                    'color': "disabled",
                },
                {
                    'name': "Bar",
                    'url': "http://localhost:8080/job/Folder2/job/Bar",
                    'color': "blue",
                },
            ]
        )

        self.assertEquals(
            get_data_mock.call_args_list,
            [
                mock.call(
                    'http://localhost:8080/job/Folder1/api/python',
                    tree='jobs[name,color]'
                ),
                mock.call(
                    'http://localhost:8080/job/Folder2/api/python',
                    tree='jobs[name,color]'
                ),
            ]
        )

    @mock.patch('jenkinsapi.jenkins.JenkinsBase.get_data')
    def test_multiple_folder_levels(self, get_data_mock):
        get_data_mock.side_effect = [
            # first call
            {
                'jobs': [
                    {
                        'name': "Bar",
                        'url': "http://localhost:8080/job/Folder1/job/Bar",
                        'color': "disabled",
                    },
                    {
                        'name': "Folder2",
                        'url': "http://localhost:8080/job/Folder1/job/Folder2",
                    },
                ]
            },

            # second call
            {
                'jobs': [
                    {
                        'name': "Baz",
                        'url': "http://localhost:8080/job/Folder1/job/Folder2/job/Baz",
                        'color': "disabled",
                    },
                ]
            },
        ]

        jobs = [
            {
                'name': "Foo",
                'url': "http://localhost:8080/job/Foo",
                'color': "blue",
            },
            {
                'name': "Folder1",
                'url': "http://localhost:8080/job/Folder1",
            },
        ]

        self.assertEquals(
            self.jb.resolve_job_folders(jobs),
            [
                {
                    'name': "Foo",
                    'url': "http://localhost:8080/job/Foo",
                    'color': "blue",
                },
                {
                    'name': "Bar",
                    'url': "http://localhost:8080/job/Folder1/job/Bar",
                    'color': "disabled",
                },
                {
                    'name': "Baz",
                    'url': ("http://localhost:8080/job/Folder1"
                            "/job/Folder2/job/Baz"),
                    'color': "disabled",
                },
            ]
        )

        self.assertEquals(
            get_data_mock.call_args_list,
            [
                mock.call(
                    'http://localhost:8080/job/Folder1/api/python',
                    tree='jobs[name,color]'
                ),
                mock.call(
                    'http://localhost:8080/job/Folder1'
                    '/job/Folder2/api/python',
                    tree='jobs[name,color]'
                ),
            ]
        )
