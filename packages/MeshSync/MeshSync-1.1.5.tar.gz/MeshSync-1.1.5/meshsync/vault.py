import httpx


class MeshVault:
    def __init__(self):
        self.vault_storage = {}
        pass

    async def get_secrets(self):
        # Create a Secrets Manager client
        try:
            h = {"Content-Type": "application/json"}
            u = "https://nuivbbqndi.execute-api.us-east-1.amazonaws.com/default/MeshVault-API"
            async with httpx.AsyncClient() as client:
                response = await client.get(u, headers=h)
                response_json = response.json()
                if 'Message' in response_json:
                    return None

                for k, v in response_json.items():
                    self.vault_storage[k] = v

                return self.vault_storage
        except Exception as e:
            print(f"[MeshVault] Error: {e}")
            return None
