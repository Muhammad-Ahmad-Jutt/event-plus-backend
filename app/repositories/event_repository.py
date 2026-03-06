from app.domain.event import Event


class EventRepository:

    def __init__(self, dynamodb, table_name):
        self.table = dynamodb.Table(table_name)

    def save(self, event: Event):

        item = {
            "PK": f"EVENT#{event.id}",
            "SK": "DETAILS",
            "name": event.name,
            "description": event.description,
            "event_start_datetime": str(event.event_start_datetime) if event.event_start_datetime else None,
            "event_end_datetime": str(event.event_end_datetime) if event.event_end_datetime else None,
            "organizer_email": event.organizer_email,
            "slug": event.slug,
        }

        self.table.put_item(Item=item)
    def get_by_organizer_email(self, organizer_email):

        response = self.table.query(
            IndexName="organizer_email-index",
            KeyConditionExpression="organizer_email = :organizer_email",
            ExpressionAttributeValues={
                ":organizer_email": organizer_email
            }
        )

        items = response.get("Items", [])

        events = []
        for item in items:
            events.append(Event(
                id=item["PK"].split("#")[1],
                name=item["name"],
                description=item.get("description"),
                event_start_datetime=item.get("event_start_datetime"),
                event_end_datetime=item.get("event_end_datetime"),
                organizer_email=item.get("organizer_email"),
            ))

        return events
    def get_by_id(self, event_id):

        response = self.table.get_item(
            Key={
                "PK": f"EVENT#{event_id}",
                "SK": "DETAILS"
            }
        )

        item = response.get("Item")

        if not item:
            return None

        return Event(
            id=item["PK"].split("#")[1],
            name=item["name"],
            description=item.get("description"),
            event_start_datetime=item.get("event_start_datetime"),
            event_end_datetime=item.get("event_end_datetime"),
            organizer_email=item.get("organizer_email"),
        )
    def delete_event(self, event_id):
        self.table.delete_item(
            Key={
                "PK": f"EVENT#{event_id}",
                "SK": "DETAILS"
            }
        )
    def update_status(self, event_id, status):
        self.table.update_item(
            Key={
                "PK": f"EVENT#{event_id}",
                "SK": "DETAILS"
            },
            UpdateExpression="set #s = :s",
            ExpressionAttributeNames={
                "#s": "status"
            },
            ExpressionAttributeValues={
                ":s": status
            }
        )
    def get_by_slug(self, slug):
        response = self.table.query(
            IndexName="slug-index",
            KeyConditionExpression="slug = :slug",
            ExpressionAttributeValues={
                ":slug": slug
            }
        )

        items = response.get("Items", [])

        if not items:
            return None

        item = items[0]

        return Event(
            id=item["PK"].split("#")[1],
            name=item["name"],
            description=item.get("description"),
            event_start_datetime=item.get("event_start_datetime"),
            event_end_datetime=item.get("event_end_datetime"),
            organizer_email=item.get("organizer_email"),
        )