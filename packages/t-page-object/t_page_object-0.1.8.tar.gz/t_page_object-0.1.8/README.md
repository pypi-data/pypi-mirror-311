# T_page_object 📦

> **A Python package for taking an object oriented approach
            when interacting with web pages and their elements .**

## 📑 Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [API Documentation](#api-documentation)
- [License](#license)

## Overview
This package provides various modules and classes for creating portals, web pages and web elements.
            
There are also usable web elements that have commonly used methods built in.

## Installation
```bash
pip install t-page-object
```

## Usage Example
For detailed examples, please refer to our
            [quick start page](https://www.notion.so/thoughtfulautomation/T-Page-Object-126f43a78fa480e39a1af8f99f93affe).

### 
## API Documentation

---

## Base_app
### Module: `t_page_object.base_app`

_Module for BaseApp class._

- **Class:** `BaseApp`
  > Base class for application or portal objects and their configuration.
  - **Method:** `open_browser`
    > Open browser and set Selenium options.

---

## Base_element
### Module: `t_page_object.base_element`

_Contains the BaseElement class._

- **Class:** `BaseElement`
  > This is an Element used to build each Page.
  - **Method:** `format_xpath`
    > If using a dynamic xpath, this method formats the xpath string.

        Args:
            *args (list): The arguments to be used to format the xpath.
            **kwargs (dict): The keyword arguments to be used to format the
        
  - **Method:** `wait_element_load`
    > 
        Wait for element to load.

        Args:
            timeout (int, optional): The maximum time to wait for the element to be present, in seconds.
                Defaults to None. Overwrites apps inherent timeout if set.

        Returns:
            bool: True if element is visible, False not found and wait is False otherwise.

        Raises:
            AssertionError: If element is not visible and wait is True.
        

---

## Base_page
### Module: `t_page_object.base_page`

_Contains the BasePage class which is the parent class for all page objects in the project._

- **Class:** `BasePage`
  > Base page class for all page objects in the project.
  - **Method:** `get_element_from_shadow_roots`
    > Get element from nested shadow roots.

        Args:
            roots: The css locators of the shadow root elements, in hierarchal order.
            element_css: The css locator of the element to find.

        Returns:
            The WebElement of the element found.
        
  - **Method:** `visit`
    > Navigate to the base page URL.
  - **Method:** `wait_for_new_window_and_switch`
    > Function for waiting and switching to new window.

        Args:
            old_window_handles: The list of window handles before the new window is opened.

        Returns:
            The new window handle.
        
  - **Method:** `wait_page_load`
    > Wait for the page to load by waiting for the verification element to load.

        timeout: The maximum time to wait for the element to be present, in seconds.
        

---

## Bot_config
### Module: `t_page_object.bot_config`

_Congifuration module for the t_page_object package._

- **Class:** `BotConfig`
  > Class for configuration.

---

## Elements
### Module: `t_page_object.elements`

_Module for all base ui components._

### Module: `t_page_object.elements.button_element`

_Button element module._

- **Class:** `ButtonElement`
  > Standard button element.
  - **Method:** `click`
    > Main click method for button element.

        Checks if button is dev_save_sensitive and if dev_safe_mode is enabled.
        
  - **Method:** `click_button`
    > Redirects to click method.
  - **Method:** `click_button_if_visible`
    > Redirects to click method.
  - **Method:** `click_button_when_visible`
    > Redirects to click method.
  - **Method:** `click_element`
    > Redirects to click method.
  - **Method:** `click_element_if_visible`
    > Redirects to click method.
  - **Method:** `click_element_when_clickable`
    > Redirects to click method.
  - **Method:** `click_element_when_visible`
    > Redirects to click method.
### Module: `t_page_object.elements.checkox_element`

_Checkbox element module._

- **Class:** `CheckboxElement`
  > Checkbox element.
  - **Method:** `select`
    > Selects the checkbox element.
### Module: `t_page_object.elements.container_element`

_Class for container elements._

- **Class:** `ContainerElement`
  > Container element. Used to hold multiple text elements.
  - **Method:** `get_text_values`
    > Get text for each element with id matching class attribute.

        Args:
            cls (Type[TO]): The class to use for the object.

        Returns:
            Instance of input class with text values.
        
  - **Method:** `set_text_values`
    > Sets text for each element with id matching class attribute.

        Args:
            cls (Type[TO]): The object to use for the text values.
        
### Module: `t_page_object.elements.dropdown_element`

_Dropdown element module._

- **Class:** `DropdownElement`
  > Standard dropdown element.
  - **Method:** `click_and_select_option`
    > Selects an option from the dropdown list based on the provided text.

        The dropdown list is clicked to open the list and the option is selected.

        Args:
            text_to_find (str): The text of the option to be selected from the dropdown list.
            option_tag (str, optional): The tag of the option to be selected from the dropdown list. Defaults to 'li'.

        Returns:
            None
        
  - **Method:** `type_and_enter`
    > Selects an option from the dropdown list based on the provided text.

        The text is input into the dropdown list input and the Enter key is pressed to select the option.

        Args:
            text_to_enter (str): The text/s of the option to be selected from the dropdown list.
            option_tag (str): The tag used for the different options. Defaults to 'li'.

        Returns:
            None
        
### Module: `t_page_object.elements.iframe_element`

_Frame element module._

- **Class:** `IFrameElement`
  > Class for frame element model.
  - **Method:** `select_iframe`
    > Select frame.
  - **Method:** `select_nested_iframe`
    > Select nested frame.

        Args:
            frames: list of frame locators
            from_base: bool, if True, unselects the current frame before selecting the nested frames
        
  - **Method:** `unselect_iframe`
    > Selects base frame.
### Module: `t_page_object.elements.image_element`

_Image element module._

- **Class:** `ImageElement`
  > Image element.
  - **Method:** `download_image`
    > Download images using RPA.HTTP and return the local path.

        Args:
            download_path (str, optional): The path to save the downloaded image. Defaults to output_folder.

        Returns:
            str: The path of the downloaded image.
        
### Module: `t_page_object.elements.input_element`

_Input element module._

- **Class:** `InputElement`
  > Input element.
  - **Method:** `click_and_input_text`
    > Input text into element.
  - **Method:** `get_input_value`
    > Get input value.
  - **Method:** `input_text_and_check`
    > 
        Inputs the given text into an element and verifies the input.

        Args:
            text (str): The text to input into the element.
            tries (int, optional): The number of attempts to verify the text input. Defaults to 5.

        Returns:
            None
        
### Module: `t_page_object.elements.table_element`

_Table element module._

- **Class:** `TableElement`
  > Table element.
### Module: `t_page_object.elements.text_element`

_This module contains the TextElement class for the text element model._

- **Class:** `TextElement`
  > Input element.
  - **Method:** `get_clean_text`
    > Get text from element and clean.

---

## Selenium_manager
### Module: `t_page_object.selenium_manager`

_Create a singleton manager to ensure a single instance of Selenium._

- **Class:** `SeleniumManager`
  > Singleton manager to ensure a single instance of Selenium.

---

## T_requests
### Module: `t_page_object.t_requests`

_A wrapper module for making HTTP requests using httpx._

- **Class:** `Requests`
  > A wrapper class for making HTTP requests using httpx.

    This class provides methods to make HTTP GET, POST, PUT, and DELETE requests
    with support for setting headers, cookies, and user agent. It also includes
    error handling.

    Attributes:
        default_headers (dict): The default headers to include in the requests.
        cookies (dict): The cookies to include in the requests.
    
  - **Method:** `delete`
    > Sends a DELETE request to the specified URL with optional headers and cookies.

        Args:
            url: A string representing the request URL.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful
        
  - **Method:** `get`
    > Sends a GET request to the specified URL with optional headers, cookies, and parameters.

        Args:
            url: A string representing the request URL.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.
            params: A dictionary containing the request parameters. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful.
        
  - **Method:** `get_response_data`
    > Get the response data.

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
        
  - **Method:** `post`
    > Sends a POST request to the specified URL with optional data, JSON, headers, and cookies.

        Args:
            url: A string representing the request URL.
            data: The data to send in the request body. Defaults to None.
            json: The JSON data to send in the request body. Defaults to None.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful.
        
  - **Method:** `put`
    > Sends a PUT request to the specified URL with optional data, JSON, headers, and cookies.

        Args:
            url: A string representing the request URL.
            data: The data to send in the request body. Defaults to None.
            json: The JSON data to send in the request body. Defaults to None.
            headers: A dictionary containing the request headers. Defaults to an empty dictionary.
            cookies: A dictionary containing the request cookies. Defaults to an empty dictionary.

        Returns:
            The response content if the request is successful
        
  - **Method:** `remove_headers`
    > Removes the default headers.

        Args:
            key: The key to remove from the headers.
        
  - **Method:** `set_cookies`
    > Updates the cookies with the provided cookies.

        Args:
            cookies: A dictionary containing the cookies to update.
        
  - **Method:** `set_cookies_to_session`
    > Updates the cookies with the provided cookies.

        Args:
            cookies: A dictionary containing the cookies to update.
        
  - **Method:** `set_headers`
    > Updates the default headers with the provided headers.

        Args:
            headers: A dictionary containing the headers to update.
        
  - **Method:** `set_user_agent`
    > Sets the User-Agent header to the provided user agent string.

        Args:
            user_agent: A string representing the user agent to set.
        

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
