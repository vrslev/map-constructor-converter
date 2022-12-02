from geodecoder.routes import Routes, parse_routes


def test_parse_routes(routes: Routes, content: str):
    assert parse_routes(content) == routes
