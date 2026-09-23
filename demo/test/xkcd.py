import schemathesis

schema = schemathesis.openapi.from_path("api/xkcd/schema.openapi.yaml")
base_url = "http://127.0.0.1:5000"


@schema.auth()
class XkcdAuthProvider:
    def get(self, case: schemathesis.Case, ctx: schemathesis.AuthContext):
        return "super-secret"

    def set(self, case: schemathesis.Case, data: str, ctx: schemathesis.AuthContext):
        case.headers["Authorization"] = f"Bearer {data}"


@schema.parametrize()
def test_api(case: schemathesis.Case):
    case.call_and_validate(base_url=base_url)
