from models import LeaveRequest
from datetime import timedelta

class LeaveRequestService:
    def create_leave_request(self,employee_id,start_date,end_date,leave_type,reason):
        if end_date<=start_date:
            raise ValueError("end date must be after start date")
        if (end_date-start_date).days>14:
            raise ValueError("maximum consecutive leave days exceed")
        leave_request=LeaveRequest(employee_id,start_date,end_date,leave_type,reason)
        return leave_request
    
    def get_employee_leave_requests(self,employee_id):
        leave_requests = LeaveRequest.query.filter_by(employee_id=employee_id).all()
        return leave_requests