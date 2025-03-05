import unittest
from app import app, db
from services import LeaveRequestService

class TestLeaveRequestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] =  True
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///memory'
        db.create_all
        self.leave_request_service=LeaveRequestService()


    def test_create_leave_request(self):
        data={
            "id": "LR001",
            "employee_id": "EMP001",
            "start_date": "2025-03-01",
            "end_date": "2025-03-05",
            "leave_type": "ANNUAL",
            "reason": "Family vacation to visit parents",
            "status": "PENDING",
            "working_days": 3,
            "created_at": "2025-02-11T10:00:00Z"
            }
        response = app.test_client().post('/api/v1/leave-requests',json=data)
