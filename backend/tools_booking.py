import re
from dateutil.parser import parse as parse_date


def validate_email(email: str) -> bool:
    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    pattern = r"^\+?\d{7,15}$"
    return re.match(pattern, phone) is not None


def parse_date_text(date_text: str) -> str:
    try:
        dt = parse_date(date_text, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""
