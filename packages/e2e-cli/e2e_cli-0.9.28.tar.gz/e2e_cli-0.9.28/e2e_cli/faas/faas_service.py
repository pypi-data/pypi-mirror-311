import json
import os
import shutil
import yaml
from prettytable import PrettyTable

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.apiclient import ApiClient
from e2e_cli.core.helper_service import Checks
from e2e_cli.faas.constants import (DEFAULT_FUNCTION_CONFIG_NAME, DEPLOY_API_ENDPOINT, RUNTIME_LANGUAGE_MAPPING,
                                    GET_ALL_FUNCTION_API_ENDPOINT, DELETE_FUNCTION_API_ENDPOINT,
                                    UPDATE_FUNCTION_API_ENDPOINT)
from e2e_cli.faas.helper_service import HelperService

class FaaSServices:
    def __init__(self, **kwargs):
        self.user_creds = get_user_cred(kwargs.get("alias"))
        self.api_key = self.user_creds[1]
        self.auth_token = self.user_creds[0]
        self.arguments = kwargs.get("arguments")
    
    def caller(self, method):
        allowed_method = {
            "deploy": self.create_function,
            "list": self.list_functions,
            "destroy": self.delete_function,
            "redeploy": self.update_function,
        }
        return allowed_method.get(method)

    def create_function(self):
        function_name = self.arguments.args.name
        current_working_dir = os.getcwd()
        function_path = f"{current_working_dir}/{function_name}"
        try:
            with open(f"{function_path}/{DEFAULT_FUNCTION_CONFIG_NAME}", 'r') as config_file:
                config_data = yaml.safe_load(config_file)
            language = config_data.get("function").get("runtime")
            runtime = RUNTIME_LANGUAGE_MAPPING.inv.get(language)
            code, requirement = HelperService.get_function_details(function_path, language)
        except Exception as e:
            print(f"Error in fetching function details. error--{e}")
            return
        
        api_client = ApiClient(self.api_key, self.auth_token)
        env_var = config_data.get("function").get("environment")
        secrets = config_data.get("function").get("secrets")
        payload = {
            "function": config_data.get("function").get("name"),
            "runtime": runtime,
            "arguments": {}, # need to implement
            "code": code,
            "memory": config_data.get("function").get("limits").get("memory"),
            "timeout": config_data.get("function").get("limits").get("timeout"),
            "params": {}, # need to implement
            "requirements": requirement,
            "environment_variables": env_var if env_var else {},
            "secrets": secrets if secrets else []
        }
        response = api_client.get_response(url=DEPLOY_API_ENDPOINT, method="POST",
                                           payload=payload)
        
        if not response:
            print("There is some error while creating. Kindly try after some time.")
            return
        Checks.status_result(response)
    
    def list_functions(self):
        api_client = ApiClient(self.api_key,self.auth_token)
        response = api_client.get_response(url=GET_ALL_FUNCTION_API_ENDPOINT, method="GET")
        if not response:
            print("There is some error while listing. Kindly try after some time.")
            return
        if response.get("code") != 200:
            Checks.status_result(response)
        function_table = PrettyTable()
        function_table.field_names = ["Function", "Language", "Status", "Invocation Url"]
        function_details = response.get("data")
        for function_detail in function_details:
            function_table.add_row([function_detail.get("name"), function_detail.get("runtime"),
                                  function_detail.get("status"), function_detail.get("url")])
        print(function_table)
    
    def delete_function(self):
        function_name = self.arguments.args.name
        api_client = ApiClient(self.api_key,self.auth_token)
        payload = {"function": function_name}
        response = api_client.get_response(url=DELETE_FUNCTION_API_ENDPOINT.format(
            function_name=function_name), method="DELETE", payload=payload)
        if not response:
            print("There is some error while deleting. Kindly try after some time.")
            return
        if response.get("code") != 200:
            Checks.status_result(response)
        is_delete = input("Would you want to delete function related setup also(y,n): ")
        if is_delete == 'y':
            shutil.rmtree(f"{os.getcwd()}/{function_name}")
        print(f"Your Function named {function_name} is deleted successfully.")

    def update_function(self):
        function_name = self.arguments.args.name
        current_working_dir = os.getcwd()
        function_path = f"{current_working_dir}/{function_name}"
        try:
            with open(f"{function_path}/{DEFAULT_FUNCTION_CONFIG_NAME}", 'r') as config_file:
                config_data = yaml.safe_load(config_file)
            code, requirement = HelperService.get_function_details(function_path, config_data.get("function").get("runtime"))
        except Exception as e:
            print(f"While Updating Error in fetching function details. error--{e}")
            return
        env_var = config_data.get("function").get("environment")
        secrets = config_data.get("function").get("secrets")
        payload = {
            "code": code,
            "params": {}, # need to be implemented
            "requirements": requirement,
            "environment_variables": env_var if env_var else {},
            "secrets": secrets if secrets else []
        }
        api_client = ApiClient(self.api_key,self.auth_token)
        response = api_client.get_response(url=UPDATE_FUNCTION_API_ENDPOINT.format(
            function_name=function_name), method="PUT", payload=payload)
        if not response:
            print("There is some error while updating. Kindly try after some time.")
            return
        Checks.status_result(response)
