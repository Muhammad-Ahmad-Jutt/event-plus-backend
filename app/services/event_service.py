import uuid
from flask_jwt_extended import create_access_token
from app.domain.event import Event
from app.extensions import generate_slug
class EventService:

    def __init__(self, event_repository, user_repository):
        self.event_repository = event_repository
        self.user_repository = user_repository

    def create_event(self, title, description, event_start_datetime,event_end_datetime, organizer_id, organizer_name, organizing_for, no_of_participants_allowed=10):
    
        slug = generate_slug(title)
        if self.event_repository.get_by_title_and_id(title,organizer_id):
            raise ValueError("An event with the same title already exists. Please choose a different title.")
        if title is None or len(str(title)) < 8 or len(str(title)) > 20:
            raise ValueError("Title is required and must be between 8 and 20 characters long")
        if event_start_datetime is None or event_end_datetime is None :
            raise ValueError("Event start datetime and end datetime are required")
        if self.event_repository.get_by_slug(slug):
            raise ValueError("An event with the same title already exists. Please choose a different title.")
        event = Event(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            event_start_datetime=event_start_datetime,
            event_end_datetime=event_end_datetime, # for now we are setting end datetime same as start datetime, we can change it later
            no_of_participants_allowed=no_of_participants_allowed,
            organizer_id=organizer_id,
            organizer_name=organizer_name,
            organizing_for=organizing_for,
            slug=slug
        )
        self.event_repository.save(event)

        return event
    def update_event(
        self,
        event_id,
        title=None,
        description=None,
        status=None,
        event_start_datetime=None,
        event_end_datetime=None,
        no_of_participants_allowed=None,
        room_id=None,
        organizing_for=None
    ):
        # Fetch the event
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        # # Prevent updates on certain statuses
        # if event.status in ['stopped', 'completed', 'running', 'cancelled']:
        #     raise ValueError("Cannot update an event that is stopped, completed, running, or cancelled")

        # Validate title length if provided
        if title is not None and (len(str(title)) < 8 or len(str(title)) > 20):
            raise ValueError("Title must be between 8 and 20 characters long")

        # Handle slug generation if title is provided
        if title is not None:
            slug = generate_slug(title)
            existing_event = self.event_repository.get_by_slug(slug)
            if existing_event and existing_event.id != event_id:
                raise ValueError("An event with the same title already exists. Please choose a different title.")
            event.slug = slug
            event.title = title

        # Dynamically update other fields
        for key, value in {
            'description': description,
            'status': status,
            'event_start_datetime': event_start_datetime,
            'event_end_datetime': event_end_datetime,
            'no_of_participants_allowed': no_of_participants_allowed,
            'room_id': room_id,
            'organizing_for': organizing_for
        }.items():
            if value is not None:
                setattr(event, key, value)

        # Save the updated event
        self.event_repository.save(event)
        return event
    def delete_event(self, event_id, user_id):
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        if event.organizer_id != user_id:
            raise ValueError("Unauthorized")
        if event.status in ['stopped', 'completed', 'cancelled', 'running']:
            raise ValueError("Cannot delete an event that is stopped, completed, running, or cancelled")
        self.event_repository.delete_event(event_id)

    def create_room_for_event(self, event_id):
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        room_id = str(uuid.uuid4())
        return room_id
    def get_event_by_room_id(self, room_id):
        event = self.event_repository.get_by_room_id(room_id)
        if not event:
            raise ValueError("Event not found")
        return event
    def get_events_by_organizer_id(self, organizer_id):
        events = self.event_repository.get_events_by_organizer_id(organizer_id)
        return events
    def by_id(self, event_id):
        event = self.event_repository.get_by_id(event_id)
        return event