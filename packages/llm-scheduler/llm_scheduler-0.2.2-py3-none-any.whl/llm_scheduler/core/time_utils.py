from datetime import datetime, timedelta
import pytz
from typing import Optional, Tuple
import re

class TimeParser:
    """Utility class for handling time parsing and validation"""
    
    def __init__(self, default_timezone: str = "UTC"):
        self.default_timezone = pytz.timezone(default_timezone)
        
    def parse_and_validate_time(
        self,
        time_str: str,
        base_time: Optional[datetime] = None,
        user_timezone: Optional[str] = None
    ) -> Tuple[datetime, str]:
        """Parse time string and return validated datetime"""
        try:
            if not base_time:
                base_time = datetime.now(self.default_timezone)
                
            user_tz = pytz.timezone(user_timezone) if user_timezone else self.default_timezone
            
            # Try parsing as ISO format first
            try:
                dt = datetime.fromisoformat(time_str)
                if dt.tzinfo is None:
                    dt = user_tz.localize(dt)
                return dt.astimezone(pytz.UTC), "UTC"
            except ValueError:
                pass
                
            # Try natural language parsing
            parsed_time = self._parse_natural_language(time_str, base_time, user_tz)
            if parsed_time:
                return parsed_time.astimezone(pytz.UTC), "UTC"
                
            raise ValueError(f"Could not parse time: {time_str}")
            
        except Exception as e:
            raise ValueError(f"Time parsing failed: {str(e)}")
            
    def _parse_natural_language(
        self,
        text: str,
        base_time: datetime,
        timezone: pytz.timezone
    ) -> Optional[datetime]:
        """Parse natural language time expressions"""
        patterns = {
            # Add your time patterns here
            r'in (\d+) (minute|minutes|hour|hours|day|days)': self._handle_relative_time,
            r'tomorrow at (\d{1,2}):(\d{2})\s*(am|pm)': self._handle_tomorrow_at,
            r'today at (\d{1,2}):(\d{2})\s*(am|pm)': self._handle_today_at,
            # Add more patterns as needed
        }
        
        for pattern, handler in patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                return handler(match, base_time, timezone)
                
        return None
        
    def _handle_relative_time(
        self,
        match: re.Match,
        base_time: datetime,
        timezone: pytz.timezone
    ) -> datetime:
        """Handle relative time expressions"""
        amount = int(match.group(1))
        unit = match.group(2).lower()
        
        if unit in ['minute', 'minutes']:
            delta = timedelta(minutes=amount)
        elif unit in ['hour', 'hours']:
            delta = timedelta(hours=amount)
        elif unit in ['day', 'days']:
            delta = timedelta(days=amount)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")
            
        return base_time + delta
        
    # Add more handler methods as needed 