class KYCState:
    def __init__(self):
        self.user_id=None
        self.aadhaar_data=None
        self.pan_data=None
        self.ocr_text=None
        self.pan_ocr_text=None
        self.selfie_frames=[]
        self.liveness=None
        self.form=None
        self.account=None
        self.payment=None
        # raw uploads
        self.aadhaar_bytes=None
        self.pan_bytes=None
        self.validation_ok=None

    def to_response(self):
        """
        Return a JSON-serialisable view, dropping raw bytes and selfie frame blobs.
        """
        safe = {}
        for k, v in self.__dict__.items():
            if k in ("aadhaar_bytes", "pan_bytes", "selfie_frames"):
                continue
            safe[k] = v
        return safe
