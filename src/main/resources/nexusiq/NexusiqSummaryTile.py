import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest


username = nexusiqServer['username']
password = nexusiqServer['password']
httpRequest = HttpRequest(nexusiqServer, username, password)

apps = {}
violationsArray = []

# Fetching the list of policies
url = '/api/v2/policies/'
print "About to read Policy List"
response = httpRequest.get(url, contentType='application/json')
policyList = json.loads(response.getResponse())
#print json.dumps(policyList, indent=4)

# Grabbing policy name that matches the security-level
policy = [item for item in policyList['policies'] if item['name'] == secLevel ]
if policy:
  policyID = policy[0]['id']


  # Fetching policy voilations
  url = '/api/v2/policyViolations?p=%s' % policyID
  print "About to get violations from the response"
  response = httpRequest.get(url, contentType='application/json')
  violations = json.loads(response.getResponse())
  #print json.dumps(violations, indent=4)

  # Grabbing voilations for the matching application
  app = [item for item in violations['applicationViolations'] if item['application']['name'] == application]
  if app:
    for policyViolation in app[0]['policyViolations']:
      policyName = policyViolation['policyName']
      violationObject = {
          'appName'   : application,
          'stageId'   : policyViolation['stageId'],
          'reportUrl' : policyViolation['reportUrl'],
      }
      violationsArray.append(violationObject)

    appObject = {
      policyName : violationsArray
    }
    apps.update(appObject)
     
print "%s voilations for applicaton %s" % (secLevel, application)
data = json.dumps(apps)
print json.dumps(data, indent=4)
