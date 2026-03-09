from boto3.dynamodb.conditions import Key
from app.domain.event import Event

class EventRepository:

    def __init__(self, dynamodb, table_name):
        self.table = dynamodb.Table(table_name)

    def save(self, event: Event):
        item = {
            "PK": f"EVENT#{event.id}",
            "SK": "DETAILS",
            "title": event.title,
            "description": event.description,
            "event_start_datetime": str(event.event_start_datetime) if event.event_start_datetime else None,
            "event_end_datetime": str(event.event_end_datetime) if event.event_end_datetime else None,
            "organizer_id": event.organizer_id,
            "slug": event.slug,
        }
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
        return Event(
            id=item["PK"].split("#")[1],
            title=item["title"],
            description=item.get("description"),
            event_start_datetime=item.get("event_start_datetime"),
            event_end_datetime=item.get("event_end_datetime"),
            organizer_id=item.get("organizer_id"),
        )
    def get_events_by_organizer_id(self, organizer_id):
        response = self.table.query(
            IndexName="organizer-index",
            KeyConditionExpression=Key("organizer_id").eq(organizer_id)
        )
        items = response.get("Items", [])
        return [
            Event(
                id=item["PK"].split("#")[1],
                title=item["title"],
                description=item.get("description"),
                event_start_datetime=item.get("event_start_datetime"),
                event_end_datetime=item.get("event_end_datetime"),
                organizer_id=item.get("organizer_id"),
            )
            for item in items
        ]
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
        return Event(
            id=item["PK"].split("#")[1],
            title=item["title"],
            description=item.get("description"),
            event_start_datetime=item.get("event_start_datetime"),
            event_end_datetime=item.get("event_end_datetime"),
            organizer_id=item.get("organizer_id"),
        )

    def get_by_title_and_id(self, title, organizer_id):
        # Use a composite filter if title is not the partition key
        response = self.table.query(
            IndexName="title-organizerid-index",
            KeyConditionExpression=Key("title").eq(title) & Key("organizer_id").eq(organizer_id)
        )
        print("Query response:---------------------------------------------------------------------------------------------", response)  
        items = response.get("Items")
        if not items:
            return False
        else:
            return True