from pydantic import HttpUrl, TypeAdapter

http_url_adapter = TypeAdapter(HttpUrl)


def validate_http_url(url: str) -> HttpUrl:
    return http_url_adapter.validate_python(url)
