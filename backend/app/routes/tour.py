from fastapi import APIRouter

from app.schemas.tour import TourDateOut

router = APIRouter(prefix="/api/tour-dates", tags=["tour"])


@router.get("", response_model=list[TourDateOut])
def list_tour_dates() -> list[TourDateOut]:
	return [
		TourDateOut(
			id=1,
			event_name="Live at Das Lichtwerk",
			date="2026-06-14",
			city="Berlin",
			venue_name="Das Lichtwerk",
			ticket_url="https://example.com/tickets/berlin",
		),
		TourDateOut(
			id=2,
			event_name="Live at Stromhaus",
			date="2026-07-02",
			city="Leipzig",
			venue_name="Stromhaus",
			ticket_url="https://example.com/tickets/leipzig",
		),
	]
