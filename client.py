import httplib
import json

# use this server for dev
SERVER = 'localhost:5000'

SERVER = 'shortenit.elasticbeanstalk.com'

# use this server for prod, once it's on ec2
# SERVER = 'xxxxx.aws.ec2.com:5000'


def create_shortened_url(data):
    ''' connect to webapp and create a shortened url '''
    h = httplib.HTTPConnection(SERVER)
    data = json.dumps(data)
    print 'POST http://'+SERVER+'/shorten', data
    h.request('POST', 'http://'+SERVER+'/shorten', body=data)
    resp = h.getresponse()
    return resp.read()


def visit_url(hashed):
    ''' visit /hashed '''
    h = httplib.HTTPConnection(SERVER)
    print 'GET http://'+SERVER+'/' + hashed
    h.request('GET', 'http://'+SERVER+'/' + hashed)
    resp = h.getresponse()
    return resp.read()


def print_analytics(hashed):
    ''' view analytics for the link /hashed '''
    h = httplib.HTTPConnection(SERVER)
    print 'GET http://'+SERVER+'/data?hash=' + hashed
    h.request('GET', 'http://'+SERVER+'/data?hash=' + hashed)
    resp = h.getresponse()
    print resp.read()
    print 'GET', 'http://'+SERVER+'/data/browsers?hash=' + hashed
    h.request('GET', 'http://'+SERVER+'/data/browsers?hash=' + hashed)
    resp = h.getresponse()
    print resp.read()


if __name__ == '__main__':
    print 'Shorten-It is a URL shortener which allows users to create shorter'
    print 'urls. It then provides analytics for who visits this redirect link.'
    print ''
    print 'The endpoint for creating a shortened url is POST /shorten'
    print 'This takes argument url and optional argument hash. url is the '
    print 'long url you wish to shorten. If you wish to define what the shortened'
    print 'url looks like (shortenit.elasticbeanstalk.com/HASH - admittedly not'
    print 'very short) you can provide'
    print 'a hash argument. There are useful error messages if arguments are '
    print 'not provided.'
    print '----------------'
    print 'try to create shortened url with no url parameter:'
    print create_shortened_url({})
    print '----------------'
    print 'cannot create hash shorten as it is an endpoint already:'
    print create_shortened_url({'url': 'www.google.com', 'hash': 'shorten'})
    print '-----------------'
    print 'create shortened url with no hash'
    print create_shortened_url({'url': 'www.google.com'})
    print '----------------'
    print 'try to create shortened url with hash "g" - already exisits'
    print create_shortened_url({'url': 'www.google.com', 'hash': 'g'})
    print '----------------'
    print 'Now other endpoints are defined by the created hashes. For example:'
    print 'now visit /g and get a 301:'
    print visit_url('g')
    print '----------------'
    print 'visit a wrong code and get an error message'
    print visit_url('asdf')
    print '----------------'
    print 'The other endpoints are analytics endpoints.'
    print '/data returns the number of visits there have been to a shortened url'
    print 'while /data/browsers shows the breakdown by browsers.'
    print 'Future analytics are in the pipelin'
    print '----------------'
    print 'see count at /g'
    print_analytics('g')
    print 'now visit g once, see increase'
    visit_url('g')
    print_analytics('g')
