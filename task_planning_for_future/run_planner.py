from datetime import datetime, timedelta
from .models import TaskPlan

# dummy db session
db_session = None

# 9:00 get for next 30 minutes
# 9:25 get for next 30 minutes
# keep 5 minutes between run_planned_tasks, so you will not miss anthing in between


def publish_task(task_type, kwargs):
    pass


# cron job, every 25 minutes
def run_planned_tasks():
    # in prod is better to use datetime.utcnow()
    now = datetime.now()
    to_time_period = now + timedelta(minutes=30)

    planned_tasks = (
        db_session.query(TaskPlan)
        .filter(
            TaskPlan.active.is_(True),
            TaskPlan.execution_date.between(now, to_time_period),
        )
        .all()
    )

    for pt in planned_tasks:
        publish_task(pt.task_type, pt.kwargs)
