from behave import given, when, then
from tests.pages.home_page import HomePage

def _home(context) -> HomePage:
    if not hasattr(context, "home") or context.home is None:
        context.home = HomePage(context.page)
    return context.home

# -------------------- Common Step --------------------
@given("I open the DHCW home page")
def step_open_home_page(context):
    home = _home(context)
    home.open(context.app_cfg.base_url)

# -------------------- Search Box Steps --------------------
@when('I click on Search Text box in Home Page and Enter text "{search_text}"')
def step_search_text(context, search_text):
    _home(context).search(search_text)

@then('I can see a "search results" side heading appear')
def step_verify_search_heading(context):
    _home(context).should_see_search_results("search results")

@then("I can see Results appear containing text '{expected_text}'")
def step_verify_search_results(context, expected_text):
    _home(context).assert_results_containing(expected_text)

# -------------------- Hyperlink Navigation Steps --------------------
@when('I click on the "{hyperlink}" hyper link')
def step_click_hyperlink(context, hyperlink):
    _home(context).click_nav_link(hyperlink)

@then('I\'m navigated to the page with Title "{expected_title}"')
def step_verify_page_title(context, expected_title):
    _home(context).should_have_title(expected_title)

# -------------------- Dropdown Steps --------------------
@when("I click on the Search options dropdown next to the Search Text Box")
def step_click_dropdown(context):
    _home(context).open_search_options_dropdown()

@then("I can see the following dropdown options:")
def step_verify_dropdown_options(context):
    expected_options = [row["Option"] for row in context.table]
    _home(context).assert_dropdown_options(expected_options)
