from service_v1.models import (
    user_model,
    user_auth_model,
    order_model,
    product_model
)

# import utility modules
from service_v1.utils.price_convert import rupiah_format
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations


def show_order_controller (header_request) :
    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # admin validation by token
                if not admin_checker (access_token = access_token) :
                    http_status_code, message_response, data_response = show_order(access_token)

                else :
                    http_status_code : int = 403
                    message_response : str =  "Maaf, kamu bukan user."
                    data_response    : dict = {}

            else :
                http_status_code : int = 403
                message_response : str =  "Token salah atau tidak tersedia."
                data_response    : dict = {}

        else :
            http_status_code : int = 400
            message_response : str =  "Token telah kadaluarsa."
            data_response    : dict = {}

    else :
        http_status_code : int = 403
        message_response : str =  "Header 'Token' tidak tersedia"
        data_response    : dict = {}

    return http_status_code, message_response, data_response


def show_order (access_token) : 
    # Response view
    response_view : list = []

    # Get Order Data
    # order_datas : list = order_model.objects.filter(status = "pending").values()
    order_datas : list = list(order_model.objects.filter(
        user = user_auth_model.objects.get(access_token = access_token).user,
        status = "pending"
    ).values())[::-1]

    # Order Data Filterization
    for order_data in order_datas :
        customer_data : user_model = user_model.objects.get(
            id = user_auth_model.objects.get(
                access_token = access_token
            ).user_id
        )

        # Get Product Data
        product_data : product_model = product_model.objects \
            .get(id = order_data.get('product_id'))

        # Data Order
        data_order : dict = {}

        # User Data
        data_order['username'] = customer_data.username
        data_order['email']    = customer_data.email

        # Product Data
        data_order['product_name']  = product_data.product_name
        data_order['product_price'] = rupiah_format(product_data.product_price, True)
        data_order['product_url']   = product_data.product_url

        # Order Data
        data_order['order_quantity'] = order_data.get('order_quantity')
        data_order['order_price_total'] = rupiah_format(
            order_data.get('order_quantity') * product_data.product_price, True)

        data_order['order_date']   = order_data.get('order_date')
        data_order['order_status'] = order_data.get('status')

        response_view.append(data_order)


    message_response : str  = "berhasil menampilkan order"
    http_status_code : int  = 200
    data_response    : dict = response_view

    return http_status_code, message_response, data_response


def admin_checker (access_token : str) -> bool :
    get_auth_data = user_auth_model.objects.get(access_token = access_token)
    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin