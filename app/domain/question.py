class Question:
    def __init__(self, id, organizer_id, text, type,event_id=None, options=None, correct_answer=None):
        self.id = id  # unique question_id
        self.organizer_id = organizer_id
        self.event_id = event_id
        self.text = text
        self.type = type
        self.options = options or []
        self.correct_answer = correct_answer