import random
import hashlib
import time

OTP_TTL = 300          # 5 minutes
MAX_ATTEMPTS = 5
RESEND_COOLDOWN = 60   # seconds

# In-memory stores
_otp_store = {}
_resend_store = {}

# email -> {
#   hash: str,
#   expires_at: float,
#   attempts: int
# }

def generate_otp():
    return str(random.randint(100000, 999999))


def _is_expired(expires_at):
    return time.time() > expires_at


def can_resend(email):
    entry = _resend_store.get(email)

    if entry and not _is_expired(entry["expires_at"]):
        return False

    _resend_store[email] = {
        "expires_at": time.time() + RESEND_COOLDOWN
    }
    return True


def save_otp(redis, email, otp):
    hashed = hashlib.sha256(otp.encode()).hexdigest()

    _otp_store[email] = {
        "hash": hashed,
        "expires_at": time.time() + OTP_TTL,
        "attempts": 0
    }


def redis_verify_otp(redis, email, user_otp):
    entry = _otp_store.get(email)

    if not entry:
        return False, "OTP expired"

    if _is_expired(entry["expires_at"]):
        _otp_store.pop(email, None)
        return False, "OTP expired"

    if entry["attempts"] >= MAX_ATTEMPTS:
        return False, "Too many attempts"

    hashed = hashlib.sha256(user_otp.encode()).hexdigest()
    if hashed != entry["hash"]:
        entry["attempts"] += 1
        return False, "Invalid OTP"

    # Success → cleanup
    _otp_store.pop(email, None)
    _resend_store.pop(email, None)

    return True, "Verified"
