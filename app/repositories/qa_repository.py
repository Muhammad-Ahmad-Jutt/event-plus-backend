
from app.domain.question import Question
from app.domain.answer import Answer
from boto3.dynamodb.conditions import Key


class QARepository:
    def __init__(self, dynamodb, table_name):
        self.table = dynamodb.Table(table_name)

    def save_question(self, question):
        item = {
            "PK": f"ROOM#{question['room_id']}",
            "SK": f"QUESTION#{question['id']}",
            "organizer_id": question['organizer_id'],
            "text": question['text'],
            "type": question['type'],
            "options": question['options'],
            "correct_answer": question['correct_answer']
        }
        self.table.put_item(Item=item)
        return question['id']

    def save_answer(self, answer: Answer):
        
        item = {
            "PK": f"QUESTION#{answer['question_id']}",
            "SK": f"ANSWER#{answer['id']}",
            "participant_id": answer['participant_id'],
            "text": answer['answer_text'],
            "submitted_at": answer['submitted_at']
        }
        self.table.put_item(Item=item)
        return answer['id']
    def get_question_by_id(self, room_id, question_id):

        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f"ROOM#{room_id}") & Key("SK").eq(f"QUESTION#{question_id}")
        )
        items = response.get("Items", [])
        if not items:
            return None
        item = items[0]
        return Question(
            id=item["SK"].split("#")[1],
            organizer_id=item["organizer_id"],
            room_id=item["PK"].split("#")[1],
            text=item["text"],
            type=item["type"],
            options=item.get("options", []),
            correct_answer=item.get("correct_answer")
        )
    def get_answers_by_question_id(self, question_id):
        response = self.table.query(
            KeyConditionExpression=Key("SK").begins_with(f"ANSWER#") & Key("PK").eq(f"QUESTION#{question_id}")
        )
        items = response.get("Items", [])
        answers = []
        for item in items:
            answers.append(Answer(
                id=item["SK"].split("#")[1],
                question_id=item["PK"].split("#")[1],
                participant_id=item["participant_id"],
                answer_text=item["text"],
                submitted_at=item["submitted_at"],
            ))
        return answers