import log
import pomace

from . import Script


class TruthSocial(Script):
    URL = "https://truthsocial.com"

    def run(self, page: pomace.Page) -> pomace.Page:
        pomace.shared.client.clear_cookies()
        person = pomace.fake.person

        log.info(f"Beginning iteration as {person}")
        page = page.click_register()

        if "birth date" in page:
            page.select_year("1980")
            page = page.click_next(wait=1)

        page.fill_email(person.email)
        return page.click_next(wait=1)

    def check(self, page: pomace.Page) -> bool:
        return "We sent you an email" in page
