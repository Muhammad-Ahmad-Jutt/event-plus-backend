from flask import request, current_app
from flask_socketio import join_room, leave_room, emit
from flask_jwt_extended import decode_token
from app.extensions import socketio, convert_dict_to_json,get_current_user_name
from app.services.event_service import EventService
from app.services.qa_service import QAService
from app.services.authentication_service import AuthService
from app.domain.question import Question
connected_users = {}

@socketio.on('connect')
def handle_connect():
    
    token = request.args.get('token')
    room_id = request.args.get('room_id')

    if not token or not room_id:
        return False  # Reject connection

    try:
        user_identity = decode_token(token)['sub']
        event = current_app.event_service.event_repository.get_by_room_id(room_id)
        if not event:
            print("Event not found for room_id:", room_id)
            return False  # Reject connection
    except Exception as e:
        print("Invalid token:", e)
        return False

    join_room(room_id)
    connected_users[request.sid] = {
        'user_id': user_identity,
        'room_id': room_id
    }
    user_name = get_current_user_name(user_identity)
    emit('status', {'message': f'User {user_name} connected to room {room_id}'}, room=room_id)

@socketio.on('disconnect')
def handle_disconnect():
    info = connected_users.pop(request.sid, None)
    user_name = get_current_user_name(info['user_id']) if info else "Unknown User"
    if info:
        leave_room(info['room_id'])

@socketio.on('message')
def handle_message(data):
    info = connected_users.get(request.sid)
    if not info:
        return
    room_id = info['room_id']
    user_name = get_current_user_name(info['user_id'])
    emit('message', {'user': user_name, 'message': data['message']}, room=room_id)

@socketio.on('create_question')
def handle_create_question(data):
    info = connected_users.get(request.sid)
    if not info:
        return
    data["room_id"] = info['room_id']
    data["organizer_id"]=info['user_id']

    # Process the question creation logic here
    print(f"Received question creation request in room: {data}")
    question_id, user_email = current_app.qa_service.save_question(question=data)

    # emit_question_data = {'user': user_email, 'question': data['text'],'question_id': question_id, 'room_id': info['room_id']}
    # print(f"Emitting question creation to room {info['room_id']}: {emit_question_data}")
    emit(
    "receive_question",   # 👈 event name (you choose this)
    {
        'user': user_email,
        'question': data['text'],
        'question_id': question_id
    },
    room=info['room_id']
)
@socketio.on('submit_answer')
def handle_submit_answer(data):
    info = connected_users.get(request.sid)
    if not info:
        return
    data["room_id"] = info['room_id']
    question_id = data['question_id']  
    answer_id, user_email = current_app.qa_service.save_answer({
        "room_id": data["room_id"],
        "question_id": question_id,
        "participant_id": request.sid,
        "answer_text": data['answer_text']
    })
    user_name = get_current_user_name(info['user_id'])
    emit('answer_submitted', {'user': user_name, 'answer': data['answer_text']}, room=data['room_id']) 