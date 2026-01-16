import random
import hashlib

OTP_TTL = 300
MAX_ATTEMPTS = 5
RESEND_COOLDOWN = 60


def _otp_key(email):
	return f"otp:{email}"

def _attempts_key(email):
    return f"otp_attempts:{email}"
    
def _resend_key(email):
    return f"otp_resend:{email}"
    
    
def generate_otp():
    return str(random.randint(100000, 999999))
   
def can_resend(redis, email):
    if redis.exists(_resend_key(email)):
        return False
    
    redis.setex(_resend_key(email), RESEND_COOLDOWN, 1)
    return True
    
def save_otp(redis, email, otp):
    hashed = hashlib.sha256(otp.encode()).hexdigest()
    redis.setex(_otp_key(email), OTP_TTL, hashed)
    redis.setex(_attempts_key(email), OTP_TTL, 0)
    
def redis_verify_otp(redis, email, user_otp):
    stored = redis.get(_otp_key(email))
    
    if not stored:
        return False ,"OTP Expired"
        
    attempts = int(redis.get(_attempts_key(email)) or 0)
    if attempts >= MAX_ATTEMPTS:
        return False, "Too many attempts"

    hashed = hashlib.sha256(user_otp.encode()).hexdigest()
    if hashed != stored:
        redis.incr(_attempts_key(email))
        redis.expire(_attempts_key(email), OTP_TTL) 
        return False, "Invalid OTP"

    redis.delete(_otp_key(email))
    redis.delete(_attempts_key(email))
    return True, "Verified"