from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote, unquote
from urllib.request import Request, urlopen

from fastapi import APIRouter

from app.config import settings
from app.schemas.tour import TourDateOut

router = APIRouter(prefix="/api/tour-dates", tags=["tour"])


def _normalize_ics_text(value: str) -> str:
	return (
		value.replace("\\,", ",")
		.replace("\\;", ";")
		.replace("\\n", " ")
		.replace("\\\\", "\\")
		.strip()
	)


def _unfold_ics_lines(text: str) -> list[str]:
	lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
	unfolded: list[str] = []
	for raw_line in lines:
		if not raw_line:
			continue
		if (raw_line.startswith(" ") or raw_line.startswith("\t")) and unfolded:
			unfolded[-1] += raw_line[1:]
		else:
			unfolded.append(raw_line)
	return unfolded


def _parse_ics_start_to_iso_date(value: str) -> str | None:
	cleaned = value.strip()
	if len(cleaned) >= 8 and cleaned[:8].isdigit():
		return f"{cleaned[:4]}-{cleaned[4:6]}-{cleaned[6:8]}"
	return None


def _load_google_ics_tour_dates() -> list[TourDateOut]:
	ics_url = settings.google_calendar_ics_url
	if not ics_url:
		return []

	request = Request(ics_url, headers={"Accept": "text/calendar"})
	with urlopen(request, timeout=8) as response:
		ics_text = response.read().decode("utf-8", errors="replace")

	lines = _unfold_ics_lines(ics_text)
	today_iso = datetime.now(UTC).date().isoformat()

	events: list[dict[str, str]] = []
	current: dict[str, str] | None = None
	for line in lines:
		upper_line = line.upper()
		if upper_line == "BEGIN:VEVENT":
			current = {}
			continue
		if upper_line == "END:VEVENT":
			if current:
				events.append(current)
			current = None
			continue
		if current is None or ":" not in line:
			continue

		key_with_params, value = line.split(":", 1)
		key = key_with_params.split(";", 1)[0].strip().upper()
		if key in {"SUMMARY", "LOCATION", "URL", "DTSTART", "DESCRIPTION"}:
			current[key] = _normalize_ics_text(value)

	def extract_first_http_url(raw_text: str) -> str | None:
		decoded = unquote(raw_text)
		match = re.search(r"(https?://[^\s<>\"']+)", decoded)
		if not match:
			return None
		return match.group(1).strip()

	def ticket_url_from_ics_item(item: dict[str, str]) -> str:
		direct_url = extract_first_http_url(item.get("URL", ""))
		if direct_url:
			return direct_url

		description = item.get("DESCRIPTION", "")
		description_decoded = unquote(description)
		match = re.search(
			r"tickets?\s*:\s*(https?://[^\s<>\"']+)",
			description_decoded,
			flags=re.IGNORECASE,
		)
		if match:
			return match.group(1).strip()

		fallback_url = extract_first_http_url(description)
		if fallback_url:
			return fallback_url

		return "https://example.com/tickets"

	results: list[TourDateOut] = []
	for item in events:
		date_iso = _parse_ics_start_to_iso_date(item.get("DTSTART", ""))
		if not date_iso or date_iso < today_iso:
			continue

		event_name = item.get("SUMMARY", "Live Show").strip() or "Live Show"
		city, venue_name = _city_and_venue({"location": item.get("LOCATION", "")})
		ticket_url = ticket_url_from_ics_item(item)
		results.append(
			TourDateOut(
				id=len(results) + 1,
				event_name=event_name,
				date=date_iso,
				city=city,
				venue_name=venue_name,
				ticket_url=ticket_url,
			)
		)

	results.sort(key=lambda entry: str(entry.date))
	return results


def _ticket_url_from_event(item: dict[str, Any]) -> str:
	html_link = item.get("htmlLink")
	if isinstance(html_link, str) and html_link:
		return html_link
	return "https://example.com/tickets"


def _city_and_venue(item: dict[str, Any]) -> tuple[str, str]:
	location = item.get("location")
	if isinstance(location, str) and location.strip():
		parts = [part.strip() for part in location.split(",") if part.strip()]
		if len(parts) >= 2:
			return parts[-1], parts[0]
		return location.strip(), location.strip()
	return "TBA", "TBA"


def _date_from_event(item: dict[str, Any]) -> str:
	start = item.get("start", {})
	if isinstance(start, dict):
		date_value = start.get("date")
		if isinstance(date_value, str) and date_value:
			return date_value
		datetime_value = start.get("dateTime")
		if isinstance(datetime_value, str) and datetime_value:
			return datetime_value[:10]
	return "2026-01-01"


def _load_google_tour_dates() -> list[TourDateOut]:
	calendar_id = settings.google_calendar_id
	api_key = settings.google_api_key
	if not calendar_id or not api_key:
		return []

	now_iso = datetime.now(UTC).isoformat().replace("+00:00", "Z")
	calendar_id_encoded = quote(calendar_id, safe="")
	url = (
		f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id_encoded}/events"
		f"?key={api_key}&singleEvents=true&orderBy=startTime&timeMin={now_iso}&maxResults=20"
	)

	request = Request(url, headers={"Accept": "application/json"})
	with urlopen(request, timeout=8) as response:
		payload = json.loads(response.read().decode("utf-8"))

	items = payload.get("items", [])
	if not isinstance(items, list):
		return []

	results: list[TourDateOut] = []
	for idx, item in enumerate(items, start=1):
		if not isinstance(item, dict):
			continue
		event_name = item.get("summary")
		if not isinstance(event_name, str) or not event_name.strip():
			event_name = "Live Show"
		city, venue_name = _city_and_venue(item)
		results.append(
			TourDateOut(
				id=idx,
				event_name=event_name.strip(),
				date=_date_from_event(item),
				city=city,
				venue_name=venue_name,
				ticket_url=_ticket_url_from_event(item),
			)
		)
	return results


@router.get("", response_model=list[TourDateOut])
def list_tour_dates() -> list[TourDateOut]:
	try:
		ics_dates = _load_google_ics_tour_dates()
		if ics_dates:
			return ics_dates
	except Exception:
		pass

	try:
		google_dates = _load_google_tour_dates()
		if google_dates:
			return google_dates
	except Exception:
		pass

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
