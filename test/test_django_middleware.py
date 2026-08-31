import pytest

django = pytest.importorskip("django")

from django.conf import settings  # noqa: E402
from django.http import HttpResponse  # noqa: E402
from django.test import RequestFactory  # noqa: E402


@pytest.fixture(scope="module", autouse=True)
def django_settings():
    if not settings.configured:
        settings.configure(DEBUG=True, ALLOWED_HOSTS=["*"])
        django.setup()


def make_middleware():
    from pyinstrument.middleware import ProfilerMiddleware

    return ProfilerMiddleware(lambda request: None)


def stop_profiler(request):
    if hasattr(request, "profiler"):
        request.profiler.stop()


def test_show_callback_is_respected_with_profile_dir(tmp_path):
    from django.test import override_settings

    with override_settings(
        PYINSTRUMENT_PROFILE_DIR=str(tmp_path),
        PYINSTRUMENT_SHOW_CALLBACK=lambda request: False,
    ):
        request = RequestFactory().get("/")
        try:
            make_middleware().process_request(request)
            assert not hasattr(request, "profiler")
        finally:
            stop_profiler(request)


def test_profile_dir_still_profiles_when_callback_allows(tmp_path):
    from django.test import override_settings

    with override_settings(
        PYINSTRUMENT_PROFILE_DIR=str(tmp_path),
        PYINSTRUMENT_SHOW_CALLBACK=lambda request: True,
    ):
        request = RequestFactory().get("/")
        try:
            make_middleware().process_request(request)
            assert hasattr(request, "profiler")
        finally:
            stop_profiler(request)


def test_csp_nonce_is_applied_to_profile_scripts():
    from django.test import override_settings

    nonce_calls = 0

    def get_nonce():
        nonlocal nonce_calls
        nonce_calls += 1
        return 'nonce&"value'

    with override_settings(PYINSTRUMENT_CSP_NONCE=get_nonce):
        request = RequestFactory().get("/?profile")
        middleware = make_middleware()
        try:
            middleware.process_request(request)
            response = middleware.process_response(request, HttpResponse())
        except Exception:
            stop_profiler(request)
            raise

    output = response.content.decode()
    assert nonce_calls == 1
    assert output.count('<script nonce="nonce&amp;&quot;value">') == 2
