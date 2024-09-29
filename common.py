from selenium.webdriver.common.by import By


class DefaultWebElement:
    def __init__(self, text=""):
        self.text = text


def findElement(className, element, tag="div", multiple=False, d="None"):
    selector = f"{tag}.{className}" if className else tag
    try:
        if multiple:
            return element.find_elements(By.CSS_SELECTOR, selector)
        else:
            return element.find_element(By.CSS_SELECTOR, selector)
    except Exception:
        return [] if multiple else DefaultWebElement(d)


def findText(element, text):
    return element.find_elements(By.XPATH, f'.//*[text()="{text}"]')
