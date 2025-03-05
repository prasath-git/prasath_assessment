from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class LeaveRequest(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    employee_id = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    leave_type = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="PENDING")
    working_days = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, employee_id, start_date, end_date, leave_type, reason):
        self.id = self.generate_id()
        self.employee_id = employee_id
        self.start_date = start_date
        self.end_date = end_date
        self.leave_type = leave_type
        self.reason = reason
        self.working_days = self.calculate_working_days()

    @staticmethod
    def generate_id():
        last_request = LeaveRequest.query.order_by(LeaveRequest.id.desc()).first()
        if last_request and last_request.id.startswith("LR"):
            last_num = int(last_request.id[2:]) 
            new_id = f"LR{last_num + 1:03d}" 
        else:
            new_id = "LR001"
        return new_id

    def calculate_working_days(self):
        days = (self.end_date - self.start_date).days + 1
        weekends = sum(1 for i in range(days) if (self.start_date + timedelta(days=i)).weekday() >= 5)
        return days - weekends
