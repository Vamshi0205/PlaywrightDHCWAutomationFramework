import pytest, os, time
from pathlib import Path
from playwright.sync_api import sync_playwright
from framework.core.paths import ARTIFACTS
from framework.core.config import load_config
from . import register_cli


def pytest_addoption(parser):
    register_cli(parser)

@pytest.fixture(scope="session")
def config(pytestconfig):
    env = pytestconfig.getoption("--env") or "qa"
    cfg = load_config(env)
    print(f"Using config env={env} base_url={cfg.base_url}")
    return cfg

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance, pytestconfig):
    headed = bool(pytestconfig.getoption("--headed"))
    browser = playwright_instance.chromium.launch(headless=not headed)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser, config, request):
    # Create per-test context & page; start tracing
    context = browser.new_context(base_url=config.base_url, record_video_dir=str(ARTIFACTS / "videos"))
    page = context.new_page()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield page
    # Teardown with failure-aware attachments
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False
    ts = time.strftime("%Y%m%d-%H%M%S")
    name = f"{request.node.name}-{ts}"
    trace = ARTIFACTS / f"{name}.zip"
    if failed:
        png = ARTIFACTS / f"{name}.png"
        try:
            page.screenshot(path=str(png), full_page=True)
            print(f"Saved failure screenshot: {png}")
        except Exception as e:
            print(f"Screenshot failed: {e}")
    try:
        context.tracing.stop(path=str(trace))
        print(f"Saved trace: {trace}")
    except Exception as e:
        print(f"Trace stop failed: {e}")
    context.close()

# Hook to know if test failed (so page fixture can react)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
