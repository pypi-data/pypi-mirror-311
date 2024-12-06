"""
WGM_api - API Client for WireGuard Management

This library provides a client for interacting with a WireGuard server API, 
allowing users to perform actions such as creating, deleting, enabling, and 
disabling users, as well as managing sessions and retrieving user information.

Features:
- Start a session with the server using credentials (IP, port, password).
- Retrieve a list of all users.
- Perform data manipulation actions (e.g., create, delete, enable, disable users).
- Supports automatic session re-establishment if authentication fails.

Usage:
    1. Initialize the `WGM_api` class.
    2. Use the `start_session` method to authenticate and establish a session.
    3. Use methods like `get_all_users`, `create_user`, `delete_user`, etc., 
       to interact with the WireGuard server.

Dependencies:
    - requests
    - json
    - logging

Example:
    session = WGM_api()
    session.start_session(ip_address="ip_address", port=port, password="your_password")
    session.create_user(name="new_user")
    session.delete_user(value="existing_user")

"""

import requests
import json
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class WGM_api:
    _ip_address = None
    _port = None
    _password = None

    _api_clients = "api/wireguard/client"

    def __init__(self):
        self.session = requests.Session()
    
    def start_session(self, ip_address: str, port: int, password: str):
        r"""
        Initializes a session with the server using the provided credentials.

        This method sends a POST request to the server to establish a session. 
        If the session is successfully established, the session cookies are set 
        and stored for future requests. If the connection fails, an exception is raised.

        :param ip_address: 
            The IP address of the server to connect to.
        :param port: 
            The port number of the server to connect to.
        :param password: 
            The password used for authentication to establish the session.

        :raises Exception: 
            If the server returns a non-204 response, indicating a failure to connect.

        :return: 
            None. Sets internal attributes (`_ip_address`, `_port`, `_password`) 
            and configures session cookies upon successful connection.
        """

        try:
            logger.info(f"Attempting to start session with server {ip_address}:{port}...")
            res = self.session.post(url=f"http://{ip_address}:{port}/api/session", json={"password":f"{password}"})
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred during session establishment: {e}")
            raise

        if res.status_code != 204:
            logger.error("Failed to establish session, received non-204 response.")
            return False
        else:
            logger.info("Session established successfully.")
            cookies = [
                {"domain": key.domain, "name": key.name, "path": key.path, "value": key.value}
                for key in self.session.cookies
            ]
            for cookie in cookies:
                self.session.cookies.set(**cookie)

            self._ip_address = ip_address
            self._port = port
            self._password = password

            return True
            
    def get_all_users(self):
        r"""
        Retrieves the list of all users from the server.

        This method sends a GET request to the server to fetch a list of all users. 
        If the server returns a 401 (Unauthorized) status code, it attempts to re-establish 
        the session by calling `start_session`. If the request succeeds, it returns the 
        list of users as a JSON object.

        :return: 
            A list of users in JSON format if the request is successful.
            None if the session needs to be re-established.

        :raises Exception: 
            If the session re-establishment fails, or the response is not valid.
        """
        try:
            logger.info(f"Fetching all users from server {self._ip_address}:{self._port}...")
            res = self.session.get(url=f"http://{self._ip_address}:{self._port}/{self._api_clients}")
            res.raise_for_status()

            if res.status_code == 401:
                logger.warning("Session expired or unauthorized (401). Attempting to re-establish session...")
                self.start_session(ip_address=self._ip_address, port=self._port, password=self._password)
                return self.get_all_users()  # Retry after re-establishing the session
            else:
                logger.info(f"Successfully retrieved {len(res.json())} users.")
                return json.loads(res.text)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while fetching users: {e}")
            raise

    def data_manipulation(self, value, action, endpoint_suffix="", payload=None, success_message="", not_found_message="", path=""):
        r"""
        Performs a specified action on a user's data by sending an HTTP request to the server.

        This method facilitates actions such as creating, deleting, updating, or retrieving 
        data for a user. It identifies the user by their ID or username, constructs the 
        appropriate endpoint URL, and sends the request using the specified HTTP method.

        If the action involves downloading a configuration file (`endpoint_suffix="/configuration"`),
        the file is saved to the specified directory. If the directory does not exist, it will 
        be created automatically.

        :param value: 
            The identifier of the user. This can be:
            - User ID (str): A unique identifier for the user.
            - Username (str): The name of the user in the system.

        :param action: 
            The HTTP method to be used for the request. Common actions include:
            - 'GET': To retrieve data (e.g., download configuration).
            - 'POST': To create new data.
            - 'PUT': To update existing data.
            - 'DELETE': To delete data.

        :param endpoint_suffix: 
            (Optional) A suffix to be added to the API endpoint URL (e.g., "/configuration" 
            for downloading configuration). Default is an empty string.

        :param payload: 
            (Optional) Data to be included in the request body, typically used for 
            'POST' or 'PUT' requests. Default is `None`.

        :param success_message: 
            A message logged if the request is successful. Default is an empty string.

        :param not_found_message: 
            A message logged if the user is not found (404 response). Default is an empty string.

        :param path: 
            (Optional) The directory where configuration files should be saved if 
            the action involves downloading configurations. Default is an empty string.
            - If the directory does not exist, it will be created automatically.
            - If no path is specified, files will be saved to the current working directory.

        :return: 
            - `True` if the action is successfully completed.
            - `False` if the action fails or the user is not found.
            - For configuration downloads, the file will be saved to the specified directory.
        """
        try:
            logger.info(f"Attempting to manipulate data for user: {value} using action: {action}.")
            users = self.get_all_users()
            user_found = False

            for user in users:
                if user['id'] == value or user['name'] == value:
                    user_found = True
                    url = f"http://{self._ip_address}:{self._port}/{self._api_clients}/{user['id']}{endpoint_suffix}"
                    logger.info(f"User found. Sending {action} request to: {url}")
                    response = self.session.request(method=action, url=url, json=payload)

                    if response.status_code == 404:
                        logger.warning(f"User {value} not found on server. {not_found_message}")
                        return False
                    elif response.status_code in [200, 204]:  # Assuming 200/204 success codes for the action
                        logger.info(f"Action {action} on user {value} was successful. {success_message}")
                        if endpoint_suffix == "/configuration":
                            name = user["name"]

                            path_to_config = os.path.join(path, f"{name}.conf")
                            with open(path_to_config, "wb") as file:
                                file.write(response.content)
                                logger.info(f"The {name}.conf configuration file has been generated at {path_to_config}.")
                            return True

                        return True
                    else:
                        logger.error(f"Failed to perform {action} on user {value}. Status code: {response.status_code}. Response: {response.text}")
                        return False

            if not user_found:
                logger.warning(f"User {value} not found in the user list.")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while performing action on user {value}: {e}")
            raise  # Re-raise the exception to handle it higher up


    def create_user(self, name: str, download_config: bool = False, path: str = "."):
        r"""
        Creates a new user in the system with a unique name.

        This method sends a POST request to create a user with the specified name. 
        If a user with the same name already exists, a numerical suffix is added to 
        ensure uniqueness (e.g., "user_1", "user_2", etc.).

        :param name: 
            The desired username for the new user. 
            If the name is already taken, a unique suffix will be appended.

        :return: 
            True if the user is successfully created.
            If a 401 (Unauthorized) error occurs, the method automatically restarts 
            the session using the current connection parameters.
            Prints the response status code to the console.
        """
        
        try:
            users = self.get_all_users()
            check_username = [user['name'] for user in users if user["name"].startswith(name)]

            if check_username:
                max_suff = 0
                for u_name in check_username:
                    if u_name == name:
                        curr_suff = 0
                    else:
                        suff = u_name[len(name):]
                        if suff.startswith('_'):
                            suff = suff[1:]
                        try:
                            curr_suff = int(suff)
                        except ValueError:
                            curr_suff = 0
                    max_suff = max(max_suff, curr_suff)
                name = f"{name}_{max_suff+1}"

            logger.info(f"Attempting to create user with name: {name}")
            res = self.session.post(url=f"http://{self._ip_address}:{self._port}/{self._api_clients}", json={"name": f"{name}"})

            if res.status_code == 401:
                logger.warning(f"Unauthorized access while creating user {name}. Restarting session.")
                self.start_session(ip_address=self._ip_address, port=self._port, password=self._password)
            else:
                if res.status_code == 200 or res.status_code == 201:
                    logger.info(f"User {name} successfully created. Response status code: {res.status_code}")
                    if download_config:
                        self.download_config(name, path)
                    return True
                else:
                    logger.error(f"Failed to create user {name}. Status code: {res.status_code}. Response: {res.text}")
                    return False
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while creating user {name}: {e}")
            raise  # Re-raise the exception to handle it higher up

    def download_config(self, value, path=""):
        r"""
        Downloads a configuration file for a user.

        This method sends a `GET` request to the server to retrieve a user's 
        configuration file. If the configuration is successfully generated, it 
        will be saved to the specified `path`. If no path is provided, the default 
        behavior depends on the implementation of `self.data_manipulation`.

        :param value:
            The identifier of the user whose configuration is to be downloaded.
            This can be one of the following:
            - User ID (str): A unique numerical identifier for the user.
            - Username (str): The name of the user in the system.

        :param path: 
            (Optional) The file path where the configuration will be saved.
            If not provided, the default behavior of the `self.data_manipulation`
            method will determine the file's location. 

            *Note*: If saving to a specific location is required, ensure this
            parameter is set explicitly.

        :return:
            - `True` if the configuration file is successfully generated and saved.
            - `False` if there is an error during the configuration process.
        """

        try:
            request = self.data_manipulation(
                value=value,
                action='GET',
                endpoint_suffix="/configuration",
                success_message="The configuration has been downloaded.",
                not_found_message="The configuration was not found.",
                path=path
            )

            if request:
                logger.info(f"The configuration file has been successfully generated.")
                return True
            else:
                logger.warning("An error occurred during the formation of the configuration file.")
                return False

        except Exception as e:
            logger.error(f"An error occurred while downloading the user configuration {value}: {e}")

        
    def delete_user(self, value):
        r"""
        Deletes a user from the system by either user ID or username.

        This method sends a `DELETE` request to the server to remove a user. 
        It accepts either the user's ID or username to identify the user. 
        If the user is found and successfully deleted, a success message is displayed. 
        If the user is not found, a not-found message is displayed.

        :param value: 
            The identifier of the user to be deleted. 
            Can be one of the following:
            - User ID (str): A unique numerical identifier for the user.
            - Username (str): The name of the user in the system.

        :return: 
            None. Prints success or failure messages based on the result.
        """

        try:
            request = self.data_manipulation(
                value=value,
                action='DELETE',
                success_message="The user was deleted.",
                not_found_message="The user was not found."
                )
            
            if request:
                logger.info(f"User {value} successfully deleted.")
            else:
                logger.warning(f"Failed to delete user {value}.")

        except Exception as e:
            logger.error(f"Error occurred while deleting user {value}: {e}")
            raise  # Re-raise the exception to handle it higher up

    def enable_user(self, value):
        r"""
        Enables a user by sending a POST request to the server.

        This method sends a POST request to enable a user identified by either their 
        ID or name. It uses the `data_manipulation` method to handle the request and 
        print success or error messages based on the response.

        :param value: 
            The identifier of the user to be enabled (either ID or current name).

        :return: 
            None. The success or error message is printed based on the result of the operation.
        """

        try:
            request = self.data_manipulation(
                value=value,
                action="POST",
                endpoint_suffix="/enable",
                success_message="The user was enabled.",
                not_found_message="The user was not found."
                )
            
            if request:
                logger.info(f"User {value} successfully enabled.")
            else:
                logger.warning(f"Failed to enable user {value}.")

        except Exception as e:
            logger.error(f"Error occurred while enabling user {value}: {e}")
            raise  # Re-raise the exception to handle it higher up
    
    def disable_user(self, value):
        r"""
        Disables a user by sending a POST request to the server.

        This method sends a POST request to disable a user identified by either their 
        ID or name. It uses the `data_manipulation` method to handle the request and 
        print success or error messages based on the response.

        :param value: 
            The identifier of the user to be disabled (either ID or current name).

        :return: 
            None. The success or error message is printed based on the result of the operation.
        """

        try:
            request = self.data_manipulation(
                value=value,
                action="POST",
                endpoint_suffix="/disable",
                success_message="The user was disabled.",
                not_found_message="The user was not found."
                )
            
            if request:
                logger.info(f"User {value} successfully disabled.")
            else:
                logger.warning(f"Failed to disable user {value}.")

        except Exception as e:
            logger.error(f"Error occurred while disabling user {value}: {e}")
            raise  # Re-raise the exception to handle it higher up