from screens.home_screen import HomeScreen
from screens.item_details_screen import ItemDetailsScreen
from screens.search_screen import SearchScreen


def test_search_donut_and_open_item_details(driver):
    home_screen = HomeScreen(driver)
    home_screen.navigate_home()
    home_screen.open_search()

    search_screen = SearchScreen(driver)
    search_screen.search_for("donut")
    search_screen.select_result("Donut")

    assert ItemDetailsScreen(driver).wait_until_loaded("Details")
