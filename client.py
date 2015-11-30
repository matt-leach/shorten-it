import httplib
import json

# use this server for dev
SERVER = 'localhost:5000'

# use this server for prod, once it's on ec2
# SERVER = 'xxxxx.aws.ec2.com:5000'


def create_shortened_url(data):
    out = dict()
    h = httplib.HTTPConnection(SERVER)
    data = json.dumps(data)
    h.request('POST', 'http://'+SERVER+'/shorten', body=data)
    resp = h.getresponse()
    out = resp.read()
    return out

if __name__ == '__main__':
    print '----------------'
    print 'try to create shortened url with no url parameter:'
    print create_shortened_url({})
    print 'create shortened url to google with hash "g"'
    print create_shortened_url({'url': 'www.google.com', 'hash': 'g'})
    print 'try again with same hash - not allowed:'
    print create_shortened_url({'url': 'www.google.com', 'hash': 'g'})
