from constants import STUDENTS_ENROLLED_XPATH1, STUDENTS_ENROLLED_XPATH2, TIME_REQ_XPATH1, TIME_REQ_XPATH2, \
    PAGINATION_BUTTON_XPATH, TIME_TO_WAIT, COURSE_CARD_XPATH, PAGINATION_CONTAINER, TIME_TO_NEXT_PAGE, DIFFICULTY_XPATH, \
    COURSE_CARD_LINK_XPATH, INSTITUTE_XPATH, RATING_XPATH, RECENT_VIEWS_XPATH, TITLE_XPATH, SKILL_XPATH, \
    SUBCOURSE_XPATH, LEARNERS_XPATH
import pandas as pd


def get_students_and_time(path_list, driver):
    element = ''
    for i in range(len(path_list)):
        try:
            element = driver.find_elements('xpath', path_list[i])[0].text
            if element != '':  # we found rating
                break
        except:
            continue
    return element


def get_total_pagination_pages(driver):
    pagination_buttons = driver.find_elements('xpath', PAGINATION_BUTTON_XPATH)
    try:
        span = driver.find_element('xpath',
                                   PAGINATION_BUTTON_XPATH + '[' + str(len(pagination_buttons)) + ']' + '//span')
        total_pages = span.text
        pages = int(total_pages)
    except:
        pages = 1
    return pages


def get_total_courses_in_page(driver):
    driver.implicitly_wait(TIME_TO_WAIT)
    courses = driver.find_elements('xpath', COURSE_CARD_XPATH)
    return courses


def get_text_from_list(list):
    text_arr = []
    for i in range(len(list)):
        txt = list[i].text
        if txt != '':
            text_arr.append(txt)
    return text_arr


def get_value(element_type, xpath, driver):
    try:
        if element_type == 'image':
            return driver.find_element('xpath', xpath).get_attribute('src')
        elif element_type == 'list':
            return get_text_from_list(driver.find_elements('xpath', xpath))
        else:
            element = driver.find_element('xpath', xpath)
            element_txt = element.text
            if not element_txt:
                element_txt = element.get_attribute("innerText")
            if not element_txt:
                element_txt = element.get_attribute("textContent")
            return element_txt
    except:
        return ''


def get_details_from_card(txt):
    x = txt.split('·')
    return {
        'difficulty': x[0].strip(),
        'duration': x[-1].strip(),
    }


def go_to_course(driver):
    data = []
    pages = get_total_pagination_pages(driver)
    print("Total Pages are: " + str(pages))
    for x in range(pages):
        if x + 1 == pages:  # checking if last page is displayed then close program (scraping)
            driver.close()
            break

        if x == 0:
            driver.implicitly_wait(TIME_TO_WAIT)
        elif x != 0:
            # going to next page in pagination
            driver.find_element('xpath',
                                PAGINATION_CONTAINER + '//button[@data-e2e="pagination-controls-next"]').click()
            driver.implicitly_wait(TIME_TO_NEXT_PAGE)  # waiting for next page to load

        links = get_total_courses_in_page(driver)
        print('total links in page no.' + str(x + 1) + ' is : ' + str(len(links)))

        for y in range(len(links)):
            details_from_card = get_details_from_card(get_value('text', COURSE_CARD_XPATH + '[' + str(
                y + 1) + ']' + COURSE_CARD_LINK_XPATH + DIFFICULTY_XPATH, driver))

            driver.find_element('xpath', COURSE_CARD_XPATH + '[' + str(
                y + 1) + ']' + COURSE_CARD_LINK_XPATH).click()  # going to course detail
            driver.implicitly_wait(5)
            driver.switch_to.window(driver.window_handles[1])

            data.append({
                'title': get_value('text', TITLE_XPATH, driver),
                'institute': get_value('text', COURSE_CARD_XPATH
                                       + '[' + str(y + 1) + ']' + COURSE_CARD_LINK_XPATH + INSTITUTE_XPATH, driver),
                'rating': get_value('text', RATING_XPATH, driver).replace("\nstars", ""),
                'recentViews': get_value('text', RECENT_VIEWS_XPATH, driver),
                'studentsEnrolled': get_students_and_time([STUDENTS_ENROLLED_XPATH1, STUDENTS_ENROLLED_XPATH2], driver),
                'timeReq': get_students_and_time([TIME_REQ_XPATH1, TIME_REQ_XPATH2], driver),
                'skills': get_value('list', SKILL_XPATH, driver),
                'learner': get_value('text', LEARNERS_XPATH, driver),
                'difficulty': details_from_card['difficulty'],
                'duration': details_from_card['duration'],
                'subCourse': get_value('text', SUBCOURSE_XPATH, driver),
            })
            print(str(y) + ": " + str(data[-1]))

            pd.DataFrame(data=data).to_csv('coursera.csv')

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    return data
