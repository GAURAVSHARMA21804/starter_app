from Database.init_and_conf import db
from datetime import datetime
import pytz




############################# companies all Starter_operators Info ########################################

class User_info(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    mobile_no=db.Column(db.String(15), unique=True, nullable=False)
    username=db.Column(db.String(50), nullable=False)
    date_of_birth=db.Column(db.Date, nullable=True)
    password=db.Column(db.String(14), nullable=True, default=None)
    created_date_time=db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))


class Unregister_user(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    mobile_no = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    password = db.Column(db.String(14), nullable=True, default=None)
    otp = db.Column(db.String(6), nullable=False)
    is_registered = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    
###################################### Device registrations #######################################3 
class DeviceSales(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    ServTimeStemp = db.Column(db.DateTime, default=datetime.utcnow)
    buyer_mobile = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(length=50),nullable=False)
    device_id = db.Column(db.String(length=40),nullable=False)
    buyer_name = db.Column(db.String(length=40),nullable=False)
    dealer_name = db.Column(db.String(length=40),nullable=False)
    city = db.Column(db.String(length=50),nullable=True)
    
class Unregister_device(db.Model):
    did = db.Column(db.Integer, primary_key=True)
    ServTimeStemp = db.Column(db.DateTime, default=datetime.utcnow)
    user_mobile = db.Column(db.String(50), nullable=False)
    buyer_mobile = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(length=50),nullable=False)
    device_id = db.Column(db.String(length=40),nullable=False)
    device_name = db.Column(db.String(length=40),nullable=True)
    otp = db.Column(db.Integer,nullable=False)
    
class Device_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(length=50),nullable=False)
    device_id = db.Column(db.String(length=40),unique=True)
    device_name = db.Column(db.String(length=40),nullable=True)
    # vehicle_number = db.Column(db.String(length=40),nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    deregistred_on = db.Column(db.DateTime,nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    is_connected = db.Column(db.Boolean, default=False)
    is_configured = db.Column(db.Boolean, default=False)
    # firmware_ver = db.Column(db.String(length=10))
    last_seen = db.Column(db.DateTime, default=None)
    no_of_subs = db.Column(db.Integer)
    subs_limit = db.Column(db.Integer)
    # config_id = db.Column(db.Integer, db.ForeignKey('devconfig.config_id'))
    
class Subscribers_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(length=40), db.ForeignKey('device_info.device_id'), nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), nullable=False)
    subscriber_mobile_no = db.Column(db.String(length=40), nullable=False)
    is_subscripted = db.Column(db.Boolean, default=False)

    # Define relationships (optional, but useful for easier access)
    device = db.relationship('Device_info', backref=db.backref('subscribers', lazy=True))
    user = db.relationship('User_info', backref=db.backref('subscribers', lazy=True),
                            foreign_keys=[subscriber_id, subscriber_mobile_no])

    
    
    


