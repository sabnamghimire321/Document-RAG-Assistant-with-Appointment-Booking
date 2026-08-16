import json
from pathlib import Path

from backend.rag_chain import answer_from_docs
from backend.tools_booking import parse_date_text, validate_email, validate_phone

APPOINTMENTS_FILE = Path("storage/appointments.jsonl")

BOOKING_TRIGGERS = ["call me", "book appointment", "schedule", "i want a call"]


def agent_tool(query: str, booking_info: dict = None) -> str:
    if booking_info and any(t in query.lower() for t in BOOKING_TRIGGERS):
        return book_appointment(booking_info)
    return answer_from_docs(query)


def book_appointment(booking_info: dict) -> str:
    name = booking_info.get("name", "")
    phone = booking_info.get("phone", "")
    email = booking_info.get("email", "")
    date_text = booking_info.get("date", "")

    if not name:
        return "Name is required."
    if not validate_phone(phone):
        return "Invalid phone number."
    if not validate_email(email):
        return "Invalid email."

    date_iso = parse_date_text(date_text)
    if not date_iso:
        return "Invalid date."

    APPOINTMENTS_FILE.parent.mkdir(exist_ok=True)
    with APPOINTMENTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"name": name, "phone": phone, "email": email, "date": date_iso}) + "\n")

    return f"Appointment booked for {name} on {date_iso}."
