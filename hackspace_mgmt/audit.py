


from datetime import datetime, timezone
from typing import Any, Optional

from hackspace_mgmt.models import Member, AuditLog, db


def create_audit_log(category: str, event: str, data: Optional[dict[str, Any]]=None, member: Optional[Member]=None, logged_at: Optional[datetime]=None, commit: bool=True):
    if logged_at is None:
        logged_at = datetime.now(timezone.utc)
    
    log = AuditLog(
        logged_at=logged_at,
        category=category,
        event=event,
        member_id=member.id if member else None,
        data=data
    )

    db.session.add(log)
    if commit:
        db.session.commit()