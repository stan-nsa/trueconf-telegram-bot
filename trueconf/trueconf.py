# https://<trueconf-server>/api/v3.6/logs/messages?access_token=<token>&sort_order=0&to_call_id=<chat-name>&timezone=0&page_size=100&date_from=2024-09-13%2014:00:00

import requests

# Отключение предупреждени: "InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised."
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class Trueconf:
    server: str
    api_adr: str
    token: str
    api_url: str
    chat: str
    
    def __init__(this, server: str, api_adr: str, token: str, chat: str):
        this.server = server
        this.api_adr = api_adr
        this.token = token
        this.chat = chat
        this.api_url = f"https://{this.server}/{this.api_adr}"

    def get_request_trueconf_api(this, query_str: str) -> dict:
        url = f"{this.api_url}/{query_str}&access_token={this.token}"
        
        print(url)  # For debug
        
        response = requests.get(url, params={"Content-Type": "application/json"}, verify=False)
        
        return response.json()

    def get_chat_messages_data(this, date_from: str = None) -> dict:
        query_str = f"logs/messages?sort_order=0&to_call_id={this.chat}&timezone=0&page_size=100"
        
        if date_from:
            query_str += f"&date_from={date_from}"
        
        data = this.get_request_trueconf_api(query_str=query_str)
        
        return data

