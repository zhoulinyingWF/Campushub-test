class VenueApi:
    """场地模块接口对象层：列表 / 详情 / 时间段 / 热门排行。"""

    def __init__(self, client):
        self.client = client

    def list(self, **query):
        return self.client.get("/venue/list", params=query or None)

    def detail(self, venue_id):
        return self.client.get(f"/venue/{venue_id}")

    def slots(self, venue_id, date):
        return self.client.get(f"/venue/{venue_id}/slots", params={"date": date})

    def hot(self, limit=10):
        return self.client.get("/venue/hot", params={"limit": limit})
