import time
from common import findElement, findText
from scripts import Scripts
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class BookingClasses:
    LOAD_MORE_RESULT_BUTTON = (
        "a83ed08757 c21c56c305 bf0537ecb5 f671049264 af7297d90d c0e0affd09"
    )
    HOTEL_CARD = (
        "c82435a4b8.a178069f51.a6ae3c2b40.a18aeea94d.d794b7a0f7.f53e278e95.c6710787a4"
    )
    HOTEL_NAME = "f6431b446c.a15b38c233"
    AMENITY_OUTER = "aee5343fdb"
    AMENITY_INNER = "f419a93f12"
    REVIEW = "a3b8729ab1.e6208ee469.cb2cbb3ccb"
    REVIEW_COUNT = "abf093bdfe.f45d8e4c32.d935416c47"
    COST_PRICE = "abf093bdfe.c73ff05531.e84eb96b1f"
    SELLING_PRICE = "f6431b446c.fbfd7c1165.e84eb96b1f"
    ROOMS_LEFT = "d17181842f"
    TAXES = "abf093bdfe.f45d8e4c32"
    RATING = "a3b8729ab1.d86cee9b25"


def generateBookingUrl(checkin, checkout):
    baseUrl = "https://www.booking.com/searchresults.html?"
    queryParams = {
        "aid": "304142",
        "ss": "New York",
        "ssne": "New York",
        "ssne_untouched": "New York",
        "efdco": "1",
        "lang": "en-us",
        "src": "index",
        "dest_id": "20088325",
        "dest_type": "city",
        "group_adults": "2",
        "no_rooms": "1",
        "group_children": "0",
        "nflt": "price=INR-min-max-1;class=5",
        "checkin": checkin,
        "checkout": checkout,
    }
    return baseUrl + urlencode(queryParams)


def getBookingDataForCheckingInOut(driver, checkIn, checkOut):
    bookingUrlPath = generateBookingUrl(checkIn, checkOut)

    def getAmenities(hotel):
        amenities = []
        outerSpan = findElement(BookingClasses.AMENITY_OUTER, hotel, "span", True)
        for inner in outerSpan:
            container = findElement(BookingClasses.AMENITY_INNER, inner, "span")
            if container.text.strip() != "None":
                amenities.append(container.text.strip())
        return amenities

    driver.get(bookingUrlPath)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    time.sleep(5)
    ActionChains(driver).move_by_offset(0, 0).click().perform()

    lastHeight = driver.execute_script(Scripts.GET_SCROLL_HEIGHT)

    while True:
        driver.execute_script(Scripts.SCROLL_TO_BOTTOM)
        time.sleep(5)
        newHeight = driver.execute_script(Scripts.GET_SCROLL_HEIGHT)
        if lastHeight != newHeight:
            lastHeight = newHeight
            continue
        try:
            loadButtonValue = f"//button[contains(@class, '{BookingClasses.LOAD_MORE_RESULT_BUTTON}')]"
            button = driver.find_element(By.XPATH, loadButtonValue)
            button.click()
        except Exception:
            break

    time.sleep(5)
    hotelsCls = f"div.{BookingClasses.HOTEL_CARD}"
    hotels = driver.find_elements(By.CSS_SELECTOR, hotelsCls)
    hotelDataList = []

    for hotel in hotels:
        try:
            name = findElement(BookingClasses.HOTEL_NAME, hotel)
            rating = findElement(BookingClasses.RATING, hotel, d="0.0\nNone")
            review = findElement(BookingClasses.REVIEW, hotel)
            reviewCount = findElement(BookingClasses.REVIEW_COUNT, hotel, d="0 ctr")
            price = findElement(BookingClasses.SELLING_PRICE, hotel, "span")
            taxes = findElement(BookingClasses.TAXES, hotel)
            refundable = findText(hotel, "Free cancellation")
            reservable = findText(hotel, "No prepayment needed")
            breakfast = findText(hotel, "Breakfast included")
            amenityList = getAmenities(hotel)
            roomsLeft = findElement(BookingClasses.ROOMS_LEFT, hotel, d="temp 0")
            costPriceCls = BookingClasses.COST_PRICE
            costPrice = findElement(costPriceCls, hotel, "span", d=price.text)
            hotelData = {
                "name": name.text.strip(),
                "rating": rating.text.strip().split("\n")[1],
                "review": review.text.strip(),
                "reviewCount": reviewCount.text.strip().split()[0],
                "sellingPrice": price.text.replace("₹", "").strip(),
                "costPrice": costPrice.text.replace("₹", "").strip(),
                "taxes": taxes.text.strip().split()[0],
                "roomsLeft": roomsLeft.text.strip().split()[1],
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
