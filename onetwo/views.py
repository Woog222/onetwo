from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_random_cheering_msg


@api_view(['GET', 'POST'])
def hello(request):
    data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": get_random_cheering_msg()
                    }
                }
            ]
        }
    }
    return Response(data = data)