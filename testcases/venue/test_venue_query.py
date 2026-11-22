import pytest

from api.venue_api import VenueApi


@pytest.mark.smoke
class TestVenueQuery:
    """场地查询：公开接口，覆盖列表、详情、筛选与不存在场景。"""

    def test_venue_list(self, client):
        api = VenueApi(client)
        resp = api.list().assert_success()
        assert isinstance(resp.data, list), "场地列表应返回数组"
        assert len(resp.data) > 0, "场地列表不应为空（请先初始化场地测试数据）"

    def test_venue_detail(self, client):
        api = VenueApi(client)
        venue_id = api.list().assert_success().data[0]["id"]
        resp = api.detail(venue_id).assert_success()
        assert resp.data["id"] == venue_id, "详情返回的场地与请求ID不一致"

    def test_venue_detail_not_exist(self, client):
        api = VenueApi(client)
        resp = api.detail(99999999)
        assert resp.code == 0 or resp.data is None, (
            f"不存在的场地不应返回有效数据: {resp.body}"
        )

    def test_venue_list_keyword_no_match(self, client):
        api = VenueApi(client)
        resp = api.list(keyword="不存在的场地xyz").assert_success()
        assert resp.data == [], "无匹配关键词应返回空列表"

    def test_venue_slots(self, client):
        api = VenueApi(client)
        venue_id = api.list().assert_success().data[0]["id"]
        resp = api.slots(venue_id, "2026-12-01").assert_success()
        assert isinstance(resp.data, list), "时间段应返回数组"
