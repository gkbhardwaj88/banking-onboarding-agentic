from backend.db.session import SessionLocal
from backend.db.models.kyc_session import KYCSession

class KYCRepo:
    def create(self, user_id, status):
        db = SessionLocal()
        rec = KYCSession(user_id=user_id, status=status)
        db.add(rec)
        db.commit()
        return rec
