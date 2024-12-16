from golem import actions
from runner import run_test
# import autoit


def make_txt_locator(value):
    return f'//*/label[text() = "{value}"]/following-sibling::*[1]/input'


def get_txt_element(value, seq):  # use for several rows with the same 'label' name
    elements = actions.get_browser().find_elements_by_xpath(f'//*/label[text() = "{value}"]/following-sibling::*[1]/input')
    return elements[seq]


def make_rb_locator(value):  # use for checkboxes as well
    return f'//*/label[contains(text(), "{value}")]/preceding::*[1]'


def make_ddl_locator(value):
    return f'//*/label[text() = "{value}"]/following-sibling::*[1]/select'


def get_ddl_element(value, seq):  # use for several rows with the same 'label' name
    elements = actions.get_browser().find_elements_by_xpath(f'//*/label[text() = "{value}"]/following-sibling::*[1]/select')
    return elements[seq]


def make_date_locator(value):
    return f'//*/label[text() = "{value}"]/following-sibling::*[1]//input'


def get_date_element(day):
    return f'//*[contains(@class,"react-datepicker__week")]/div[text() ="{day}"]'


def test(data):

    # ----------------------------------------Locators: title page------------------------------------------------------

    chk = ("id", "ack_cb")
    btn_next = ("xpath", "//*[@id='main_form']//button[contains(text(),'Next')]")

    # ----------------------------------------Locators: first page------------------------------------------------------

    # text fields:

    txt_first_name = ("xpath", make_txt_locator("First Name"), "First Name")
    txt_middle_name = ("xpath", make_txt_locator("Middle Name"), "Middle Name")
    txt_last_name = ("xpath", make_txt_locator("Last Name"), "Last Name")
    txt_suffix = ("xpath", make_txt_locator("Suffix"), "Suffix")
    txt_previous_married_name = ("xpath", make_txt_locator("Previous Married Name"), "Previous Married Name")
    txt_maiden_name = ("xpath", make_txt_locator("Maiden Name (if applicable)"), "Maiden Name (if applicable)")
    txt_address = ("xpath", make_txt_locator("Address"), "Address")
    txt_city = ("xpath", make_txt_locator("City"), "City")
    txt_zip_code = ("xpath", make_txt_locator("Zip Code"), "Zip Code")
    txt_city_of_birth = ("xpath", make_txt_locator("City of Birth"), "City of Birth")
    txt_county_of_birth = ("xpath", make_txt_locator("County of Birth"), "County of Birth")
    txt_country_of_birth = ("xpath", make_txt_locator("Country of Birth"), "Country of Birth")
    txt_SSN = ("xpath", make_txt_locator("Social Security Number"), "SSN")
    txt_parent_1_name = ("xpath", make_txt_locator("Parent 1 Name"), "Parent 1 Name")
    txt_parent_2_name = ("xpath", make_txt_locator("Parent 2 Name"), "Parent 2 Name")
    # txt_city_of_birth = ("xpath", make_locator(""), "")
    # txt_city_of_birth = ("xpath", make_locator(""), "")

    # radio buttons

    rb_gender = ("xpath", make_rb_locator("Male"), "Gender")
    rb_present_marital_status = ("xpath", make_rb_locator("Single"), "Present Marital Status 1")
    rb_proof_of_age = ("xpath", make_rb_locator("Valid Driver's License"), "Proof of Age")

    # dop-downs

    ddl_state = ("xpath", make_ddl_locator("State"), "State")
    ddl_state_of_birth = ("xpath", make_ddl_locator("State of Birth"), "State of Birth")
    ddl_SSN = ("xpath", make_ddl_locator("I have a valid Social Security Number:"), "I have a valid Social Security Number")

    # dates

    date_picker_of_birth = ("xpath", make_date_locator("Date of Birth"), "Date of Birth date picker")
    date_of_birth = ("xpath", get_date_element(15), "Date of Birth")

    # buttons

    btn_previous_month = ("xpath", '//*//button[text()="Previous Month"]', "Previous Month")
    btn_next_page = ("xpath", "//*/button[text() =  'Next']", "Next Page")

    # checkboxes:

    chk_i_affirm = ("xpath", make_rb_locator("I affirm and certify"), "I affirm and certify : checkbox")

    # --------------------------------------------Fill: title page------------------------------------------------------

    actions.get('https://bouldercountyco.seamlessdocs.com/ng/fa/CO23071000444507881')
    actions.click(chk)
    actions.click(btn_next)

    # -------------------------------------------Test Data--------------------------------------------------------------

    test_data = [
        {"first_name": "RUDOLPH",
         "middle_name": "middle_test",
         "last_name": "FALCON",
         "suffix": "suffix_test",
         "previous_married_name": "previous_test"}, {}]

    # print(test_data[0]["first_name"])

    # ----------------------------------------Fill: first page------------------------------------------------------

    # actions.send_keys(txt_first_name, 'RUDOLPH')
    # actions.send_keys(txt_middle_name, 'middle_test')
    # actions.send_keys(txt_last_name, 'FALCON')
    # actions.send_keys(txt_suffix, 'suffix_test')
    # actions.send_keys(txt_previous_married_name, 'previous_test')
    # actions.send_keys(txt_maiden_name, 'maiden_test')
    # actions.click(rb_gender)
    # actions.send_keys(txt_address, 'test_address')
    # actions.send_keys(txt_city, 'test_city')
    # actions.select_option_by_index(ddl_state, 1)
    # actions.send_keys(txt_zip_code, '44444')
    # actions.click(date_picker_of_birth)
    # actions.wait_for_element_displayed(btn_previous_month)
    # actions.click(btn_previous_month)
    # actions.click(date_of_birth)
    # actions.send_keys(txt_city_of_birth, 'test_city_of_birth')
    # actions.select_option_by_index(ddl_state_of_birth, 2)
    # actions.send_keys(txt_county_of_birth, 'test_county_of_birth')
    # actions.send_keys(txt_country_of_birth, 'test_country_of_birth')
    # actions.select_option_by_index(ddl_SSN, 1)
    # actions.wait_for_element_displayed(txt_SSN)
    # actions.send_keys(txt_SSN, '111-11-1111')
    # actions.click(rb_present_marital_status)
    # actions.send_keys(txt_parent_1_name, 'test_parent_1')
    # actions.send_keys(txt_parent_2_name, 'test_parent_2')
    # actions.click(rb_proof_of_age)
    # actions.send_keys(get_txt_element("City of Residence", 0), 'test1')
    # actions.send_keys(get_txt_element("City of Residence", 1), 'test2')
    # actions.select_option_by_index(get_ddl_element("State of Residence", 0), 1)
    # actions.select_option_by_index(get_ddl_element("State of Residence", 1), 2)
    # actions.click(chk_i_affirm)
    # actions.click(btn_next_page)

    input("\nPress Enter to finish...")



if __name__ == '__main__':
    run_test(__file__)