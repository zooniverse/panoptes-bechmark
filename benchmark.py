import datetime
import sys

from panoptes_client import (
    Project,
    Subject,
    SubjectSet,
    Workflow,
)


TEST_REPEATS = 5


def time_exec(func):
    start = datetime.datetime.now()
    func()
    end = datetime.datetime.now()
    return (end-start).total_seconds()

subject_set_ids = (5751, 8450, 8451)
subject_ids = []
workflow_ids = []

def first_10_subjects():
    for subject_set_id in subject_set_ids:
        subjects = Subject.where(subject_set_id=subject_set_id)
        for s in subjects.object_list:
            subject_ids.append(s['id'])

tests = [
    ('List launch approved projects', (
        lambda: [x for x in Project.where(launch_approved=True)]
    )),
    ('List workflows for Muon Hunter', (
        lambda: [w for w in Workflow.where(project_id=3098)]
    )),
    ('List workflows for Gravity Spy', (
        lambda: [w for w in Workflow.where(project_id=1104)]
    )),
    ('List subject sets for Muon Hunter', (
        lambda: [s for s in SubjectSet.where(project_id=3098)]
    )),
    ('List subject sets for Gravity Spy', (
        lambda: [s for s in SubjectSet.where(project_id=1104)]
    )),
    ('List first 10 subjects in subject sets', first_10_subjects),
    ('Fetch subjects by ID', (
        lambda: [Subject.find(s_id) for s_id in subject_ids[:10]]
    )),
    ('Fetch queued subjects for workflow', (
        lambda: [
            s for s in Subject.where(id='queued', workflow_id=2473).object_list
        ]
    )),
]

NAME_FORMAT_STRING = '\033[1m{{:>{}}}\033[0m'.format(
    max(map(len, [t[0] for t in tests]))
)
AVG_FORMAT_STRING = '\t\033[36m{:.2f}\033[0m'

for name, func in tests:
    print NAME_FORMAT_STRING.format(name),
    sys.stdout.flush()
    results = []
    for repeat in range(TEST_REPEATS):
        result = time_exec(func)
        results.append(result)
        print '\t{:.2f}'.format(result),
        sys.stdout.flush()
    print AVG_FORMAT_STRING.format(float(sum(results)) / len(results))
