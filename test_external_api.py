import httpx

response = httpx.get(
    "https://jsonplaceholder.typicode.com/posts/1" , 
    headers={
        'Accept' : 'application/json'
    }
)

response.raise_for_status()
print(response.status_code)
print(response.json())