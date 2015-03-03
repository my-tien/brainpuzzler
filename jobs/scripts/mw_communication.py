from datetime import datetime
from pprint import pprint

from jobs.scripts.MW_API import MW_API


mw_api = MW_API('af801b23166b3a7a80df6eaf7efa3031095d16e69572f910a5c88bf2f6cf7fd9')
campaign_id = '2ebd1883a3f7'


def get_tasks():
    return mw_get('/campaign_hg/list_tasks/' + campaign_id)["tasks"]


def get_unrated_tasks():
    tasks = get_tasks()
    if tasks is not None:
        return [task for task in tasks if "NOTRATED" in task]


def get_accepted_tasks():
    tasks = get_tasks()
    if tasks is not None:
        return [task for task in tasks if "SATISFIED" in task]


def rate_task(task_id, accepted, comment):
    response = mw_put('/campaign_hg/rate_task/' + campaign_id,
                      {
                          'id_task': str(task_id),
                          'rating': 'OK' if accepted else 'NOK',
                          'comment': comment
                      })
    pprint(response)


def get_task_vcode(task_id):
    task_info = mw_get('/campaign_hg/get_task_info/{0}'.format(task_id))
    if task_info is not None and len(task_info["task_details"]["proof"]) > 0:
        return task_info["task_details"]["proof"][0]


def get_task_worker(task_id):
    task_info = mw_get('/campaign_hg/get_task_info/{0}'.format(task_id))
    if task_info is not None:
        return task_info["task_details"]["worker_id"]


def get_submission_date(task_id):
    task_info = mw_get('/campaign_hg/get_task_info/{0}'.format(task_id))
    if task_info is not None:
        date = datetime.strptime(task_info["task_details"]["finished_datetime"])
        print(date)


def mw_get(url):
    response = mw_api.do_request('GET', url)
    if response["value"]["status"] == "SUCCESS":
        return response["value"]


def mw_put(url, content):
    response = mw_api.do_request('PUT', url, content)
    if response["value"]["status"] == "SUCCESS":
        return response["value"]