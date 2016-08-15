"""
TARGETS = [
    {
        'id': 'unique id',
        'name': 'user friendly name',
        'monitor': [
            'target-name1': {
                'type': 'MULTI' or 'ONE',
                'path': 'file path',
                'ext': 'file extension',
                'period': 'cron period',
            },
            ...
        ]
    },
    ...
]

* id SHOULD equal to backup root path, e.g /backup/{id}
* path SHOULD start after backup root path
    * if type is MULTI, program will try to find
      /backup/{id}/{path}/YYYYMMDD{ext}
    * if type is ONE, program will try to find
      /backup/{id}/{path} and ext will be IGNORED
* ext SHOULD contain . (dot)
* period SHOULD the cron format, e.g 0 6 * * * *
"""

TARGETS = [
    {
        'id': 'test',
        'name': 'Test App',
        'monitor': [
            {
                'type': 'ONE',
                'path': 'one-greate-image-file.img',
                'period': '0 6 * * 0 *',
            },
            {
                'type': 'MULTI',
                'path': 'database',
                'ext': '.sql',
                'period': '0 0 * * * *',
            },
        ],
    },
]
