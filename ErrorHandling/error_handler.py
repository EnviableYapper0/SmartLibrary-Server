from flask import jsonify


def error_handler(error, status_code=500):
    exceptional_return = jsonify(message=str(error))
    exceptional_return.status_code = status_code
    return exceptional_return


def custom_message_error_handler(error, message="Internal Server Error. Please contact staff.", status_code=500):
    exceptional_return = jsonify(message=message)
    exceptional_return.status_code = status_code
    return exceptional_return


def index_error_handler(error):
    return error_handler(error, 409)


def does_not_exist(error):
    return custom_message_error_handler(error, "The requested resource does not exist.", 404)


def rule_error_handler(error):
    return error_handler(error, 403)
