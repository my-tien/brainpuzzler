__author__ = 'tieni'

import os
import numpy
from xml.dom import minidom
from zipfile import ZipFile

from brainpuzzler.settings import MEDIA_ROOT
from jobs.models import Submission
from jobs.mergelist import Mergelist
from jobs.plotter import save_histogram
from jobs.scripts.submission_validation import time
from jobs.mw_communication import campaign_info, get_tasks, get_accepted_tasks, get_tasks_from, Task


def run(*args):
    submissions = None
    times = []
    if "conventional-time" in args:
        base = "/home/knossos/conventional_submits/"
        folders = [name for name in os.listdir(base)]
        for dir in folders:
            if dir == "mergelists":
                continue
            for file in os.listdir(base + dir):
                with ZipFile(base + dir + "/" + file, 'r') as kzip, kzip.open("annotation.xml", 'r') as xml:
                    annotation = str(xml.read(), 'utf-8')
                    times.append(time(annotation)/1000/60)
                    if time(annotation)/1000/60 == 0:
                        print(base + dir + "/" + file + " with time {0}".format(time(annotation)))
        save_histogram(times, [x*5 for x in range(0, 10)], "time in minutes", "number of jobs", "conventional_time.png")
        print("{0:.2f} min avg time, {1:.2f} h total time ({2} files, {3} min, {4} max)"
              .format(sum(times)/len(times), sum(times)/60, len(times), min(times), max(times)))

    if "mw-time" in args:
        times = []
        valid_submits = Submission.objects.filter(state__in=[Submission.CREATED, Submission.ACCEPTED])
        valids = len(valid_submits)
        for index, submission in enumerate(valid_submits):
            print("we are at {0} from {1}".format(index, valids))
            annotation = submission.annotation()
            if annotation:
                times.append(time(submission.annotation())/1000/60)

        save_histogram(times, [x*5 for x in range(0, 10)], "time in minutes", "number of jobs", "mw_time.png")
        print("{0:.2f} min avg time, {1:.2f} h total time ({2} files, {3} min, {4} max)"
              .format(sum(times)/len(times), sum(times)/60, len(times), min(times), max(times)))

    if "time-per-todo" in args:
        if submissions is None:
            submissions = Submission.objects.all()
        for submission in submissions:
            submission_path = MEDIA_ROOT + os.path.basename(submission.submit_file.name)
            job_path = MEDIA_ROOT + os.path.basename(submission.job.job_file.name)
            with ZipFile(job_path, 'r') as job, \
                    ZipFile(submission_path, 'r') as submit, submit.open("annotation.xml", 'r') as annotation:
                len_todolist = len([str(line, 'utf-8') for line in job.open("mergelist.txt", 'r')]) / 4
                xml_string = str(annotation.read(), 'utf-8')
                dom = minidom.parseString(xml_string)
                time_secs = int(dom.getElementsByTagName("time")[0].attributes["ms"].value) / 1000
                time_minutes = time_secs / 60
                time_per_todo = float(time_secs)/len_todolist
                times.append(time_per_todo)
                print("len {0}, time {1}min: {2:.1f}s/todo in file {3}"
                      .format(int(len_todolist), int(time_minutes), time_per_todo, os.path.basename(job_path)))
        avg_time = sum(times)/len(times)
        times.sort()
        print("average of {0} submits: {1:.1f}s/todo. range: [{2}, {3}]".format(len(times), avg_time, times[0], times[-1]))
        print(times)

    if "split-requests" in args:
        if submissions is None:
            submissions = Submission.objects.all()
        splits = []
        for submission in submissions:
            mergelist = submission.mergelist()
            splits.append(mergelist.count_comment("Split required"))
        splits.sort()
        avg_splits = sum(splits)/len(splits)
        print(splits)
        print("average of {0} submits: {1} splits/submit. range [{2}, {3}]".format(len(splits), avg_splits, splits[0], splits[-1]))

    if "submits-per-day" in args:
        accepted = get_tasks()
        dates = {}
        for elem in accepted:
            task = Task(elem[0])
            date = task.submit_date()
            found = False
            for date_elem in dates:
                if date_elem == date.date():
                    found = True
                    try:
                        dates[date_elem] += 1
                    except KeyError:
                        dates[date_elem] = 1
            if not found:
                dates[date.date()] = 1
        print(sorted(dates.items(), key=lambda x: x[0]))
        avg_submits = 0
        for num in dates.values():
            avg_submits += num
        avg_submits /= float(len(dates))
        print("Average submits per day ({0} days): {1:.2f}".format(len(dates), avg_submits))

    if "accepted-ratio" in args:
        info = campaign_info()
        ok = int(info["tasks_ok"])
        nok = int(info["tasks_nok"])
        print("{0} tasks: {1} accepted ({2:.2f}%) and {3} rejected tasks ({4:.2f}%)"
              .format(ok + nok, ok, ok/float(ok+nok), nok, nok/float(ok+nok)))

    if "workers" in args:
        tasks = get_tasks()
        workers = set()
        tasks = [Task(elem[0]) for elem in tasks]
        for task in tasks:
            workers.add(task.worker())
        print(workers)
        print("{0} workers participated.".format(len(workers)))

