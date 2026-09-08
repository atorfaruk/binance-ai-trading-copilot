from .trade_proposal import calculate_fingerprint
class ApprovalError(ValueError): pass
class HumanApprovalGate:
    def __init__(self): self._approved_fingerprint=None
    def request(self,proposal,response):
        current=calculate_fingerprint(proposal)
        if proposal.fingerprint!=current: raise ApprovalError("proposal fingerprint is invalid or stale")
        if response.strip()!="YES": self._approved_fingerprint=None; return False
        self._approved_fingerprint=current; return True
    def is_approved(self,proposal):
        current=calculate_fingerprint(proposal)
        return self._approved_fingerprint==current and proposal.fingerprint==current
    def clear(self): self._approved_fingerprint=None
