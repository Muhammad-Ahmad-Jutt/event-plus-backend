from datetime import datetime
class Event:

    def __init__(
        self,
        id,
        title,
        organizer_id,
        description=None,
        event_start_datetime=None,
        event_end_datetime=None,
        organizer_name=None,
        organizing_for=None,
        no_of_participants_allowed=None,
        room_id=None,
        slug=None,
        status=None,
        questionnaire=None
    ):
        if not id or not title or not organizer_id:
            raise ValueError("Missing required fields for Event")

        self.id = id
        self.title = title
        self.description = description
        self.event_start_datetime = event_start_datetime
        self.event_end_datetime = event_end_datetime
        self.organizer_id = organizer_id
        self.organizer_name = organizer_name
        self.organizing_for = organizing_for
        self.no_of_participants_allowed = no_of_participants_allowed
        self.room_id = room_id
        self.slug = slug
        self.status = status
        self.questionnaire = questionnaire

    def update_event(
        self,
        title=None,
        description=None,
        organizer_name=None,
        organizing_for=None,
        event_start_datetime=None,
        event_end_datetime=None,
        no_of_participants_allowed=None,
        room_id=None,
        status=None,
        questionnaire=None

    ):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if organizer_name is not None:
            self.organizer_name = organizer_name
        if organizing_for is not None:
            self.organizing_for = organizing_for
        if event_start_datetime is not None:
            self.event_start_datetime = event_start_datetime
        if event_end_datetime is not None:
            self.event_end_datetime = event_end_datetime
        if room_id is not None:
            self.room_id = room_id
        if status is not None:
            self.status = status
        if no_of_participants_allowed is not None:
            self.no_of_participants_allowed = no_of_participants_allowed
        if questionnaire is not None:
            self.questionnaire = questionnaire