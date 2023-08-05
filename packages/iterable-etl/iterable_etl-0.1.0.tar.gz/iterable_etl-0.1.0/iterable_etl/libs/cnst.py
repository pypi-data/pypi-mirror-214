"""constants"""

import os
from datetime import date
from typing import Dict, Any

urls = {
    "lists": "https://api.iterable.com/api/lists",
    "campaigns": "https://api.iterable.com/api/campaigns",
    "metrics": "https://api.iterable.com/api/campaigns/metrics",
}


def get_headers() -> Dict[str, Any]:
    """header config for Iterable API"""
    headers = {
        "Api-Key": os.environ.get("ITERABLE_KEY"),
        "Content-Type": "application/json",
    }
    return headers


def get_todays_date():
    """today"""
    today = date.today()
    return today.strftime("%Y-%m-%d")
