import httplib2
import urllib
import json
import re


class BadRequest(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class API(object):
    def __init__(self, username, password, **kwargs):
        """ Authenticate with your HeyWatch credentials
            hw = heywatch.API(user, passwd)

            kwargs are any valid arguments passed to httplib2.Http contructor
        """
        self.url = 'https://heywatch.com'
        self.cli = httplib2.Http(**kwargs)
        self.cli.add_credentials(username, password)

        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'HeyWatch py/1.0.1',
        }

        self.account()

    def account(self):
        """ Get account information
            hw.account()
        """
        return self.request('/account')

    def info(self, resource, id):
        """ Get info about a given resource and id
            hw.info('format', 31)
        """
        return self.request('/' + resource + '/' + str(id))

    def jpg(self, id, **params):
        """ Generate thumbnails in the foreground or background via async=True
            hw.jpg(12345, start=2)
            => thumbnail data

            hw.jpg(12345, async=True, number=6, s3_directive='s3://accesskey:secretkey@bucket')
            => True
        """
        if 'async' in params:
            params.pop('async')
            self.request('/encoded_video/' + str(id) + '/thumbnails', 'POST', body=urllib.urlencode(params))
            return True

        if len(params) > 0:
            params = '?' + urllib.urlencode(params)
        else:
            params = ''

        return self.request('/encoded_video/' + str(id) + '.jpg' + params)

    def bin(self, resource, id):
        """ Get the binary data of a video / encoded_video
            hw.bin('encoded_video', 12345)
        """
        self.cli.follow_redirects = False
        response, content = self.cli.request(self.url + '/' + resource + '/' + str(id) + '.bin', 'GET')
        self.cli.follow_redirects = True
        return self.cli.request(response['location'], 'GET')[1]

    def all(self, resource):
        """ Get all objects from a given resource
            hw.all('video')
            hw.all('job')

            FIXME:
            no filters
        """
        return self.request('/' + resource)

    def count(self, resource):
        """ Count objects from a given resource
            hw.count('encoded_video')
            hw.count('format')

            FIXME:
            no filters
        """
        return len(self.all(resource))

    def create(self, resource, **data):
        """ Create a resource with the give data
            hw.create('download', url='http://site.com/video.mp4', title='testing')
        """
        return self.request('/' + resource, 'POST', body=urllib.urlencode(data))

    def update(self, resource, id, **data):
        """ Update an object by giving its resource and ID
            hw.update('format', 9877, video_bitrate=890)
        """
        self.request('/' + resource + '/' + str(id), 'PUT', body=urllib.urlencode(data))
        return True

    def delete(self, resource, id):
        """ Delete a resource
            hw.delete('format', 9807)
        """
        self.request('/' + resource + '/' + str(id), 'DELETE')
        return True

    def request(self, resource, method='GET', **args):
        params = {'headers': self.headers}
        params.update(args)

        response, content = self.cli.request(self.url + resource, method, **params)

        if re.search('^4|5', response['status']):
            raise BadRequest(response['status'] + " " + content)

        if len(content) > 0 and re.search('json', response['content-type']):
            return json.loads(content)
        else:
            return content
