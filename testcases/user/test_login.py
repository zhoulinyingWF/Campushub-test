import pytest

from api.user_api import UserApi


@pytest.mark.smoke
class TestLogin:
    """登录接口：正常流 + 异常流。"""

    def test_login_success(self, client, test_user):
        api = UserApi(client)
        resp = api.login(test_user["username"], test_user["password"]).assert_success()
        assert resp.data["token"], "登录成功但未返回token"
        assert resp.data["username"] == test_user["username"]

    def test_login_wrong_password(self, client, test_user):
        api = UserApi(client)
        api.login(test_user["username"], "wrong_password_xxx").assert_business_fail()

    def test_login_user_not_exist(self, client):
        api = UserApi(client)
        api.login("no_such_user_99999", "whatever").assert_business_fail()

    @pytest.mark.parametrize(
        "username,password",
        [("", "Test@123456"), ("someuser", ""), ("", "")],
        ids=["用户名为空", "密码为空", "均为空"],
    )
    def test_login_empty_params(self, client, username, password):
        api = UserApi(client)
        resp = api.login(username, password)
        assert resp.code != 1, f"空参数登录不应成功: {resp.body}"


@pytest.mark.smoke
class TestCurrentUser:
    """当前用户信息：鉴权正反场景。"""

    def test_me_with_token(self, authed_client):
        api = UserApi(authed_client)
        resp = api.me().assert_success()
        assert resp.data["username"], "已登录但未返回用户信息"

    def test_me_without_token(self, client):
        api = UserApi(client)
        resp = api.me()
        assert resp.code != 1, "未携带Token不应获取到用户信息"

    def test_me_with_invalid_token(self, client):
        client.set_token("invalid.token.xxx")
        api = UserApi(client)
        resp = api.me()
        assert resp.code != 1, "非法Token不应获取到用户信息"
