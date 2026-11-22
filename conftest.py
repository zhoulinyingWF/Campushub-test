import time

import pytest

from api.user_api import UserApi
from common.config_loader import load_config
from common.http_client import HttpClient


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture()
def client(config):
    """未登录态客户端，每个用例独立，避免 Token 串扰。"""
    return HttpClient(config["base_url"], config.get("timeout", 10))


@pytest.fixture(scope="session")
def test_user(config):
    """session 级测试账号：自动注册并登录，测试数据自备，不依赖既有数据。"""
    http = HttpClient(config["base_url"], config.get("timeout", 10))
    api = UserApi(http)
    username = f"autotest_{int(time.time())}"
    password = "Test@123456"
    api.register(username, password).assert_success()
    token = api.login(username, password).assert_success().data["token"]
    return {"username": username, "password": password, "token": token}


@pytest.fixture()
def authed_client(client, test_user):
    """已登录态客户端，自动携带测试用户 Token。"""
    client.set_token(test_user["token"])
    return client
