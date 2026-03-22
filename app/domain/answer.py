class Answer:
    def __init__(self, id, question_id, participant_id, answer_text, submitted_at, event_id):
        if not id or not question_id or not participant_id or not answer_text:
            raise ValueError("Missing required fields for Answer")
        self.id = id  # unique answer_id
        self.question_id = question_id
        self.participant_id = participant_id
        self.answer_text = answer_text
        self.submitted_at = submitted_at
        self.event_id = event_id