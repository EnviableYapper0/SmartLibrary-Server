from flask import jsonify


def bad_input_handler(error, status_code = 400):
    response_content = {'message': str(error)}
    exceptional_return = jsonify(response_content)
    exceptional_return.status_code = status_code
    return exceptional_return


def index_error_handler(error):
    return bad_input_handler(error, 409)


def does_not_exist(error):
    return bad_input_handler(error, 404)


def rule_error_handler(error):
    return bad_input_handler(error, 403)
