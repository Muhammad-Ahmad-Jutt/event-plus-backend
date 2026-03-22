
from app.domain.answer import Answer
from app.domain.question import Question
import uuid
from app.services.authentication_service import AuthService
class QAService:
    def __init__(self, qa_repository, event_repository):
        self.qa_repository = qa_repository
        self.event_repository = event_repository

    def save_question(self, question):
        if not all([question.room_id, question.organizer_id, question.text, question.type]):
            raise ValueError("Question must have room_id, text and type")
        event = self.event_repository.get_event_by_room_id(question.room_id)
        if not event:
            raise ValueError("Event not found")
        question.id = str(uuid.uuid4())
        question_id = self.qa_repository.save_question(question)
        user_email = self.auth_repository.get_user_by_id(question.organizer_id).email
        return question_id, user_email
    def update_question(self, question_id, updated_fields):
        question = self.qa_repository.get_question_by_id(question_id)
        if not question:
            raise ValueError("Question not found")
        for key, value in updated_fields.items():
            setattr(question, key, value)
        self.qa_repository.save_question(question)
    def save_answer(self, answer):

        if not all([answer.room_id, answer.question_id, answer.participant_id, answer.answer_text]):
            raise ValueError("Answer must have room_id, question_id, participant_id and answer_text")
        event = self.event_repository.get_event_by_room_id(answer.room_id)
        question = self.qa_repository.get_question_by_id(answer.question_id)
        if not event:
            raise ValueError("Event not found")
        if not question:
            raise ValueError("Invalid question_id")
        answer.id = str(uuid.uuid4())
        answer_id = self.qa_repository.save_answer(answer)
        user_email = self.auth_repository.get_user_by_id(answer.participant_id).email
        return answer_id, user_email
    def update_answer(self, question_id, updated_fields):
        # This method would require fetching the answer first, which is not implemented in the repository
        # For simplicity, let's assume we can fetch the answer by its ID (this would require a new method in the repository)
        answers = self.qa_repository.get_answers_by_question_id(question_id)
        if not answers:
            raise ValueError("Answer not found")
        for key, value in updated_fields.items():
            setattr(answers[0], key, value)
        self.qa_repository.save_answer(answers[0])
