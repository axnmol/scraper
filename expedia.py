import time
from common import findElement, findText
from scripts import Scripts
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class ExpediaClasses:
    HOTEL_CARD = "uitk-card-content-section.uitk-card-content-section-padded.uitk-layout-grid-item.uitk-layout-grid-item-has-column-start-by-medium"
    HOTEL_NAME = "uitk-heading.uitk-heading-5.overflow-wrap.uitk-layout-grid-item.uitk-layout-grid-item-has-row-start"
    AMENITY = "uitk-text.truncate-lines-2.uitk-type-200.uitk-text-default-theme"
    REVIEW = "uitk-text.uitk-type-300.uitk-type-medium.uitk-text-emphasis-theme"
    REVIEW_COUNT = "uitk-text.uitk-type-200.uitk-type-regular.uitk-text-default-theme"
    SELLING_PRICE = "uitk-text.uitk-type-500.uitk-type-medium.uitk-text-emphasis-theme"
    ROOMS_LEFT = "uitk-badge-text"
    TOTAL = "uitk-text.uitk-type-end.uitk-type-200.uitk-text-default-theme"
    RATING = "uitk-badge-base-text"


def generateExpediaUrl(checkin, checkout):
    baseUrl = "https://www.expedia.co.in/Hotel-Search?"
    queryParams = {
        "adults": 2,
        "d1": checkin,
        "d2": checkout,
        "destination": "New York",
        "endDate": checkout,
        "regionId": "178293",
        "rooms": 1,
        "sort": "RECOMMENDED",
        "startDate": checkin,
        "useRewards": "false",
    }
    return baseUrl + urlencode(queryParams) + "$star=5&star=50"


def getExpediaDataForCheckingInOut(driver, checkIn, checkOut):
    expediaUrlPath = generateExpediaUrl(checkIn, checkOut)

    def getTaxes(totalCls, hotel, price):
        try:
            divs = findElement(totalCls, hotel, multiple=True)
            for div in divs:
                strs = div.text.split()
                if len(strs) == 2:
                    total = int(strs[0].replace("₹", "").replace(",", "").strip())
                    return total - int(price.replace("₹", "").replace(",", "").strip())
            return 0
        except Exception:
            return 0

    def getAmenities(amenitiesCls, hotel):
        amenities = []
        divs = findElement(amenitiesCls, hotel, multiple=True)
        for div in divs:
            if div.text.strip() != "Breakfast included":
                amenities.append(div.text.strip())
        return amenities

    driver.get(expediaUrlPath)
    driver.set_window_size(800, 1000)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    time.sleep(5)
    ActionChains(driver).move_by_offset(0, 0).click().perform()
    time.sleep(5)
    lastHeight = driver.execute_script(Scripts.GET_SCROLL_HEIGHT)

    while True:
        driver.execute_script(Scripts.SCROLL_TO_BOTTOM)
        time.sleep(5)
        newHeight = driver.execute_script(Scripts.GET_SCROLL_HEIGHT)
        if lastHeight != newHeight:
            lastHeight = newHeight
            continue
        else:
            break

    time.sleep(5)
    hotelsCls = f"div.{ExpediaClasses.HOTEL_CARD}"
    hotels = driver.find_elements(By.CSS_SELECTOR, hotelsCls)
    hotelDataList = []

    for hotel in hotels:
        try:
            name = findElement(ExpediaClasses.HOTEL_NAME, hotel, "h3")
            rating = findElement(ExpediaClasses.RATING, hotel, "span")
            review = findElement(ExpediaClasses.REVIEW, hotel, "span")
            reviewCountCls = ExpediaClasses.REVIEW_COUNT
            reviewCount = findElement(reviewCountCls, hotel, "span", d="0 ctr")
            price = findElement(ExpediaClasses.SELLING_PRICE, hotel)
            taxes = getTaxes(ExpediaClasses.TOTAL, hotel, price.text)
            refundable = findText(hotel, "Fully refundable")
            reservable = findText(hotel, "Reserve now, pay later")
            breakfast = findText(hotel, "Breakfast included")
            amenityList = getAmenities(ExpediaClasses.AMENITY, hotel)
            roomsLeft = findElement(ExpediaClasses.ROOMS_LEFT, hotel, "span").text
            roomsLeft = roomsLeft.strip().split()[2] if "We have" in roomsLeft else 0
            costPrice = findElement("", hotel, "del", d=price.text)
            hotelData = {
                "name": name.text.strip(),
                "rating": rating.text.strip(),
                "review": review.text.strip(),
                "reviewCount": reviewCount.text.strip().split()[0],
                "sellingPrice": price.text.replace("₹", "").strip(),
                "costPrice": costPrice.text.replace("₹", "").strip(),
                "taxes": taxes,
                "roomsLeft": roomsLeft,
                "checkIn": checkIn,
                "checkOut": checkOut,
                "refundable": bool(refundable),
                "reservable": bool(reservable),
                "breakfast": bool(breakfast),
                "amenities": amenityList,
            }
            hotelDataList.append(hotelData)

        except Exception as e:
            print(name)
            print(f"Error processing hotel: {e}")
    return hotelDataList
