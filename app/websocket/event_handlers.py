from flask import request, current_app
from flask_socketio import join_room, leave_room, emit
from flask_jwt_extended import decode_token
from app.extensions import socketio
from app.services.event_service import EventService
from app.services.qa_service import QAService
from app.services.authentication_service import AuthService
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

    emit('status', {'message': f'User {user_identity} connected to room {room_id}'}, room=room_id)
    print(f"{user_identity} connected to {room_id}")

@socketio.on('disconnect')
def handle_disconnect():
    info = connected_users.pop(request.sid, None)
    if info:
        leave_room(info['room_id'])
        print(f"User {info['user_id']} disconnected from room {info['room_id']}")

@socketio.on('message')
def handle_message(data):
    info = connected_users.get(request.sid)
    if not info:
        return
    room_id = info['room_id']
    print(f"Emitting message to room {room_id}: {data['message']}")
    emit('message', {'user': info['user_id'], 'message': data['message']}, room=room_id)

@socketio.on('create_question')
def handle_create_question(data):
    info = connected_users.get(request.sid)
    if not info:
        return
    room_id = info['room_id']
    data["organizer_id"]=info['user_id']
    # Process the question creation logic here

    question_id, user_email = QAService.save_question(data['question'])
    print(f"User {user_email} created a question in room {room_id}: {data['question']}")
    emit('question_created', {'user': user_email, 'question': data['question']}, room=room_id)

@socketio.on('submit_answer')
def handle_submit_answer(data):
    info = connected_users.get(request.sid)
    if not info:
        return
    room_id = info['room_id']
    question_id = data['question_id']  
    answer_id, user_email = QAService.save_answer({
        "room_id": room_id,
        "question_id": question_id,
        "participant_id": info['user_id'],
        "answer_text": data['answer']
    })
    print(f"User {user_email} submitted an answer in room {room_id}: {data['answer']}")
    emit('answer_submitted', {'user': user_email, 'answer': data['answer']}, room=room_id) 