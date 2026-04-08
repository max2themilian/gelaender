from datetime import date

from pydantic import BaseModel, HttpUrl


class TourDateOut(BaseModel):
	id: int
	event_name: str
	date: date
	city: str
	venue_name: str
	ticket_url: HttpUrl
