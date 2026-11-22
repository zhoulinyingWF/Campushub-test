class UserApi:
    """用户模块接口对象层：注册 / 登录 / 当前用户。"""

    def __init__(self, client):
        self.client = client

    def register(self, username, password, real_name="自动化测试", **extra):
        payload = {
            "username": username,
            "password": password,
            "realName": real_name,
            **extra,
        }
        return self.client.post("/user/register", payload)

    def login(self, username, password):
        return self.client.post(
            "/user/login", {"username": username, "password": password}
        )

    def me(self):
        return self.client.get("/user/me")
