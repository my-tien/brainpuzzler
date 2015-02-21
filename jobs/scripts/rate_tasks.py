from scripts.mergelist_validation import Chunk
from scripts.mw_communication import Campaign


campaign_id = '2ebd1883a3f7'


def run(*args):
    campaign = Campaign(campaign_id)
    unrated = campaign.get_unrated_tasks()
    if unrated is None:
        print("No unrated tasks at the moment!")

    for task in unrated:
        pass    