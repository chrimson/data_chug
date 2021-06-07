import datetime as dt
import json
import re
import requests
import time
import base64

with open('config.json', 'r') as config_file:
  config = json.load(config_file, 'r')

SC_URL = ''
SC_UN = ''
SC_PW = ''


DAYS_CAP = 5

today = dt.datetime.utcnow()
year = today.year
month = '{:02}'.format(today.month)
#day
#hour
#minute

login = '{"username": "%s", "password": "%s"}' % (SC_UN, SC_PW)

response = requests.post('https://%s/rest/token' % SC_URL,
                         verify = False,
                         data = login)

common_headers = {'X-SecurityCenter': str(response.json()['response']['token']),
                  'Cookie': re.findall('(TNS_SESSIONID=[0-9a-f]+)', response.headers['set-cookie'])[1]}

json_headers = common_headers.copy()
json_headers['Content-Type'] = 'application/json'

download_headers = common_headers.copy()
download_headers.update({'Pragma': 'public',
                         'Expires': '0',
                         'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
                         'Content-Description': 'File Transfer',
                         'Content-Type': 'application/octet-stream',
                         'Content-Transfer-Encoding': 'binary'})

start_time = str(time.time() - int(DAYS_CAP) * 86400)
params = {'startTime': start_time,
          'filter': 'completed',
          'fields': 'name,id'}

response = requests.get('https://%s/rest/scanResult' % SC_URL,
                        params = params,
                        verify = False,
                        headers = json_headers)
scans = response.json()['response']

scan_type in ['usable', 'manageable']:

  for scan in scans[scan_type]:

    basename = ('%s_%s' % (scan['id', scan['name'])).replace(' ', '_').replace('/', '\\')
    filename = '%s.zip' % basename
    download_headers['Content-Disposition'] = 'attachment; filename="%s"' % filename

    try:
      response = requests.post('https://%s/rest/scanResult/%s/download' % (SC_URL, scan['id']),
                               json = {'downloadType': 'v2'},
                               verify = False,
                               headers = download_headers,
                               stream = True)

      with open(filename, 'wb') as scan_file:
        for chunk in response.iter_content(chunk_size = 128):
          scan_file.write(chunk)

    except:
      pass


    # Save the file
    # path_ext = '%s/%s/%s/%s' % (S3_PATH, year, month, day)

requests.delete('https://%s/rest/token' % SC_URL,
                verify = False,
                headers = json_headers)


