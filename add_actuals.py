import pandas as pd
import json
import requests

# credentials
API_TOKEN = ''
USERNAME = ''

# deployment instance
DEPLOYMENT_ID = ''

# dataset with actual outcomes
#
# REQUIREMENTS:
#   * prediction input and result storage must be enabled on your account
#   * need an associationId (join key) and actualValue
#   * can optionally include a timestamp and a flag indicating action was taken
#   * MAX 10000 RECORDS
#
actuals = pd.read_csv('actuals.csv')
actuals['associationId'] = actuals['key']
actuals['actualValue'] = actuals['value']
data = json.dumps({
    'data':
    actuals[['associationId', 'actualValue']].to_dict('records')
})

# set up request
headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    # datarobot-key only required for cloud deployments
    'datarobot-key': '',
    'Authorization': 'Token %s' % API_TOKEN
}

# if installed on-prem replace url with location of your instance
response = requests.post(
    'https://app.datarobot.com/api/v2/deployments/%s/actuals/fromJSON' % DEPLOYMENT_ID
    data=data,
    headers=headers
)
