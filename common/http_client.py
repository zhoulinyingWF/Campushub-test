import requests


class ApiResponse:
    """统一响应包装：同时保留 HTTP 状态码与 Result 业务结构，支持分层断言。"""

    def __init__(self, http_status, body):
        self.http_status = http_status
        self.body = body or {}
        self.code = self.body.get("code")
        self.message = self.body.get("message") or ""
        self.data = self.body.get("data")

    def assert_success(self):
        """断言 HTTP 200 且业务码 code=1，返回自身便于链式取值。"""
        assert self.http_status == 200, (
            f"HTTP状态码异常: {self.http_status}, body={self.body}"
        )
        assert self.code == 1, (
            f"业务失败: code={self.code}, message={self.message}"
        )
        return self

    def assert_business_fail(self, message_contains=None):
        """断言业务失败 code=0，可选校验错误信息关键字。"""
        assert self.code == 0, f"预期业务失败，实际成功: data={self.data}"
        if message_contains:
            assert message_contains in self.message, (
                f"错误信息不匹配: 期望包含[{message_contains}], 实际[{self.message}]"
            )
        return self


class HttpClient:
    """接口请求客户端：base_url 拼接、Token 注入、Result 统一剥壳。"""

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def set_token(self, token):
        """设置/清除 Bearer Token，模拟登录态与未登录态。"""
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        else:
            self.session.headers.pop("Authorization", None)

    def request(self, method, path, *, params=None, json=None):
        resp = self.session.request(
            method,
            f"{self.base_url}{path}",
            params=params,
            json=json,
            timeout=self.timeout,
        )
        try:
            body = resp.json()
        except ValueError:
            raise AssertionError(
                f"响应非JSON: HTTP {resp.status_code}, {resp.text[:200]}"
            )
        return ApiResponse(resp.status_code, body)

    def get(self, path, params=None):
        return self.request("GET", path, params=params)

    def post(self, path, json=None):
        return self.request("POST", path, json=json)

    def put(self, path, json=None):
        return self.request("PUT", path, json=json)
