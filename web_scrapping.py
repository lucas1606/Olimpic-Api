from logging import NullHandler
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
#id = onetrust-accept-btn-handler

class OlimpicScraper:
    def __init__(self) -> None:
        self.url = 'https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/medal-standings.htm'
        self.driver = Chrome()
        self.cookie_btn_id = 'onetrust-accept-btn-handler'
        self.team = {
            "rank": 0,
            "team": 0,
            "gold": 0,
            "silver": 0,
            "bronze": 0,
            "total": 0,
            "total_ranking": 0,
        }
        #self.driver.maximize_window()

    def init_session(self):
        self.driver.get(self.url)

    def accept_cookies(self):
        try:
            cookie_btn = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, self.cookie_btn_id))
            )
        finally:
            actions = ActionChains(self.driver)
            actions.move_to_element(cookie_btn)
            actions.double_click(cookie_btn)
            actions.perform()

    def scrapp_table(self):
        
        num_rows = len(self.driver.find_elements_by_xpath("//*[@id='medal-standing-table']/tbody/tr"))
        num_cols = len(self.driver.find_elements_by_xpath("//*[@id='medal-standing-table']/tbody/tr[1]/td"))
        table =[]
        for row in range(1,(num_rows + 1)):
            team = []
            for col in range(1,(num_cols)):
                xpath = "//*[@id='medal-standing-table']/tbody/tr[{}]/td[{}]".format(row,col)
                cell_text = self.driver.find_element_by_xpath(xpath).text
                if cell_text is not None:
                    team.append(cell_text)
            table.append(team)
        
        return table


wd = OlimpicScraper()
wd.init_session()
try: 
    wd.accept_cookies()
finally:
    wd.get_page_source()

#Código apenas pega apenas o final da tabela