from common.basepage import BasePage
from duba.PageObjects.main_page import main_page

"""反馈建议"""


class FeedbackPage(BasePage):
    def pre_open(self):
        self.mp = main_page()
        self.mp.feedback_click()


if __name__ == '__main__':
    page = FeedbackPage()
