import requests

class MW_API:

  def __init__(self,api_key,api_url='https://api.microworkers.com'):
    self.api_key = api_key
    self.api_url = api_url
  
  def do_request(self, method = '', action = '', params = {}, files = {}):
    method = method.lower();
    if not method in ['get', 'put', 'post']:
      raise Exception('Method: "' + method + '" is not supported');

    headers = {'MicroworkersApiKey': self.api_key}
    
    if method == 'get':
      r = requests.get(self.api_url + action, params=params, headers=headers)
    if method == 'put':
      r = requests.put(self.api_url + action, data=params, headers=headers)
    if method == 'post':
      r = requests.post(self.api_url + action, files=files, data=params, headers=headers)
    
    if r.status_code == requests.codes.ok:
      try:
        value = r.json()
        return {'type': 'json', 'value': value}
      except ValueError, e:
        return {'type': 'body', 'value' : r.content}
      
    try:
      r.raise_for_status()
    except Exception, e:
      return {'type': 'error', 'value': e}