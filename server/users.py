from coapthon.resources.resource import Resource
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('RFID-Users')

class UsersResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(UsersResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "test"

    def render_GET(self, request):
        res = table.get_item(
            Key = {
                'UID': request.uri_query
            }
        )
        try:
            self.payload = json.dumps(res['Item'])
        except KeyError:
            self.payload = json.dumps({})
        return self

    def render_POST(self, request):
        res = UsersResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True
