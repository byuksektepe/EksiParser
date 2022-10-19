class Selectors:
    EMAIL_SELECTOR = "//input[@id='username']"
    PASSWORD_SELECTOR = "//input[@id='password']"
    LOGIN_BUTTON_SELECTOR = "//div[@class='actions']/button[@class='btn btn-primary btn-lg btn-block']"

    SEARCH_SELECTOR = "//form[@id='search-form']/input[@id='search-textbox']"
    SEARCH_BUTTON_SELECTOR = "//form[@id='search-form']/button"
    ROBOT_TEST_SELECTOR = "//label[.='insanlık testi']"

    LOGIN_CHECK_SELECTOR = "//nav[@id='top-navigation']//li[contains(@class, 'messages')]"
    MAIN_TITLES_SELECTOR = "//ul[@id='quick-index-nav']//a[not(contains(@class, 'not-index')) and not " \
                           "(contains(@href, 'kenar')) and not(contains(@class, 'dropdown-toggle'))]"

    TOPIC_TITLES_SELECTOR_LEFT = "//div[@id='index-section']//ul[@class='topic-list partial']//li/a"
    TOPIC_TITLES_SELECTOR_RIGHT = "//div[@id='topic']//h1/a"

    SITE_FOOTER_SELECTOR = "//footer[@id='site-footer']"
    TOPIC_TITLE_SELECTOR = "//div[@id='topic']//h1"
    ENTRY_INPUT_SELECTOR = "//textarea[@class='edittextbox with-helpers track-changes']"
    ACCEPT_COOKIES_SELECTOR = "//button[@id='onetrust-accept-btn-handler']"

