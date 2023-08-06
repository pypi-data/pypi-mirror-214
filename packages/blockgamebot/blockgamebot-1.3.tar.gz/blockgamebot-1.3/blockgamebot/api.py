import aiohttp

class Scammers:
    def __init__(self, api_key):

        self.key = api_key

        self.urls = {
            "all": f"https://api.nom-nom.link/scammers?key={self.key}",
            "lookup": f"https://api.nom-nom.link/lookup/scammer/ARGUMENTS?key={self.key}",
        }

    async def get_all(self):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self.urls["all"])
            return await resp.json()
    
    
    async def lookup(self, argument):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self.urls["lookup"].replace("ARGUMENTS", argument))
            return await resp.json()
