import argparse
import os
import aiohttp #type: ignore
import asyncio
from getpass import getpass
import json
from dotenv import load_dotenv #type: ignore
from .error_handler import CustomException
from .sign_device import sign_device

def main():
    cli = FlowxCLI()  # Create an instance of the FlowxCLI class
    cli.main()  # Call the instance's main method

async def loading_spinner(msg: str):
    import itertools
    spinner = itertools.cycle(['|', '/', '-', '\\']) # spinner characters
    for _ in range(20): # Loop to simulate loading for 20 iterations
        print(f'\r{msg} {next(spinner)}', end='', flush=True)
        await asyncio.sleep(0.1) # Async sleep for non-blocking behavior

class FlowxCLI:

    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        self.file_path = os.path.join(self.home_dir, ".flowx")
        self._baseurl= "https://flowx-backend.onrender.com/api/v1"


    def main(self):
        parser = argparse.ArgumentParser(description="Flowx_sdk CLI tool")
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Subcommand: init
        subparsers.add_parser('init', help='Initialize Flowx SDK')

        # Subcommand: login
        subparsers.add_parser('login', help='Login to Flowx SDK')

        # Subcommand: signup
        subparsers.add_parser('signup', help='Sign up for Flowx SDK')

        # Subcommand: create
        create_parser = subparsers.add_parser('create', help='Create a resource')
        create_parser.add_argument('--token', required=True, help='API-Token for resource creation')

        args = parser.parse_args()

        if args.command == 'init':
            self.init_flowx()
        elif args.command == "login":
            asyncio.run(self.login("logging in user ..."))
        elif args.command == 'signup':
            asyncio.run(self.signup())
        elif args.command == 'create':
            asyncio.run(self.create_api_token(args.token))

    def check_password_match(self, password: str, confirm_password: str):
        return password == confirm_password
    
    def load_flowx_env(self):
        """Load variables from the .flowx file using dotenv."""
        if os.path.exists(self.file_path):
            load_dotenv(self.file_path) # Load .flowx file as env variables

    def get_access_token(self):
        """Retrieve 'access_token' from the environment."""
        return os.getenv("access_token")

    

    async def signup(self):
        print("Create an account")
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = getpass("Set a password: ")
        confirme_password = getpass("Confirm password")
        if not self.check_password_match(password, confirme_password):
            print("Passwords do not match. Please try again.")
            return
        
        # Proceed with the rest of the signup logic
        print("Passwords match. Proceeding with signup...")

        spinner_task = asyncio.create_task(loading_spinner("Signing up"))

        payload = json.dumps({
            "username": username,
            "email": email,
            "password":password
        })
        headers = ({
            'Content-Type': 'application/json'
        })
        # Make the HTTP request asynchronously using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(self._baseurl+"/users/", headers=headers, data=payload) as response:
                # Ensure the spinner continues during the request
                await spinner_task
                if response.status == 200:
                    print("Account created successfully 👍")

                    # login user automatically
                    await self.login("Login user automatically", username, password)

                    
                else:
                    print(f"Failed to get tokens. HTTP Status: {response.status_code}, Response: {await response.text()}")
    
    async def login(self, loading_msg: str, username=None, password=None):

        # Load .flowx file into the environment
        self.load_flowx_env()

        # Check if access_token is already loaded
        access_token = self.get_access_token()
        if access_token:
            print("User already logged in.")
            return

        if username is None and password is None:
            username = input("Enter username: ")
            password = getpass("Enter password: ")
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = ({
            'Content-Type': 'application/json'
        })
        async with aiohttp.ClientSession() as session:
            async with session.post(self._baseurl+"/auth/", headers=headers, data=payload) as response:
                # Ensure the spinner continues during the request
                await asyncio.create_task(loading_spinner(loading_msg))
                if response.status == 200:
                    print("Logged in successfully 🎉🎉🎉")
                    response_data = await response.json()
                    access_token = response_data.get("access_token") # Extract the short_token

                    if access_token:
                        # Append the access_token to .flowx
                        with open(self.file_path, 'a') as file:
                            file.write(f"access_token= {access_token}\n")
                        print("\n successfully logged in start builing  🚀🚀🚀")
                        return
                    else:
                        print("Unable to log in")

    async def create_api_token(self, api_token_name):

        # Load .flowx file into the environment
        self.load_flowx_env()
        
        hardware_signature = sign_device.generate_hardware_fingerprint() #Get hardware finger print
        access_token = self.get_access_token()
        payload = json.dumps({
            "device_sig": hardware_signature,
            "name": api_token_name
        })
        headers = ({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
            }
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(self._baseurl+"/token/", headers=headers, data=payload) as response:
                # Ensure the spinner continues during the request
                await asyncio.create_task(loading_spinner("Creating API-Token"))
                if response.status == 200:
                    print(f"API-Token created successfully under this name {api_token_name} ✅✅✅")
                    response_data = await response.json()
                    api_token = response_data.get("short_token")

                    if api_token:
                        # Append the short_token to .flowx 
                        with open(self.file_path, 'a') as file:
                            file.write(f"api_token={api_token}\n")
                        print("Environment variable configured accurately 🍌🍌🍌")
                        return
                    else:
                        print("Error in fetching or creating api key")

    def init_flowx(self):
        # Check if Flowx is already initialized
        if self.check_flowx_exists():
            print("⚠️ Flowx already initialized ⚠️")
            return

        # Create the `.flowx` file
        with open(self.file_path, 'w'):
            pass  # This just opens the file and leaves it empty

        if self.check_flowx_exists():
            print("Flowx initialized properly 🚀🚀🚀")
            
        else:
            raise CustomException("Error initializing Flowx", hint="Please check your installation or reinstall")

    def check_flowx_exists(self) -> bool:
        print("ok")
        return os.path.exists(self.file_path)


# Ensure that main() only runs if the script is executed directly
if __name__ == "__main__":
    cli = FlowxCLI()
    cli.main()
