import json
from pprint import pprint

from jobs.scripts.MW_API import MW_API


mw_api = MW_API('af801b23166b3a7a80df6eaf7efa3031095d16e69572f910a5c88bf2f6cf7fd9')


class Campaign:
    def __init__(self, campaign_id):
        self.campaign_id = campaign_id

    def get_tasks(self):
        return mw_get('/campaign_hg/list_tasks/' + self.campaign_id)

    def get_unrated_tasks(self):
        tasks = self.get_tasks()
        if tasks is not None:
            return [task for task in tasks["tasks"] if "NOTRATED" in task]

    def rate_task(self, task_id, accepted, comment):
        response = mw_put('/campaign_hg/rate_task/' + self.campaign_id,
                          {
                              'id_task': str(task_id),
                              'rating': 'OK' if accepted else 'NOK',
                              'comment': comment
                          })
        pprint(response)


def get_task_vcode(task_id):
    task_info = mw_get('/campaign_hg/get_task_info/{0}'.format(task_id))
    if task_info is not None and len(task_info["proof"]) > 0:
        return task_info["proof"][0]


def mw_get(url):
    try:
        response = json.loads(mw_api.do_request('GET', url))
        if response["status"] is "SUCCESS":
            return response
    except ValueError:
        return None


def mw_put(url, content):
    try:
        response = json.loads(mw_api.do_request('PUT', url, content))
        if response["status"] is "SUCCESS":
            return response
    except ValueError:
        return None