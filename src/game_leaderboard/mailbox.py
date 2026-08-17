import requests


class SmailsMailbox:
    BASE_URL = "https://smails.dev/api/mailbox"

    def __init__(self):
        self._token = None

    def create_mailbox(self) -> bool:
        try:
            response = requests.post(self.BASE_URL, timeout=10)
            response.raise_for_status()

            data = response.json()
            token = data.get("token")

            if not token:
                return False

            self._token = token
            return True

        except (requests.RequestException, ValueError):
            return False

    def get_code(self):
        if not self._token:
            return None

        try:
            response = requests.get(
                f"{self.BASE_URL}/messages",
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=10,
            )
            response.raise_for_status()

            messages = response.json()

            if not messages:
                return None

            # Most recent message is first based on the API response.
            preview = messages[0].get("preview", "")

            # Expected format: "Your sign in code is 800728"
            import re

            match = re.search(r"sign in code is\s+(\d+)", preview, re.IGNORECASE)
            return match.group(1) if match else None

        except (requests.RequestException, ValueError):
            return None