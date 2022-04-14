# Module that contains the httpx client

import httpx

# Headers for the request
headers = {
  "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
 "accept-language" : "en-US,en;q=0.9",
 "DNT" : "1",
 "Referer" : "https://www.google.com/",
}

# Httpx client
s = httpx.Client(headers=headers, follow_redirects=True)