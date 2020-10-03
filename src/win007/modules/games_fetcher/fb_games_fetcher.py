from bs4 import BeautifulSoup
import re
from src.utils.browser_requests import BrowserRequests
from pytz import timezone
from src.win007.modules.games_fetcher.football_odds_fetcher.abstract_odds_fetcher import AbstractOddsFetcher
import datetime
from src.utils.logger import OtLogger
from multiprocessing import Pool
import multiprocessing
from src.win007.modules.games_fetcher.football_odds_fetcher.game_info_and_all_odds_sequence import GameInfoAndAllOddsSequence


class GamesFetcher:
    url_games_list = 'http://op1.win007.com/index.aspx'
    # url_games_list = 'http://op1.win007.com/nextodds/cn/20181023.html'

    odds_fetcher = None

    def __init__(self, odds_fetcher: AbstractOddsFetcher, logger:OtLogger):
        self.logger = logger
        self.odds_fetcher = odds_fetcher
        pass

    def get_games_by_kickoff(self, minutes):
        return self._get_games_with_conditions(minutes)

    def get_games_by_kickoff_and_league(self, minutes, league_ids):
        return self._get_games_with_conditions(minutes, league_ids)

    def _get_games_with_conditions(self, minutes, league_ids=None):
        try:
            response = BrowserRequests.get(self.url_games_list, self.logger)
        except:
            self.logger.exception("Can't process url - " + self.url_games_list)
            return False

        soup = BeautifulSoup(response.content.decode('gb2312', 'ignore'), "html5lib")
        game_rows = soup.findAll("tr", {"id": re.compile('tr_[0-9]{1,2}')})

        # Then time range
        time_slot_ends_at = (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).timestamp()

        games_rows_to_get_details = []
        for row in game_rows:
            tds = row.findAll("td")

            game = dict()
            game["game_id"] = self._get_game_id(tds)
            game["league_id"] = self._get_league_id(tds)
            game["kickoff"] = self._get_kickoff_time(tds)
            if game["kickoff"] > time_slot_ends_at:
                break

            if league_ids is not None and game["league_id"] not in league_ids:
                continue

            games_rows_to_get_details.append(game)

        self.logger.log(str(len(games_rows_to_get_details)) + " games to get odds for using multi-processing")
        start_time_m = datetime.datetime.now()
        with Pool(multiprocessing.cpu_count()) as p:
            # games = p.map(get_details_func, games_rows_to_get_details)
            games = p.map(self._get_details, games_rows_to_get_details)
        end_time_m = datetime.datetime.now()
        time_taken_m = end_time_m - start_time_m
        self.logger.log("Multi - Time taken to process " + str(len(games_rows_to_get_details)) + " games is " + str(time_taken_m))

        # Keep the single-process code in case issues with multi-processes
        # self.logger.log(str(len(games_rows_to_get_details)) + " games to get odds for using single-processing")
        # start_time_s = datetime.datetime.now()
        # games = []
        # for game in games_rows_to_get_details:
        #     games.append(self._get_details(game))
        #
        # end_time_s = datetime.datetime.now()
        # time_taken_s = end_time_s - start_time_s
        # self.logger.log("Single - Time taken to process " + str(len(games_rows_to_get_details)) + " games is " + str(time_taken_s))

        return games

    def _get_details(self, game):

        gid = game["game_id"]

        try:
            no_use_kickoff_time, \
            game["home_team_name"], \
            game["away_team_name"], \
            game["home_team_id"], \
            game["away_team_id"], \
            game["home_team_rank"], \
            game["away_team_rank"], \
            game["league_name"] \
                        = self.odds_fetcher.get_game_metadata(gid)

            game["odds"], \
            game["probabilities"] \
                = self.odds_fetcher.get_odds(gid)

        except StopIteration:
            pass

        self.odds_fetcher.clean_cached_game_data(gid)
        # Return game details
        return game


    def _get_league_id(self, tds):
        # Extract league_id
        league_info_a = tds[1].find("a")
        if league_info_a:
            try:
                league_id = int(re.search('.[=|/]([0-9]+)', league_info_a.attrs['href']).group(1))
            except AttributeError as ae:
                self.logger.exception("error while extracting 'league id'")
                raise ae
        else:
            league_id = None

        return league_id

    # def _get_league_name(self, tds):
    #     # Extract league_name
    #     league_info_a = tds[1].find("a")
    #     if league_info_a:
    #         league_name = league_info_a.text.strip()
    #     else:
    #         league_name = tds[1].text.strip()
    #
    #     return league_name

    def _get_kickoff_time(self, tds):
        try:
            datetime_obj = datetime.datetime.strptime(tds[2].text.strip(), '%y-%m-%d%H:%M')
            kickoff = timezone('Asia/Chongqing').localize(datetime_obj)
            rtn = kickoff.timestamp()
        except AttributeError as ae:
            self.logger.log("error while extracting 'kickoff'")
            raise ae

        return rtn

    def _get_game_id(self, tds):
        # Extract game_id
        try:
            game_id = int(re.search('/([0-9]+).', tds[12].find("a").attrs['href']).group(1))
        except AttributeError as ae:
            self.logger.exception("error while extracting 'game id'")
            raise ae

        return game_id

if __name__ == '__main__':
    bids = {
        281: "bet365",  # Bet365
        177: "pinnacle",  # Pinnacle
        81:  "betvictor",  # Bet Victor
        82: "ladbroke",

        # 80: "macau_slot",  # Macao Slot
        # 90: "easybet",  # EasyBet
        # 545: "sb",
        # 474: "sbobet",
        # 115: "will_hill",  # WH
        # 432: "hkjc",  # HKJC
        # 104: "interwetten"  # Interwetten
        # 156: "betfred",
        # 110: "snai",
        # 463: "betclick",
        # 167: "skybet",
        # 88: "coral",
        # 936: "setantabet",
        # 961: "championsbet",
        # 527: "tipico",
        # 136: "bodog",
        # 874: "bovada",
        # 695: "cashpoint",
        # 354: "boylesports",
        # 315: "victory",
        # 482: "betway",
        # 808: "betcity",
        # 798: "dafabet",
        # 255: "bwin",
        # 2: "betfair",
    }

    logger = OtLogger('/Users/wangjias/Documents/wsun/ot-aws/logs/ops_true_odds_dev.log')
    odds_fetcher = GameInfoAndAllOddsSequence(bids, logger)
    game_fetecher = GamesFetcher(odds_fetcher, logger)

    game_fetecher.get_games_by_kickoff(200)

