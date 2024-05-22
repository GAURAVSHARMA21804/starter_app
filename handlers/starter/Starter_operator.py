from flask import Blueprint, render_template, request, session, jsonify, make_response, current_app
# from handlers import is_token_expired
from Config.token_handler import TokenRequirements
from datetime import datetime, timedelta
from functools import wraps
# from Database.models import Unregister_user
from Models.starter.Starter_operator import Starter_operator_register,verify_otp_and_set_password,Starter_operator_login,Starter_operator_forgot_password,Starter_operator_device_registration,Starter_operator_device_varifiaction

Starter_operator1=Blueprint('Starter_operator', __name__)



# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'Alert!': 'Token is missing!'})
#         try:
#             payload = is_token_expired(token)
#             # Add the token payload to the kwargs so that it's available to the protected route
#             kwargs['token_payload'] = payload
#             if payload[0] == False:
#                 try:
#                     # Call the original function with the token payload
#                     return func(*args, **kwargs)
#                 except:
#                     return jsonify({"Error:": "An error occurred while trying to excute the function."})
#             else:
#                 return jsonify({'Alert!': 'Token is expired!'})
#         except:
#             return jsonify({'Alert!': 'Invalid Token!'})
#     return decorated

# @Operator1.route('/public/l')
# def public():
#     return 'For Public Operator'

# @Starter_operator1.route('/operator/auth')
# @TokenRequirements.token_required
# def auth(**kwargs):
#     return 'JWT is verified. Welcome to your Dashboard!'

@Starter_operator1.route('/starter_operator/Register', methods=['POST'])
def Starter_operator_register_handler():
    return Starter_operator_register(request.form)

@Starter_operator1.route('/starter_operator/verify_otp_and_set_password',methods=['POST'])
def verify_otp_and_set_password_handler():
    return verify_otp_and_set_password(request.form)

@Starter_operator1.route('/starter_operator/login', methods=['POST'])
def Starter_operator_login_handler():
    return Starter_operator_login(request.form)

@Starter_operator1.route('/starter_operator/forgot_password',methods=['POST'])
def Starter_operator_forogot_handler():
    return Starter_operator_forgot_password(request.form)

# @Starter_operator1.route('/Starter_operator/set_password',methods=['POST'])
# def Starter_operator_set_password_handler():
#     return Starter_operator_set_password(request.form)

@Starter_operator1.route('/starter_operator/device_registration',methods=['POST'])
@TokenRequirements.token_required
def Starter_operator_device_registration_handler(**kwargs):
    return Starter_operator_device_registration(request.form)


@Starter_operator1.route('/starter_operator/device_varifiaction',methods=['POST'])
@TokenRequirements.token_required
def Starter_operator_device_varifiaction_handler(**kwargs):
    return Starter_operator_device_varifiaction(request.form)
