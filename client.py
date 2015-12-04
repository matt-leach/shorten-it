import httplib
import json

# use this server for dev
SERVER = 'localhost:5000'

# use this server for prod, once it's on ec2
# SERVER = 'xxxxx.aws.ec2.com:5000'


def create_shortened_url(data):
    ''' connect to webapp and create a shortened url '''
    h = httplib.HTTPConnection(SERVER)
    data = json.dumps(data)
    h.request('POST', 'http://'+SERVER+'/shorten', body=data)
    resp = h.getresponse()
    return resp.read()


def visit_url(hashed):
    ''' visit /hashed '''
    h = httplib.HTTPConnection(SERVER)
    h.request('GET', 'http://'+SERVER+'/' + hashed)
    resp = h.getresponse()
    return resp.read()


def see_analytics(hashed):
    ''' view analytics for the link /hashed '''
    h = httplib.HTTPConnection(SERVER)
    h.request('GET', 'http://'+SERVER+'/data?hash=' + hashed)
    resp = h.getresponse()
    return resp.read()


if __name__ == '__main__':
    print '----------------'
    print 'try to create shortened url with no url parameter:'
    print create_shortened_url({})
    print '----------------'
    print 'cannot create hash shorten'
    print create_shortened_url({'url': 'www.google.com', 'hash': 'shorten'})
    print '-----------------'
    print 'create shortened url to google with hash "g"'
    print create_shortened_url({'url': 'www.google.com', 'hash': 'g'})
    print '----------------'
    print 'try again with same hash - not allowed:'
    print create_shortened_url({'url': 'www.google.com', 'hash': 'g'})
    print '----------------'
    print 'try with no hash:'
    print create_shortened_url({'url': 'www.google.com'})
    print '----------------'
    print 'now visit /g and get a 301:'
    print visit_url('g')
    print '----------------'
    print 'visit a wrong code'
    print visit_url('asdf')
    print 'see count at /g'
    print see_analytics('g')
    print 'now visit g once, see increase'
    visit_url('g')
    print see_analytics('g')
