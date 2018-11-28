from coapthon.resources.resource import Resource
import boto3

class UsersResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(UsersResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = {}

    def render_GET(self, request):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('RFID-Users')
        return self

    def render_POST(self, request):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('RFID-Users')
        res = UsersResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True
