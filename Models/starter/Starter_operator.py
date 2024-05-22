from flask import request, jsonify, session, current_app
import pytz
from Database.init_and_conf import db
from Database.models import  Unregister_user,User_info,DeviceSales,Unregister_device,Device_info,Subscribers_info
# from handlers import create_tocken
from Config.token_handler import TokenRequirements
import error.errors as error
from datetime import datetime, timedelta
# from Services.AWS_S3 import return_s3_client
# from Config.cred import DevConfig
# from os import path

###seralize method 



########################################### registration api ###############################3
def Starter_operator_register(data):
    try:
        mobile_no = data.get('mobile_no')
        username = data.get('username')
        date_of_birth = data.get('date_of_birth')
        
        otp='123456'
        if mobile_no is None and len(mobile_no)!=10:
            return error.INVALID_INPUT_422
        if username is None:
            return error.INVALID_INPUT_422
        user = None
        user_q = User_info.query.filter_by(mobile_no=mobile_no).first()
        if user_q is not None:
            return error.ALREADY_EXIST
        else:
            
            user = Unregister_user.query.filter_by(mobile_no=mobile_no,username=username).first()
            if user is not None:
                user.otp = otp
            else:
                # Only include dob in User creation if it exists in the request form
                user_data = {'mobile_no': mobile_no, 'username': username, 'otp': otp}
                if date_of_birth:
                    user_data['date_of_birth'] = datetime.strptime(date_of_birth, '%d-%m-%Y').date()

                user = Unregister_user(**user_data)
                db.session.add(user)
        
            db.session.commit()
            return jsonify({'otp sent succesfully ': otp}), 200
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
    
################################################## verify otp and set password ####################3
    
def verify_otp_and_set_password(data):
    try:
        mode = data.get('mode')
        mobile_no =data.get('mobile_no')
        otp=data.get('otp')
        password=data.get('password')
        confirm_password=data.get('confirm_password')
        if mode == 'register':
            user = Unregister_user.query.filter_by(mobile_no=mobile_no).first()
            if user is not None:
                if user.otp == otp:
                    if password != confirm_password:
                        return jsonify({'message':'password is not mached '}),400
                    else:
                        user.password = password
                        user.is_registered = True
                        db.session.commit()
                        if user.is_registered == True:
                            user_data = {'mobile_no': mobile_no, 'username': user.username, 'date_of_birth':user.date_of_birth,'password':user.password}
                            
                            user = User_info(**user_data)
                            db.session.add(user)
                            Unregister_user.query.filter_by(mobile_no=mobile_no).delete()
                        db.session.commit()
                        return jsonify({'message':'user is register successfully'}),200
            
            
                        
                else:
                    return error.INVALID_OTP_422
            else:
                return error.DOES_NOT_EXIST
        elif mode=='change_password':
            unr_user = Unregister_user.query.filter_by(mobile_no=mobile_no).first()
            if unr_user is None:
                print("user does not exist")
                return error.INVALID_INPUT_422
            if str(unr_user.otp) != str(otp) :
                print("otp missmatch")
                return error.INVALID_OTP_422
            reg_user = User_info.query.filter_by(mobile_no=unr_user.mobile_no).first()
            if reg_user is not None:
                if password != confirm_password:
                    return jsonify({'message':'password is not mached '}),400
                else:
                    reg_user.password = password
                    Unregister_user.query.filter_by(mobile_no=unr_user.mobile_no).delete()
                    db.session.commit()
                    print("Password change success")
                    return {"status": "Password change success!", "mobile": str(reg_user.mobile_no)}
            
            
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
        
 ############################################## login api #############################################
        
def Starter_operator_login(data):
    try:
        mobile_no = data.get('mobile_no')
        password = data.get('password')
        # date = datetime.now().date()
        # time = datetime.now().time()
        if mobile_no is None:
            return error.INVALID_INPUT_422
        if password is None:
            return error.INVALID_INPUT_422
        user = User_info.query.filter_by(mobile_no=mobile_no,password=password).first()
        
        if user is not None:
            if user.password == password:
                session['logged_in'] = True
                token = TokenRequirements.create_token(password = user.password,mobile_no = user.mobile_no, secret_key=current_app.config['SECRET_KEY'])
                return jsonify({'Response': 'User login successfull!', 'token': f'{token}','date_of_birth':f'{user.date_of_birth}','mobile_no':f'{user.mobile_no}','password':f'{user.password}'}), 200
            else:
                return jsonify({'Response:': 'Authentication Failed!'}), 401
        else:
            return jsonify({'Response:': 'User Not Found!'}), 404
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
    
     
##################################### forgot_password api ##################################################################################################
def Starter_operator_forgot_password(data):
    try:
        mobile_no = data.get('mobile_no')
        otp = '123456'
        
        if mobile_no is None or len(mobile_no) != 10:
            return error.INVALID_INPUT_422
        
        user_q = User_info.query.filter_by(mobile_no=mobile_no).first()
        if user_q is None:
            return error.INVALID_USER_422
        
        user = Unregister_user.query.filter_by(mobile_no=mobile_no).first()
        if user is not None:
            user.otp = otp
        else:
            unr_user = Unregister_user(mobile_no=user_q.mobile_no, username=user_q.username, date_of_birth=user_q.date_of_birth, otp=otp)
            db.session.add(unr_user)
        db.session.commit()
        return {"status": "OTP sent successfully to: " + str(user_q.username), "mobile": str(user_q.mobile_no)}
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
    # try:
    #     mobile_no = data.get('mobile_no')
        
        
        
    #     otp='123456'
    #     if mobile_no is None and len(mobile_no)!=10:
    #         return error.INVALID_INPUT_422
        
    #     user = None
    #     user_q = User_info.query.filter_by(mobile_no=mobile_no).first()
    #     if user_q is None:
    #         return error.INVALID_USER_422
    #     else:
    #         user = Unregister_user.query.filter_by(mobile_no=mobile_no).first()
    #         if user is not None:
    #             user.otp = otp
    #         else:
    #             # Only include dob in User creation if it exists in the request form
    #             unr_user = Unregister_user(mobile_no=user_q.mobile_no, username=user_q.username, date_of_birth= user_q.date_of_birth,otp=otp)
    #             db.session.add(unr_user)
    #     db.session.commit()
    #     return {"status": "OTP sent sucsussfully to: " + str(unr_user.username), "mobile": str(unr_user.mobile_no)}
    # except Exception as e:
    #     return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
    
    
#
    
##########################################################################################################################3##########################



  ############################################# set password code #####################  
# def Starter_operator_set_password(data):
#     try:
#         mobile_no= data.get('mobile_no')
#         password = data.get('password')
#         otp= data.get('otp')
        
#         unr_user = Unregister_user.query.filter_by(mobile_no=mobile_no).first()
#         if unr_user is None:
#             print("user does not exist")
#             return error.INVALID_INPUT_422
#         if str(unr_user.otp) != str(otp) :
#             print("otp missmatch")
#             return error.INVALID_OTP_422
#         reg_user = User_info.query.filter_by(mobile_no=unr_user.mobile_no).first()
#         if reg_user is not None:
#             reg_user.password = password
#             Unregister_user.query.filter_by(mobile_no=unr_user.mobile_no).delete()
#             db.session.commit()
#             print("Password change success")
#             return {"status": "Password change success!", "mobile": str(reg_user.mobile_no)}
#     except Exception as e:
#         return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
#######################################################################################################


##################################### device_registration ##################################################
def Starter_operator_device_registration(data):
    try:
        user_mobile = data.get('user_mobile')
        device_type = data.get('device_type')
        device_id = data.get('device_id')
        device_name = data.get('device_name')
        
        otp='123456'
        
        if user_mobile is None and len(user_mobile)!=10:
            return error.UNAUTHORIZED
        if device_type is None:
            return error.INVALID_INPUT_422
        if device_id is None:
            return error.INVALID_DEVICE_ID_422
        if device_name is None:
            return error.INVALID_DEVICE_NAME_422
        user = User_info.query.filter_by(mobile_no=user_mobile).first()
        if user is None:
            return error.INVALID_USER_422
        subscriber = Subscribers_info.query.filter_by(device_id=device_id,subscriber_mobile_no=user_mobile).first()
        if subscriber:
            return error.SUBSCRIBER_EXIST
        # user = None
        device_sale = DeviceSales.query.filter_by(device_id=device_id,device_type=device_type).first()
        if device_sale is None:
            return error.INVALID_SALE_422
        else:
            unr_device = Unregister_device.query.filter_by(device_id=device_id,user_mobile=user_mobile).first()
            if unr_device is not None:
                unr_device.otp = otp
            else:
                # Only include dob in User creation if it exists in the request form
                unr_device = Unregister_device(device_name=device_name,device_type=device_type, device_id=device_id, user_mobile=user_mobile, buyer_mobile=device_sale.buyer_mobile, otp=otp)
                db.session.add(unr_device)
                    
        db.session.commit()
        return {"status": "OTP sent sucsussfully to: " + unr_device.buyer_mobile, "deviceId": device_id, "otp":otp}
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
    
    
def Starter_operator_device_varifiaction(data):
    try:
        device_type= data.get('device_type')
        device_id =data.get('device_id')
        otp=data.get('otp')
        user_mobile=data.get('user_mobile')
        user = User_info.query.filter_by(mobile_no=user_mobile).first()
        subscriber = Subscribers_info.query.filter_by(device_id=device_id,subscriber_mobile_no=user_mobile).first()
        if subscriber:
            return error.SUBSCRIBER_EXIST
        unr_device=Unregister_device.query.filter_by(device_type=device_type,device_id=device_id,user_mobile=user_mobile).first()
        if unr_device is None:
            return error.INVALID_INPUT_422
        if str(unr_device.otp) != str(otp) :
            return error.INVALID_OTP_422
        reg_device=Device_info.query.filter_by(device_type=device_type,device_id=device_id).first()
        # current_user = User_info.query.filter_by(mobile_no=user_mobile).first()
        if reg_device is not None:
            # Unregister_device.query.filter_by(device_type=unr_device.device_type,device_id=unr_device.device_id,user_mobile=unr_device.user_mobile).delete()
            # count = 0
            # for users in reg_device.no_of_subs:
            
            #     count +=1
            if reg_device.no_of_subs is None:
                reg_device.no_of_subs = 0  # Initialize if Non
            if reg_device.no_of_subs>=reg_device.subs_limit:
                return error.LIMIT_REACHED_409
            reg_device.no_of_subs += 1
            
            subscriber_info = Subscribers_info(
                device_id=reg_device.device_id,
                subscriber_id=user.user_id,
                subscriber_mobile_no=user_mobile,
                is_subscripted=True
            )
            db.session.add(subscriber_info)
            
            Unregister_device.query.filter_by(device_type=unr_device.device_type, device_id=unr_device.device_id, user_mobile=unr_device.user_mobile).delete()
            db.session.commit()
            return {"status": "Device registration success!","Device_Id": str(reg_device.device_id)}
        reg_device =Device_info(device_name = unr_device.device_name , device_type=unr_device.device_type,device_id=unr_device.device_id, is_active = True,subs_limit =5,no_of_subs=1)
        subscriber_info = Subscribers_info(
                device_id=reg_device.device_id,
                subscriber_id=user.user_id,
                subscriber_mobile_no=user_mobile,
                is_subscripted=True
            )
       
        
        db.session.add(reg_device)
        db.session.add(subscriber_info)
        Unregister_device.query.filter_by(device_id=unr_device.device_id,device_type=unr_device.device_type,user_mobile=unr_device.user_mobile).delete()
        db.session.commit()
        return {"status": "Device registration success!"}
        
        
            
    except Exception as e:
        return jsonify({'Error': f'Block is not able to execute successfully {e}'}), 422
