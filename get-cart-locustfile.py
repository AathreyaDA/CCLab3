from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    host = "http://localhost:5000"
    username = "test123"
    password = "test123"
   
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Priority": "u=0, i",
        "Referer": "http://localhost:5000/product/1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    def on_start(self):
        # Perform login once when the test starts
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        self.default_headers["Cookies"] = f"token={self.token}"

    @task
    def view_cart(self):
        # Use a simple GET request with the token in the headers
        response = self.client.get("/cart", headers=self.default_headers)
        # Optionally handle the response (assert or log)
        if response.status_code != 200:
            response.failure(f"Request failed with status {response.status_code}")
        else:
            response.success()

if __name__ == "__main__":
    run_single_user(AddToCart)
