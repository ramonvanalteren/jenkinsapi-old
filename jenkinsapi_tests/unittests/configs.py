from jenkinsapi import config

JOB_DATA = {
    "actions": [{
        "parameterDefinitions": [{
            "defaultParameterValue": {
                "name": "param1",
                "value": "test1"
            },
            "description": "",
            "name": "param1",
            "type": "StringParameterDefinition"
        }, {
            "defaultParameterValue": {
                "name": "param2",
                "value": ""
            },
            "description": "",
            "name": "param2",
            "type": "StringParameterDefinition"
        }]
    }],
    "description": "test job",
    "displayName": "foo",
    "displayNameOrNull": None,
    "name": "foo",
    "url": "http://halob:8080/job/foo/",
    "buildable": True,
    "builds": [
        {"number": 3, "url": "http://halob:8080/job/foo/3/"},
        {"number": 2, "url": "http://halob:8080/job/foo/2/"},
        {"number": 1, "url": "http://halob:8080/job/foo/1/"}
    ],
    # allBuilds is not present in job dict returned by Jenkins
    # it is inserted here to test _add_missing_builds()
    "allBuilds": [
        {"number": 3, "url": "http://halob:8080/job/foo/3/"},
        {"number": 2, "url": "http://halob:8080/job/foo/2/"},
        {"number": 1, "url": "http://halob:8080/job/foo/1/"}
    ],
    "color": "blue",
    "firstBuild": {"number": 1, "url": "http://halob:8080/job/foo/1/"},
    "healthReport": [{
        "description": "Build stability: No recent builds failed.",
        "iconUrl": "health-80plus.png", "score": 100
    }],
    "inQueue": False,
    "keepDependencies": False,
    # build running
    "lastBuild": {"number": 4, "url": "http://halob:8080/job/foo/4/"},
    "lastCompletedBuild": {"number": 3,
                           "url": "http://halob:8080/job/foo/3/"},
    "lastFailedBuild": None,
    "lastStableBuild": {"number": 3,
                        "url": "http://halob:8080/job/foo/3/"},
    "lastSuccessfulBuild": {"number": 3,
                            "url": "http://halob:8080/job/foo/3/"},
    "lastUnstableBuild": None,
    "lastUnsuccessfulBuild": None,
    "nextBuildNumber": 4,
    "property": [],
    "queueItem": None,
    "concurrentBuild": False,
    # test1 job exists, test2 does not
    "downstreamProjects": [{'name': 'test1'}, {'name': 'test2'}],
    "scm": {},
    "upstreamProjects": []
}

URL_DATA = {'http://halob:8080/job/foo/%s' % config.JENKINS_API: JOB_DATA}

BUILD_DATA = {
    'actions': [{
        'causes': [{
            'shortDescription': 'Started by user anonymous',
            'userId': None,
            'userName': 'anonymous'
        }]
    }],
    'artifacts': [],
    'building': False,
    'builtOn': 'localhost',
    'changeSet': {'items': [], 'kind': None},
    'culprits': [],
    'description': 'Best build ever!',
    "duration": 5782,
    'estimatedDuration': 106,
    'executor': None,
    "fingerprint": [{
        "fileName": "BuildId.json",
        "hash": "e3850a45ab64aa34c1aa66e30c1a8977",
        "original": {"name": "ArtifactGenerateJob", "number": 469},
        "timestamp": 1380270162488,
        "usage": [{
            "name": "test1",
            "ranges": {
                "ranges": [{"end": 567, "start": 566}]
            }
        }, {
            "name": "test2",
            "ranges": {
                "ranges": [{"end": 150, "start": 139}]
            }
        }]
    }],
    'fullDisplayName': 'foo #1',
    'id': '2013-05-31_23-15-40',
    'keepLog': False,
    'number': 1,
    'result': 'SUCCESS',
    'timestamp': 1370042140000,
    'url': 'http://localhost:8080/job/foo/1/',
    'runs': [{
        'number': 1,
        'url': 'http//localhost:8080/job/foo/SHARD_NUM=1/1/'
    }, {
        'number': 2,
        'url': 'http//localhost:8080/job/foo/SHARD_NUM=1/2/'
    }]
}

BUILD_SCM_DATA = {
    'actions': [{
        'causes': [{'shortDescription': 'Started by an SCM change'}]
    }, {
    }, {
        'buildsByBranchName': {
            'origin/HEAD': {
                'buildNumber': 2,
                'buildResult': None,
                'revision': {
                    'SHA1': 'd2a5d435fa2df3bff572bd06e43c86544749c5d2',
                    'branch': [
                        {'SHA1': 'd2a5d435fa2df3bff572bd06e43c86544749c5d2',
                         'name': 'origin/HEAD'},
                        {'SHA1': 'd2a5d435fa2df3bff572bd06e43c86544749c5d2',
                         'name': 'origin/master'}
                    ]
                }
            },
            'origin/master': {
                'buildNumber': 2,
                'buildResult': None,
                'revision': {
                    'SHA1': 'd2a5d435fa2df3bff572bd06e43c86544749c5d2',
                    'branch': [
                        {'SHA1': 'd2a5d435fa2df3bff572bd06e43c86544749c5d2',
                         'name': 'origin/HEAD'},
                        {'SHA1': 'd2a5d435fa2df3bff572bd06e43c86544749c5d2',
                         'name': 'origin/master'}
                    ]
                }
            },
            'origin/python_3_compatibility': {
                'buildNumber': 1,
                'buildResult': None,
                'revision': {
                    'SHA1': 'c9d1c96bc926ff63a5209c51b3ed537e62ea50e6',
                    'branch': [
                        {'SHA1': 'c9d1c96bc926ff63a5209c51b3ed537e62ea50e6',
                         'name': 'origin/python_3_compatibility'}
                    ]
                }
            },
            'origin/unstable': {
                'buildNumber': 3,
                'buildResult': None,
                'revision': {
                    'SHA1': '7def9ed6e92580f37d00e4980c36c4d36e68f702',
                    'branch': [
                        {'SHA1': '7def9ed6e92580f37d00e4980c36c4d36e68f702',
                         'name': 'origin/unstable'}
                    ]
                }
            }
        },
        'lastBuiltRevision': {
            'SHA1': '7def9ed6e92580f37d00e4980c36c4d36e68f702',
            'branch': [
                {'SHA1': '7def9ed6e92580f37d00e4980c36c4d36e68f702',
                 'name': 'origin/unstable'}
            ]
        },
        'remoteUrls': [
            'https://github.com/salimfadhley/jenkinsapi.git'
        ],
        'scmName': ''
    }, {
    }, {
    }],
    'artifacts': [],
    'building': False,
    'builtOn': '',
    'changeSet': {'items': [], 'kind': 'git'},
    'culprits': [],
    'description': None,
    'duration': 1051,
    'estimatedDuration': 2260,
    'executor': None,
    'fullDisplayName': 'git_yssrtigfds #3',
    'id': '2013-06-30_01-54-35',
    'keepLog': False,
    'number': 3,
    'result': 'SUCCESS',
    'timestamp': 1372553675652,
    'url': 'http://localhost:8080/job/git_yssrtigfds/3/'
}
