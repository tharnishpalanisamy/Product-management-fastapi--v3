import httpx 

async def fetch_post(post_id:int) -> dict :
    async with httpx.AsyncClient(timeout=10.0) as client :
        reponse = await client.get(
            f"https://jsonplaceholder.typicode.com/posts/{post_id}",
            headers={
                'Accept' : 'application/json' 
            }
        )
        reponse.raise_for_status() 
        return reponse.json() 
    