
from selenium import webdriver
from selenium.webdriver.support.select import Select


class Hist:

    driver = None
    link_pattern = "http://zq.win007.com/analysis/$GID$cn.htm"
    num_prev_records = 3

    def __init__(self):
        self.driver = webdriver.Chrome()

    # Tick the boxes so that relevant odds become available. The boxes indludes:
    #  1. home-away same
    #  2. select only the given league
    #  3. select maucaoslot as bookie
    #  4. select original 1X2 odds
    def _tick_the_boxes(self, link, lid, bid):
        self.driver.get(link)

        # Tick the 'same home-away' checkbox
        v_t = self.driver.find_element_by_id('v_t')
        self.driver.execute_script("arguments[0].click();", v_t)

        # Only select the league
        for l in self.driver.find_elements_by_name("v_l"):
            if l.get_attribute('id') != str(lid) + '_v':
                self.driver.execute_script("arguments[0].click();", l)

        # Select original odds for Maucao Slot only
        Select(self.driver.find_element_by_id('sSelect_v')).select_by_value(str(bid))
        Select(self.driver.find_element_by_id('sType_v')).select_by_value("0")

    # Select the last three most recent odds
    def get_hist_odds(self, gid, lid, bid):
        self._tick_the_boxes(
            # self.link_pattern.replace('$GID$', str(gid)),
            "file:///Users/wangjiasun/Desktop/hist.htm",
            lid,
            bid
        )

        trs = self.driver.find_elements_by_css_selector('#table_v tr[id]')
        if len(trs) < self.num_prev_records:
            print('*** Only ' + str(len(trs)) + ' previous records available, skipping... ***')
            return

        for row in range(0, 3):
            print('row number is: ' + str(row))
            # print(trs[3].get_attribute('id'))
            tds = trs[row].find_elements_by_tag_name('td')
            print(tds[9].text)
            print(tds[10].find_element_by_tag_name('a').text)
            print(tds[11].text)

    def close(self):
        self.driver.close()