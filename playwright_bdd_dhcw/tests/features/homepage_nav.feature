Feature: DHCW Home page navigation

  @smoke
  Scenario: Testing Search Functionality in DHCW web application
    Given I open the DHCW home page
    When I click on Search Text box in Home Page and Enter text "Welsh Immunisation System"
    Then I can see a "search results" side heading appear
    And I can see Results appear containing text 'Welsh Immunisation System'

@nav
Scenario Outline: Testing Navigation Functionality using Hyperlinks in DHCW web application
  Given I open the DHCW home page
  When I click on the "<hyperlink>" hyper link
  Then I'm navigated to the page with Title "<expected_title>"

  Examples:
    | hyperlink               | expected_title                     |
    | National Data Resource  | National Data Resource - title      |
    | Secure Data Environment | Secure Data Environment - title     |


@nav
Scenario: Testing Dropdown Functionality in Search options in DHCW web application
  Given I open the DHCW home page
  When I click on the Search options dropdown next to the Search Text Box
  Then I can see the following dropdown options:
    | Option           |
    | Product directory |
    | About us          |
    | Our programmes    |
    | Data              |
    | Contact us        |
    | Join our team     |
    | Staff resources   |


