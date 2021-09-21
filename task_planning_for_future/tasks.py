from .models import TaskPlan


def send_feedback_email_to_customer(task_plan: TaskPlan):
    customer_email = task_plan.kwargs["customer_email"]
    print(f"Email is sent to customer {customer_email}")


def send_confirmation_email_for_host(task_plan: TaskPlan):
    host_email = task_plan.kwargs["host_email"]
    print(f"Email is sent to host {host_email}")
