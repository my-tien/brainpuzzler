import json
from pprint import pprint

from jobs.MW_API import MW_API


mw_api = MW_API('af801b23166b3a7a80df6eaf7efa3031095d16e69572f910a5c88bf2f6cf7fd9')

class Campaign:

    def __init__(self, campaign_id):
        self.campaign_id = campaign_id 


    def get_tasks(self):
        return mw_api.do_request('GET', '/campaign_hg/list_tasks/' + self.campaign_id)
    

    def get_unrated_tasks(self):
        tasks = get_tasks()
        if tasks["status"] is "SUCCESS":
            return [task for task in tasks["tasks"] if "NOTRATED" in task]


    def rate_task(self, task_id, accepted, comment):
        response = mw_api.do_request('PUT', '/campaign_hg/rate_task/' + self.campaign_id, {
          'id_task': str(task_id),
          'rating': 'OK' if accepted else 'NOK',
          'comment': comment
        })
        pprint(response)