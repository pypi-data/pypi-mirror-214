from urllib import parse
import requests
import traceback


class Telexception:
    def __init__(
        self,
        API_KEY: str,
        USER_ID: int,
        path_to_logs: str = None,
        send_traceback: bool = False,
    ):
        self.USER_ID = USER_ID
        self.API_KEY = API_KEY
        if path_to_logs:
            self.path_to_logs = path_to_logs
        else:
            self.path_to_logs = None
        self.send_traceback = send_traceback
        self.url = f"https://api.telegram.org/bot{self.API_KEY}/sendMessage?chat_id={self.USER_ID}&text="

    def send_message(self, text: str):
        requests.get(self.url + parse.quote(text) + "&parse_mode=HTML")

    def send_file(self):
        url = f"https://api.telegram.org/bot{self.API_KEY}/sendDocument?chat_id={self.USER_ID}"
        with open(self.path_to_logs, "rb") as f:
            requests.post(url, files={"document": f})

    def exception_handler(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not self.send_traceback:
                    self.send_message(
                        f"An exception was raised in function <b>{func.__name__}</b>:\n{str(e)}"
                    )
                else:
                    tb = traceback.format_exc()
                    self.send_message(
                        f"An exception was raised in function <b>{func.__name__}</b>: {str(e)}\nTraceback:\n{tb}"
                    )
                if self.path_to_logs:
                    self.send_file()
                raise e

        return wrapper
