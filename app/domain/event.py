from datetime import datetime
class Event:
    def __init__(
        self,
        id,
        title,
        description,
        organizer_id,
        organizing_for,
        event_start_datetime,
        event_end_datetime,
        no_of_participants_allowed,
        slug,
        organizer_name='organizer',
        status='scheduled',
        created_at=datetime.utcnow(),
    ):
        if not id or not title or not organizer_id or not organizer_name or not organizing_for or not event_start_datetime or not event_end_datetime or not slug:
            raise ValueError("Missing required fields for Event")
        if not isinstance(title, str) or not isinstance(description, str) or not isinstance(organizer_id, str) or not isinstance(organizer_name, str):
            raise ValueError("title, description, organizer_id and organizer_name must be strings")
        self.id = id
        self.title = title
        self.description = description
        self.organizer_id = organizer_id
        self.organizer_name = organizer_name
        self.organizing_for = organizing_for
        self.event_start_datetime = event_start_datetime
        self.event_end_datetime = event_end_datetime
        self.no_of_participants_allowed = no_of_participants_allowed
        self.status = status 
        self.slug = slug
        self.created_at = created_at or datetime.utcnow()

    def update_event(
        self,
        title=None,
        description=None,
        organizer_name=None,
        organizing_for=None,
        event_start_datetime=None,
        event_end_datetime=None,
        no_of_participants_allowed=None,
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
        if no_of_participants_allowed is not None:
            self.no_of_participants_allowed = no_of_participants_allowed
    