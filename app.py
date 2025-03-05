from flask import Flask,request,jsonify
from services import LeaveRequestService
from models import db,LeaveRequest
from datetime import datetime, timedelta

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///leave_requests.db'
db.init_app(app)

with app.app_context():
    db.create_all()

leave_request_service=LeaveRequestService()

@app.route('/api/v1/leave-requests',methods=['POST'])
def create_leave_request():
    data= request.get_json()
    employee_id= data['employee_id']
    start_date= datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    leave_type = data['leave_type']
    reason = data['reason']

    try:
        leave_request= leave_request_service.create_leave_request(employee_id,start_date,end_date,leave_type,reason)
        db.session.add(leave_request)
        db.session.commit()
        return jsonify({'id':leave_request.id}),201
    except ValueError as e:
        return jsonify({'error':'VALIDATION_ERROR', 'message':str(e)}),400
    


@app.route('/api/v1/leave-requests/<employee_id>',methods=['GET'])
def get_employee_leave_requests(employee_id):

    leave_request = leave_request_service.get_employee_leave_requests(employee_id)
    return jsonify([{'id': lr.id, 'employee_id': lr.employee_id, 'start_date': lr.start_date.isoformat(),
    'end_date': lr.end_date.isoformat(), 'leave_type': lr.leave_type, 'reason': lr.reason,
    'status': lr.status, 'working_days': lr.working_days, 'created_at': lr.created_at.isoformat()}
    for lr in leave_request])

if __name__ == '__main__':
    app.run(debug=True)
