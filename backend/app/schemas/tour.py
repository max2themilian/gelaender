from pydantic import BaseModel


class TourDateOut(BaseModel):
	id: int
	event_name: str
	date: str
	city: str
	venue_name: str
	ticket_url: str
