from urllib.parse import unquote

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Alex Laird'
__version__ = '0.1.0'


def set_request_status(request, status_type, message):
    request.session['status'] = {'type': status_type, 'msg': message}


def get_request_status(request, default=None):
    status = request.session.get('status', default)

    if not status:
        status_type = request.COOKIES.get('status_type', None)
        status_msg = request.COOKIES.get('status_msg', None)
        if status_type and status_msg:
            status = {'type': status_type, 'msg': unquote(status_msg)}

    if 'status' in request.session:
        del request.session['status']

    return status


def set_response_status(response, status):
    if status:
        response.set_cookie('status_type', status['type'])
        response.set_cookie('status_msg', status['msg'])


def clear_response_status(response):
    response.delete_cookie(key='status_type')
    response.delete_cookie(key='status_msg')