import random
import hashlib

def _otp_key(email):
	return f"otp:{email}"