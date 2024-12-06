"""A wrapper module for making HTTP requests using httpx."""
import html
import json
from typing import Any

import requests
from requests import HTTPError, JSONDecodeError, ReadTimeout, RequestException, Response, Timeout, TooManyRedirects

from .utils.logger import logger
from .exceptions import BadRequestError


class Requests:
    """A wrapper class for making HTTP requests using httpx.

    This class provides methods to make HTTP GET, POST, PUT, and DELETE requests
    with support for setting headers, cookies, and user agent. It also includes
    error handling.

    Attributes:
        default_headers (dict): The default headers to include in the requests.
        cookies (dict): The cookies to include in the requests.
    """

    def __init__(self, headers: dict[str, str] = {}, cookies: dict[str, str] = {}):
        """Initializes the request handler with optional headers and cookies.

        Args:
            headers: A dictionary containing the default request headers. Defaults to an empty dictionary.
            cookies: A dictionary or string representing the default request cookies. Defaults to an empty dictionary.
                If a string is provided, it will be converted to a dictionary.
        """
        if not headers:
            headers = {}
        if not cookies:
            cookies = {}
        elif isinstance(cookies, str):
            cookies = self.__cookie_str_to_dict(cookies)
        self.default_headers = headers
        self.cookies = cookies
        self.session = requests.session()

    def remove_headers(self, key: str) -> None:
        """Removes the default headers.

        Args:
            key: The key to remove from the headers.
        """
        del self.default_headers[key]

    def set_headers(self, headers: dict[str, str]) -> None:
        """Updates the default headers with the provided headers.

        Args:
            headers: A dictionary containing the headers to update.
        """
        self.default_headers |= headers

    def set_cookies(self, cookies: dict[str, str]) -> None:
        """Updates the cookies with the provided cookies.

        Args:
            cookies: A dictionary containing the cookies to update.
        """
        self.cookies |= cookies

    def set_cookies_to_session(self, cookies: dict[str, str]) -> None:
        """Updates the cookies with the provided cookies.

        Args:
            cookies: A dictionary containing the cookies to update.
        """
        for name, value in cookies.items():
            self.session.cookies.set(name, value)

    def set_user_agent(self, user_agent: str) -> None:
        """Sets the User-Agent header to the provided user agent string.

        Args:
            user_agent: A string representing the user agent to set.
        """
        self.default_headers["User-Agent"] = user_agent

    def __prepare_request(
        self, url: str, headers: dict[str, str], cookies: dict[str, str]
    ) -> tuple[str, dict[str, str], dict[str, str]]:
        """Prepares the request URL, headers, and cookies for the HTTP request.

        Args:
            url: A string representing the request URL.
            headers: A dictionary containing the request headers.
            cookies: A dictionary containing the request cookies.

        Returns:
            A tuple contain
            ing the updated URL, headers, and cookies.
        """
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        elif isinstance(cookies, str):
            cookies = self.__cookie_str_to_dict(cookies)
        if not isinstance(self.cookies, dict):
            self.cookies = dict(self.cookies)
        final_headers = self.default_headers.copy()
        final_headers.update(headers)
        final_cookies = self.cookies.copy()
        final_cookies.update(cookies)
        return url, final_headers, final_cookies

    @staticmethod
    def __handle_response(response: Response) -> dict[str, Any]:
        """Handles the HTTP response, checking for errors and returning the response content.

        Args:
            response: An HTTPX Response object.

        Returns:
            The JSON content if the response is in JSON format, otherwise the response text.
        """
        try:
            response.raise_for_status()
            text = html.unescape(response.text)
            return json.loads(text) if "application/json" in response.headers.get("Content-Type", "") else text
        except (HTTPError, JSONDecodeError, ReadTimeout, RequestException, Timeout, TooManyRedirects) as exc:
            logger.error(f"An error occurred while requesting: {exc.response.status_code} - {exc.response.text}")
            raise BadRequestError(str(exc))

    @staticmethod
    def __cookie_str_to_dict(cookie_str: str) -> dict[str, str]:
        """Transforms a cookie string into a dictionary.

        Args:
            cookie_str (str): The cookie string.

        Returns:
            dict: A dictionary containing the cookie key-value pairs.
        """
        cookies = {}
        pairs = cookie_str.split("; ")
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                cookies[key] = value
        return cookies

    def get_response_data(
        self,
        url: str,
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
        params: dict[str, Any] = {},
        data: Any = None,
        json: Any = None,
        method: str = "GET",
    ) -> Response:
        """Get the response data.

        Args:
            url: A string representing the request URL.
            data: The data to send in the request body. Defaults to None.
            json: The JSON data to send in the request body. Defaults to None.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.
            params: A dictionary containing the request parameters. Defaults to an empty dictionary.
            method: A string representing the request method. Defaults to "GET".

        Returns:
            The response object.
        """
        url, final_headers, final_cookies = self.__prepare_request(url, headers, cookies)
        self.set_cookies_to_session(final_cookies)
        if method == "GET":
            return self.session.get(url, headers=final_headers, params=params)
        elif method == "POST":
            return self.session.post(url, data=data, json=json, headers=final_headers)
        elif method == "PUT":
            return self.session.put(url, data=data, json=json, headers=final_headers)

    def get(
        self,
        url: str,
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
        params: dict[str, Any] = {},
    ) -> dict[str, Any]:
        """Sends a GET request to the specified URL with optional headers, cookies, and parameters.

        Args:
            url: A string representing the request URL.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.
            params: A dictionary containing the request parameters. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful.
        """
        if params is None:
            params = {}
        url, final_headers, final_cookies = self.__prepare_request(url, headers, cookies)
        self.set_cookies_to_session(final_cookies)
        response = self.session.get(url, headers=final_headers, params=params)
        return self.__handle_response(response)

    def post(
        self,
        url: str,
        data: Any = None,
        json: Any = None,
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
    ) -> dict[str, Any]:
        """Sends a POST request to the specified URL with optional data, JSON, headers, and cookies.

        Args:
            url: A string representing the request URL.
            data: The data to send in the request body. Defaults to None.
            json: The JSON data to send in the request body. Defaults to None.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful.
        """
        url, final_headers, final_cookies = self.__prepare_request(url, headers, cookies)
        self.set_cookies_to_session(final_cookies)
        response = self.session.post(url, data=data, json=json, headers=final_headers)
        return self.__handle_response(response)

    def put(
        self,
        url: str,
        data: Any = None,
        json: Any = None,
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
    ) -> dict[str, Any]:
        """Sends a PUT request to the specified URL with optional data, JSON, headers, and cookies.

        Args:
            url: A string representing the request URL.
            data: The data to send in the request body. Defaults to None.
            json: The JSON data to send in the request body. Defaults to None.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful
        """
        url, final_headers, final_cookies = self.__prepare_request(url, headers, cookies)
        self.set_cookies_to_session(final_cookies)
        response = self.session.put(url, data=data, json=json, headers=final_headers)
        return self.__handle_response(response)

    def delete(self, url: str, headers: dict[str, str] = {}, cookies: dict[str, str] = {}) -> dict[str, Any]:
        """Sends a DELETE request to the specified URL with optional headers and cookies.

        Args:
            url: A string representing the request URL.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful
        """
        url, final_headers, final_cookies = self.__prepare_request(url, headers, cookies)
        self.set_cookies_to_session(final_cookies)
        response = self.session.delete(url, headers=final_headers)
        return self.__handle_response(response)
