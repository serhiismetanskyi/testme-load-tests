"""HTTP requests utilities."""

import re


class Utils:
    """HTTP requests and tokens helpers."""

    @staticmethod
    def get_base_headers():
        """Base JSON headers."""
        base_headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        return base_headers

    @staticmethod
    def get_token_value(headers):
        """Get CSRF token from headers."""
        token_value = r"csrftoken=([a-zA-Z0-9]+);"
        token_search = re.search(token_value, str(headers))
        if token_search:
            token = token_search.group(1)
            return token
        return None

    @staticmethod
    def get_headers_with_token(token):
        """Add CSRF token to headers."""
        headers = Utils.get_base_headers()
        headers["X-CSRFToken"] = token
        return headers

    @staticmethod
    def extract_token_from_response(response):
        """Get CSRF token from response."""
        if hasattr(response, "headers") and response.headers:
            set_cookie = response.headers.get("Set-Cookie", "")
            if set_cookie:
                token = Utils.get_token_value(set_cookie)
                if token:
                    return token

        if hasattr(response, "cookies") and response.cookies:
            if isinstance(response.cookies, dict):
                if "csrftoken" in response.cookies:
                    return response.cookies["csrftoken"]
            else:
                try:
                    csrf_cookie = response.cookies.get("csrftoken")
                    if csrf_cookie:
                        return csrf_cookie
                except (AttributeError, KeyError, TypeError):
                    pass

            try:
                cookies_dict = dict(response.cookies)
                if "csrftoken" in cookies_dict:
                    return cookies_dict["csrftoken"]
            except (TypeError, ValueError):
                pass

        return None
