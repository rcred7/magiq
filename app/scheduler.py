from datetime import datetime, timedelta

def suggest_time_slot(existing_tasks, duration_minutes=30):
    now = datetime.now().replace(second=0, microsecond=0)
    future = now + timedelta(days=1)

    # Assume user is available 9 AM to 5 PM today
    slots = [now.replace(hour=h, minute=m) for h in range(9, 17) for m in (0, 30)]

    # Mark used slots
    used = {task.due.replace(second=0, microsecond=0) for task in existing_tasks if task.due}

    for slot in slots:
        if slot not in used and slot > now:
            return slot
    return None