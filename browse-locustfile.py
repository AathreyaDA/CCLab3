from locust import task, run_single_user
from locust import FastHttpUser

class Browse(FastHttpUser):
    host = "http://localhost:5000"
   
    # Define headers once for reuse
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Priority": "u=0, i",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
    }

    @task
    def browse_page(self):
        # Merge default headers with specific request header (Host)
        headers = {**self.default_headers, "Host": "localhost:5000"}
       
        # Perform the GET request
        response = self.client.get("/browse", headers=headers)
       
        # Handle response if needed (logging, assertion, etc.)
        if response.status_code != 200:
            response.failure(f"Request failed with status {response.status_code}")
        else:
            response.success()

if __name__ == "__main__":
    run_single_user(Browse)
