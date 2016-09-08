import os
from croniter import croniter
from datetime import datetime
from targets import TARGETS
from flask import Flask, render_template


app = Flask(__name__)
MAX_DATE = 999999999999


def monitor(tid, monitor):
    root_path = '/backup/%s' % tid
    path = os.path.join(root_path, monitor['path'])
    i = croniter(monitor['period'])
    should_last = i.get_prev(float) - 9 * 3600 - 59

    if monitor['type'] == 'ONE':
        if not os.path.isfile(path):
            return False, MAX_DATE, 0, 0

        last = os.path.getmtime(path)
        last_size = os.path.getsize(path)

        success = last >= should_last
        return success, last, last_size, last_size

    file_list = os.listdir(path)
    last = 0
    last_path = None
    total_size = 0

    for name in file_list:
        file_path = os.path.join(path, name)
        if not os.path.isfile(file_path):
            continue

        dot_index = name.index(".")
        fn, ext = name[:dot_index], name[dot_index:]
        if len(fn) != 8 or ext != monitor['ext']:
            continue

        mtime = os.path.getmtime(path)
        if last < mtime:
            last = mtime
            last_path = file_path

        total_size += os.path.getsize(file_path)

    if not last_path:
        return False, MAX_DATE, 0, 0

    success = last >= should_last
    last_size = os.path.getsize(last_path)

    return success, last, last_size, total_size


def date_readable(timestamp):
    if timestamp == MAX_DATE:
        return 'Not Started'
    return datetime.fromtimestamp(timestamp).isoformat()


def size_readable(size):
    postfix = ["", "KB", "MB", "GB", "TB"]
    iteration = 0
    size = float(size)
    while size >= 1024:
        iteration += 1
        size /= 1024

    return "%.2f%s" % (size, postfix[iteration])


@app.route('/')
def show_status():
    status = []
    for target in TARGETS:
        tid = target['id']
        s = {
            'success': True,
            'name': target['name'],
            'last': MAX_DATE,
            'last_size': 0,
            'total_size': 0,
        }

        for m in target['monitor']:
            success, last, last_size, total_size = monitor(tid, m)
            s['success'] = s['success'] and success
            s['last'] = min(s['last'], last)
            s['last_size'] += last_size
            s['total_size'] += total_size

        s['last'] = date_readable(s['last'])
        s['last_size'] = size_readable(s['last_size'])
        s['total_size'] = size_readable(s['total_size'])
        status.append(s)

    return render_template('index.html', status=status)
