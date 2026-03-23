from boto3.dynamodb.conditions import Key
from app.domain.event import Event
from datetime import datetime
from app.extensions import parse_event_datetime, serialize_datetime
from app.extensions import safe_parse_iso
class EventRepository:

    def __init__(self, dynamodb, table_name):
        self.table = dynamodb.Table(table_name)

    def _map_item_to_event(self, item):
        return Event(
            id=item["PK"].split("#")[1],
            title=item.get("title"),
            description=item.get("description") or "",
            event_start_datetime=parse_event_datetime(item["event_start_datetime"]) if item.get("event_start_datetime") else None,
            event_end_datetime=parse_event_datetime(item["event_end_datetime"]) if item.get("event_end_datetime") else None,
            organizer_id=item.get("organizer_id"),
            organizer_name=item.get("organizer_name") or "organizer",
            organizing_for=item.get("organizing_for") or "self",
            no_of_participants_allowed=int(item.get("no_of_participants_allowed", 10)),
            room_id=item.get("room_id"),
            slug=item.get("slug") or "",
            status=item.get("status") or "scheduled"
        )
    def save(self, event: Event):
        item = {
            "PK": f"EVENT#{event.id}",
            "SK": "DETAILS",
            "title": event.title,
            "description": event.description,
            "event_start_datetime": parse_event_datetime(event.event_start_datetime),
            "event_end_datetime": parse_event_datetime(event.event_end_datetime),
            "organizer_id": event.organizer_id,
            "slug": event.slug,
            "no_of_participants_allowed": event.no_of_participants_allowed,
            "organizer_name": event.organizer_name,
            "status": event.status,
            "room_id": event.room_id,
            "organizing_for": event.organizing_for        }

        # remove None values
        item = {k: v for k, v in item.items() if v is not None}

        self.table.put_item(Item=item)

    # def get_by_organizer_email(self, organizer_email):
    #     response = self.table.query(
    #         IndexName="organizer-index",
    #         KeyConditionExpression=Key("organizer_email").eq(organizer_email)
    #     )
    #     items = response.get("Items", [])
    #     return [
    #         Event(
    #             id=item["PK"].split("#")[1],
    #             title=item["title"],
    #             description=item.get("description"),
    #             event_start_datetime=item.get("event_start_datetime"),
    #             event_end_datetime=item.get("event_end_datetime"),
    #             organizer_email=item.get("organizer_email"),
    #         )
    #         for item in items
    #     ]

    def get_by_id(self, event_id):
        item = self.table.get_item(Key={"PK": f"EVENT#{event_id}", "SK": "DETAILS"}).get("Item")
        if not item:
            return None
        return self._map_item_to_event(item)
    def get_events_by_organizer_id(self, organizer_id):
        response = self.table.query(
            IndexName="organizer-index",
            KeyConditionExpression=Key("organizer_id").eq(organizer_id)
        )

        items = response.get("Items", [])

        return [self._map_item_to_event(item) for item in items]
    def delete_event(self, event_id):
        self.table.delete_item(Key={"PK": f"EVENT#{event_id}", "SK": "DETAILS"})

    def update_status(self, event_id, status):
        self.table.update_item(
            Key={"PK": f"EVENT#{event_id}", "SK": "DETAILS"},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": status}
        )

    def get_by_slug(self, slug):
        response = self.table.query(
            IndexName="slug-index",
            KeyConditionExpression=Key("slug").eq(slug)
        )
        items = response.get("Items")
        if not items:
            return None
        item = items[0]
        return self._map_item_to_event(item)

    def get_by_title_and_id(self, title, organizer_id):
        # Use a composite filter if title is not the partition key
        response = self.table.query(
            IndexName="title-organizerid-index",
            KeyConditionExpression=Key("title").eq(title) & Key("organizer_id").eq(organizer_id)
        )
        items = response.get("Items")
        if not items:
            return False
        else:
            return True
    def get_by_room_id(self, room_id):
        response = self.table.query(
            IndexName="room-id-index",
            KeyConditionExpression=Key("room_id").eq(room_id)
        )
        items = response.get("Items")
        if not items:
            return None
        item = items[0]
        return self._map_item_to_event(item)
    def update_room_id(self, event_id, room_id):
        self.table.update_item(
            Key={"PK": f"EVENT#{event_id}", "SK": "DETAILS"},
            UpdateExpression="SET room_id = :r",
            ExpressionAttributeValues={":r": room_id}
        )
