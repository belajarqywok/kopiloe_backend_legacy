import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  

from service_v1.controllers.admin_controllers.register_admin_controller import register_admin_controller

@csrf_exempt
def register_admin_view (request) :

    if request.method == "POST" : 
        loads_body_request = json.loads(

            request.body.decode("utf-8")
        )

        http_status_code, message_response, data_response = register_admin_controller(
            header_request = request.headers,
            body_request = loads_body_request
        )

        if http_status_code == 201 :

            del data_response["password"]
            del data_response["is_admin"]
            del data_response["verified"]
            del data_response["last_login"]

        response = {

            "http_status_code" : http_status_code,
            "message_response" : message_response,
            "data_response"    : data_response
        }

    else :

        http_status_code : int = 400
        
        response = {

            "http_status_code" : http_status_code,
            "message_response" : f"{request.method} method not found!",
            "data_response"    : {}
        }

    return JsonResponse(data = response, status = http_status_code, safe=True)
