from datetime import date, datetime
import json
import requests
import time


class AmperJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return o.__dict__


class Backend:
    def __init__(self, token, amper_url):
        self.token = token
        amper_url = amper_url if amper_url.endswith('/') else f'{amper_url}/'
        amper_url = amper_url if not amper_url.startswith('http://') else amper_url.replace('http://', 'https://')
        amper_url = amper_url if amper_url.startswith('https://') else f'https://{amper_url}'
        self.amper_url = amper_url

    def get_authorization_header(self):
        self.validate_jwt_token()
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token["access_token"]}'
        }

    def validate_jwt_token(self):
        # try:
        #     result = jwt.decode(self.token['access_token'], os.environ.get('KEYCLOAK_CLIENT_PUBLIC_KEY'), algorithms=["RS256"])
        #     print(result)
        # except jwt.ExpiredSignatureError:
        #     self.token = requests.request("POST", f'{self.amper_url}auth/token-refresh/', headers=self.get_authorization_header(), data=self.token)
        pass

    def create_log_entry_async(self, severity, message, exception=None):
        print(f'{severity}:{message}')

    def send_products(self, payload):
        try:
            self.create_log_entry_async("INFO", f"About to send {len(payload)} products records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/products-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async("ERROR",
                                            f"FAILURE while sending products after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async("INFO", f"Success while sending products records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async("ERROR", str(e), e)

    def send_product_categories(self, payload):
        try:
            self.create_log_entry_async("INFO", f"About to send {len(payload)} product categories records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/product-categories-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async("ERROR",
                                            f"FAILURE while sending product categories after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async("INFO", f"Success while sending product categories records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async("ERROR", str(e), e)

    def send_product_categories_relation(self, payload):
        try:
            self.create_log_entry_async("INFO", f"About to send {len(payload)} product categories relation records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/product-categories-relation-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async("ERROR",
                                            f"FAILURE while sending product categories relation after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async("INFO", f"Success while sending product categories relation records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async("ERROR", str(e), e)

    def send_accounts(self, payload):
        try:
            self.create_log_entry_async("INFO", f"About to send {len(payload)} accounts records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/accounts-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async("ERROR",
                                            f"FAILURE while sending accounts after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async("INFO", f"Success while sending accounts records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async("ERROR", str(e), e)
