from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class DriverFactory:
    download_path = "/home/seluser/Downloads/"
    
    @staticmethod
    def get_chrome_options():
        chrome_options = ChromeOptions()
        chrome_options.add_argument("disable-gpu")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-geolocation")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-web-security")
        prefs = {
            "download.default_directory": DriverFactory.download_path,
            "plugins.plugins_disabled": ["Chrome PDF Viewer"]
        }
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

    @staticmethod
    def get_edge_options():
        edge_options = EdgeOptions()
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-popup-blocking")
        edge_options.add_argument("--disable-geolocation")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-software-rasterizer")
        edge_options.add_argument("--disable-web-security")
        prefs = {
            "download.default_directory": DriverFactory.download_path,
            "plugins.plugins_disabled": ["Chrome PDF Viewer"]
        }
        edge_options.add_experimental_option("prefs", prefs)
        return edge_options

    @staticmethod
    def get_firefox_options():
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("disable-gpu")
        firefox_options.add_argument("--disable-notifications")
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--disable-infobars")
        firefox_options.add_argument("--disable-popup-blocking")
        firefox_options.add_argument("--disable-geolocation")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-software-rasterizer")
        firefox_options.add_argument("--disable-web-security")
        # Set download preferences if needed for Firefox
        firefox_options.set_preference("browser.download.dir", DriverFactory.download_path)
        firefox_options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
        return firefox_options

    @staticmethod
    def get_driver(browser):
        options_map = {
            "chrome": DriverFactory.get_chrome_options,
            "edge": DriverFactory.get_edge_options,
            "firefox": DriverFactory.get_firefox_options
        }

        # Convert browser to lowercase to match dictionary keys
        browser = browser.lower()
        
        if browser in options_map:
            return options_map[browser]()
        else:
            raise ValueError(f"Browser '{browser}' is not supported.")
