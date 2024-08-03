HOST = "0.0.0.0"


from datetime import datetime
from uuid import UUID

import py_avro_schema
from pydantic import BaseModel


class BookingInput(BaseModel):
    account_id: UUID
    amount: int

class BookingCommand(BookingInput):
    process_id: UUID

class Event(BaseModel):
    id: UUID
    event_datetime: datetime

class BookingEvent(BookingCommand, Event):
    running_balance: int
    

# Avro schemas
booking_command = py_avro_schema.generate(BookingCommand)
booking_event = py_avro_schema.generate(BookingEvent)
