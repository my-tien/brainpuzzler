from datetime import datetime
from pprint import pprint

from jobs.scripts.MW_API import MW_API


mw_api = MW_API('af801b23166b3a7a80df6eaf7efa3031095d16e69572f910a5c88bf2f6cf7fd9')
campaign_id = '821113b0c802'


def get_tasks():
    return mw_get('/campaign_hg/list_tasks/' + campaign_id)["tasks"]

def get_unrated_tasks():
    tasks = get_tasks()
    if tasks is not None:
        return [task for task in tasks if "NOTRATED" in task]


def get_accepted_tasks():
    tasks = get_tasks()
    if tasks is not None:
        return [task for task in tasks if "OK" in task]


def get_tasks_from(mw_id):
    return mw_get('/campaign_hg/get_worker_tasks/' + campaign_id + "_" + mw_id)["tasks"]


class Task:
    def __init__(self, task_id):
        self.id = task_id
        self.info = mw_get('/campaign_hg/get_task_info/{0}'.format(task_id))

    def vcode(self):
        if len(self.info["task_details"]["proof"]) > 0:
            return self.info["task_details"]["proof"][0]

    def worker(self):
        return self.info["task_details"]["worker_id"]

    def submit_date(self):
        return datetime.strptime(self.info["task_details"]["finished_datetime"], "%Y-%m-%d %X")

    def rate(self, accepted, comment):
        response = mw_put('/campaign_hg/rate_task/' + campaign_id,
                          {
                              'id_task': str(self.id),
                              'rating': 'OK' if accepted else 'NOK',
                              'comment': comment
                          })
        pprint(response)


def mw_get(url):
    response = mw_api.do_request('GET', url)
    if response["value"]["status"] == "SUCCESS":
        return response["value"]


def mw_put(url, content):
    response = mw_api.do_request('PUT', url, content)
    if response["value"]["status"] == "SUCCESS":
        return response["value"]