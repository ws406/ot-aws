from bs4 import BeautifulSoup
import re
from lib.crawler.browser_requests import BrowserRequests
import sys
from lib.win007.modules.games_fetcher.basketball_odds_fetcher.abstract_odds_fetcher import AbstractOddsFetcher
import time
import json


class HistGamesFetcher:
    url_season_ids = 'http://nba.nowgoal.com/jsData/LeagueSeason/sea%league_id%.js'
    url_league_info = 'http://nba.nowgoal.com/jsData/matchResult/%season_id%/l%league_id%_1_%year_month%.js'
    odds_fetcher = None

    def __init__(self, odds_fetcher: AbstractOddsFetcher):
        self.odds_fetcher = odds_fetcher
        pass

    def _get_season_ids(self, league_id, num_of_seasons, start_season_offset):
        season_ids_url = str.replace(self.url_season_ids, '%league_id%', str(league_id))
        season_ids_soup = BeautifulSoup(BrowserRequests.get(season_ids_url).text, "lxml")
        league_ids = re.findall('\'([0-9\-]+)\'', season_ids_soup.text)
        if num_of_seasons >= 1:
            return league_ids[start_season_offset:num_of_seasons+start_season_offset]
        else:
            print("num_of_seasons is expected to be a positive int instead of " + str(num_of_seasons))
            sys.exit()

    def _get_all_games_from_a_season(self, season_id, league_id, years_months):
        games = []

        year_from, year_to = str.split(season_id, '-')
        # Get season ids in short year version i.e 17-18
        short_season_id = year_from[-2:] + '-' + year_to[-2:]

        base_league_season_url = str.replace(
            str.replace(self.url_league_info, '%league_id%', str(league_id)),
            '%season_id%',
            short_season_id
        )

        for year_month in years_months :
            url = str.replace(
                    base_league_season_url,
                    '%year_month%',
                    str.replace(
                        str.replace(year_month, '%year_from%', year_from),
                        '%year_to%',
                        year_to
                    )
                )

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

            # 2: get individual game details from games page
            # Please do not try to understand it!!!
            all_games_string = re.findall('arrData = \[(.+?)\];', content)[0]
            #  "289788,1,'2017-10-18 08:00',16,2,102,99,54,38,-1,4.5,216,1,1"
            games_data = re.findall(
                "\[([0-9]*),"                                         # Game Id
                ".+?,"                                                # Don't care
                "'(?:[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})'," # Game datetime played
                "([0-9]{1,2}),"                                       # Home team ID
                "([0-9]{1,2}),"                                       # Away team ID
                "([0-9]{1,3}),"                                       # Home team score
                "([0-9]{1,3}),"                                       # Away team score
                "([0-9]{1,3}),"                                       # Home team ht ranking
                "([0-9]{1,3}),"                                       # Away team ht ranking
                ".+?\]",                                              # Don't care
                all_games_string
            )
            for game_data in games_data:
                game = dict()
                # game['is_played'] = 1 if re.findall(",(-1|0|-14|2),", game_data)[0] == '-1' else 0
                # if game['is_played'] == 0:
                #     print('\t\t\tGame has not been played yet.')
                #     continue

                game['game_id'] = int(game_data[0])
                game['home_team_id'] = int(game_data[1])
                game['away_team_id'] = int(game_data[2])
                game['home_score'] = int(game_data[3])
                game['away_score'] = int(game_data[4])
                game['home_half_score'] = int(game_data[5])
                game['away_half_score'] = int(game_data[6])

                # Calculate game result
                if game['home_score'] > game['away_score']:
                    game['result'] = '1'
                else:
                    game['result'] = '2'

                game.update(shared_game_info)

                # 3. Get more game details and odds from games page
                try:
                    game['kickoff'], \
                    game["home_team_name"], \
                    game["away_team_name"] \
                        = self.odds_fetcher.get_game_metadata(game['game_id'])

                    game["odds"], \
                    game["probabilities"] \
                        = self.odds_fetcher.get_odds(game['game_id'])

                except StopIteration:
                    print("Skip game - " + str(game['game_id']))
                    continue

                games.append(game)
        return games

    def get_hist_games_by_league(self, league_id, num_of_seasons, start_season_offset, year_month):
        season_ids = self._get_season_ids(league_id, num_of_seasons, start_season_offset)
        games = []
        for season_id in season_ids:
            print("\tSeason - " + str(season_id))
            data = self._get_all_games_from_a_season(season_id, league_id, year_month)
            if not data:
                print("\t---Season - " + str(season_id) + ' has no game data available---')
                continue
            file_name = './misc/basketball_all_odds_data/' + data[0]['league_name'] + '-' + season_id + '.json'
            self._write_to_file(file_name, data)
            print(str(len(data)) + ' games saved to ' + file_name)
            games.append(data)

    def _write_to_file(self, file_name, data):
        file = open(file_name, 'w+')
        file.write(json.dumps(data))
        file.close()