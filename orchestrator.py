PORT = "9001"
PYDANTIC_FOLDER = './pydantic_versions'


from pypi_multi_versions.importer import import_helper
from pypi_multi_versions.installer import install_version

try:
    with import_helper('pydantic', '1.10.17', PYDANTIC_FOLDER):
        import pydantic

except:
    install_version('pydantic', '1.10.17', PYDANTIC_FOLDER)
    with import_helper('pydantic', '1.10.17', PYDANTIC_FOLDER):
        import pydantic

try:
    with import_helper('pydantic', '2.8.2', PYDANTIC_FOLDER):
        from pydantic import BaseModel

except:
    install_version('pydantic', '2.8.2', PYDANTIC_FOLDER)
    with import_helper('pydantic', '2.8.2', PYDANTIC_FOLDER):
        from pydantic import BaseModel


from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

import py_avro_schema
import uvicorn
from fastapi import Body, FastAPI, status
from fastapi.responses import RedirectResponse
from fluvii.components import ProducerFactory


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


app = FastAPI()


@app.get("/", status_code=302)
def root() -> RedirectResponse:
    return RedirectResponse("/docs")

@app.post(
    '/bookings', 
    status_code=status.HTTP_202_ACCEPTED,
    tags=['bookings']
)
def post_booking(booking: Annotated[BookingInput, Body()]) -> BookingCommand:
    process_id = uuid4()

    command = BookingCommand(
        account_id=booking.account_id,
        amount=booking.amount,
        process_id=process_id
    )

    return command


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
