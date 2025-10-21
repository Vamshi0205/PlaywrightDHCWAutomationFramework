
import time
from playwright.sync_api import sync_playwright
from framework.core.config import load_config
from framework.core.paths import ARTIFACTS
from tests.pages.home_page import HomePage

def before_scenario(context, scenario):
    context.home = HomePage(context.page)

def before_all(context):
    env = context.config.userdata.get("env", "qa")
    context.app_cfg = load_config(env)

    context._pw = sync_playwright().start()
    context.browser = context._pw.chromium.launch(headless=False)

def before_scenario(context, scenario):
    context.context = context.browser.new_context(
        base_url=context.app_cfg.base_url,
        record_video_dir=str(ARTIFACTS / "videos"),
        viewport={"width": 1366, "height": 768},
    )
    context.page = context.context.new_page()
    context.context.tracing.start(screenshots=True, snapshots=True, sources=True)

def after_scenario(context, scenario):
    ts = time.strftime("%Y%m%d-%H%M%S")
    name = f"{scenario.name}-{ts}".replace(" ", "_")

    try:
        context.context.tracing.stop(path=str(ARTIFACTS / f"{name}.zip"))
    except Exception:
        pass

    if scenario.status == "failed":
        try:
            context.page.screenshot(path=str(ARTIFACTS / f"{name}.png"), full_page=True)
        except Exception:
            pass

    try:
        context.context.close()
    except Exception:
        pass

def after_all(context):
    if hasattr(context, "browser"):
        try: context.browser.close()
        except Exception: pass
    if hasattr(context, "_pw"):
        try: context._pw.stop()
        except Exception: pass
