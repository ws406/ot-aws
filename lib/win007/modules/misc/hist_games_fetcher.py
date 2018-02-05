from bs4 import BeautifulSoup
import re
from lib.crawler.browser_requests import BrowserRequests
import sys
from lib.win007.modules.games_fetcher.odds_fetcher_interface import OddsFetcherInterface
from pprint import pprint


class HistGamesFetcher:
    url_season_ids = 'http://info.nowgoal.com/jsData/LeagueSeason/sea%league_id%.js'
    # url_league_info = 'http://zq.win007.com/jsData/matchResult/%season_id%/s%league_id%.js'
    url_league_info = 'http://info.nowgoal.com/jsData/matchResult/%season_id%/s%league_id%.js'
    odds_fetcher = None

    def __init__(self, odds_fetcher: OddsFetcherInterface):
        self.odds_fetcher = odds_fetcher
        pass

    def _get_season_ids(self, league_id, num_of_seasons):
        season_ids_url = str.replace(self.url_season_ids, '%league_id%', str(league_id))


        season_ids_soup = BeautifulSoup(BrowserRequests.get(season_ids_url).text, "lxml")
        league_ids = re.findall('\'([0-9\-]+)\'', season_ids_soup.text)

        if num_of_seasons >= 1:
            return league_ids[:num_of_seasons]
        else:
            print("num_of_seasons is expected to be a positive int instead of " + str(num_of_seasons))
            sys.exit()


    def _get_all_games_from_a_season(self, season_id, league_id, sub_league_id):
        games = []
        if sub_league_id is not None:
            league_id_string = str(league_id) + '_' + str(sub_league_id)
        else:
            league_id_string = str(league_id)
        url = str.replace(
            str.replace(self.url_league_info, '%league_id%', league_id_string),
            '%season_id%',
            str(season_id)
        )
        print(url)
        content = BeautifulSoup(BrowserRequests.get(url).text, "lxml").text
        # Split the content by 'var ', so it breaks into smaller segments
        # segments = re.findall('', content)


        # Step 1: get league details first - this data is sharable
        # Get:
        #   - league_id
        #   - league_name
        #   - season
        #   - results
        #   - league_size ???
        # vars = str.split(content_soup.text, '];')
        # league_info = str.split(vars)
        shared_game_info = dict()
        shared_game_info["league_id"] = league_id
        shared_game_info["season"] = season_id

        league_name_segment = re.findall('arrLeague = \[(.+?)\];', content)[0]
        shared_game_info["league_name"] = re.findall('\'(.+?)\',', league_name_segment)[2]

        league_size_segment = re.findall('arrTeam = \[(.+?)\];', content)[0]
        shared_game_info["size"] = len(re.findall('(\[.+?\])', league_size_segment.split(';')[0]))

        print(shared_game_info)

        # 2: get individual game details from games page
        # Please do not try to understand it!!!
        rounds_segment = re.findall('jh\["R_(\d+)"\] = \[(.+?)\];', content)
        for round_info in rounds_segment:
            rounds = round_info[0]
            print("\t\tRound - " + str(rounds))
            # tmp is like
            #  "1394661,36,-1,'2017-08-12 02:45',19,59,'4-3','2-2','5','12',1.25,0.5,'3','1/1.5',1,1,1,1,0,0,'','5','12'"
            tmp_list = round_info[1].split('],[')
            for tmp in tmp_list:
                game = dict()
                game_details = re.findall("([0-9]*),.+?,(-1|0),.+?,.+?,.+?,'([0-9])-([0-9])','([0-9])-([0-9])'", tmp)[0]

                game['is_played'] = 1 if game_details[1] == '-1' else 0
                if game['is_played'] == 0:
                    print('Game has not been played yet.')
                    continue

                game['game_id'] = int(game_details[0])
                game['home_score'] = int(game_details[2])
                game['away_score'] = int(game_details[3])
                game['home_half_score'] = int(game_details[4])
                game['away_half_score'] = int(game_details[5])

                game['rounds'] = rounds

                # Calculate game result
                if game['home_score'] > game['away_score']:
                    game['result'] = '1'
                elif game['home_score'] == game['away_score']:
                    game['result'] = 'x'
                else:
                    game['result'] = '2'

                game.update(shared_game_info)

                # 3. Get more game details and odds from games page
                game['kickoff'], \
                game['home_team_name'], \
                game['away_team_name'], \
                game['home_team_id'], \
                game['away_team_id'], \
                game['home_team_rank'], \
                game['away_team_rank'] \
                    = self.odds_fetcher.get_game_metadata(game['game_id'])

                game['odds'], game['probability'], game['kelly_rates'] = self.odds_fetcher.get_odds(game['game_id'])
                games.append(game)
            break
        return games

    def get_hist_games_by_league(self, league_id, num_of_seasons, sub_league_id=None):
        games = []
        season_ids = self._get_season_ids(league_id, num_of_seasons)

        for season_id in season_ids:
            print("\tSeason - " + str(season_id))
            games.append(self._get_all_games_from_a_season(season_id, league_id, sub_league_id))
        return games