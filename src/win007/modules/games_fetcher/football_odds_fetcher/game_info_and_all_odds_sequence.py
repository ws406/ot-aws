from src.win007.modules.games_fetcher.football_odds_fetcher.abstract_odds_fetcher import AbstractOddsFetcher
import re
import datetime
import collections
from pytz import timezone
from collections import defaultdict


class GameInfoAndAllOddsSequence(AbstractOddsFetcher):

    def get_odds(self, gid):
        raw_data = self._get_data_soup_by_gid(gid)
        if raw_data is None:
            raise StopIteration

        try:
            open_final_odds_data = raw_data.text.split('game=Array(')[1].split(');')[0]
            all_odds_data = raw_data.text.split('gameDetail=Array(')[1].split(');')[0]
        except IndexError:
            raise StopIteration

        # Build the regex to extract odds from bids: "((?=80\||115\||281\||177\|)(.*?))"
        regex_pattern = '"((?='
        for key in self.bids.keys():
            regex_pattern += repr(key) + '\|'
            if key != list(self.bids.keys())[-1]:
                regex_pattern += '|'
        regex_pattern += ')(.*?))"'

        # Extract & parse odds data. Return a dictionary
        data_rows = re.finditer(regex_pattern, open_final_odds_data)
        odds = dict()
        probability = dict()
        for data_row in data_rows:
            overload = False
            # Remove trailing and prefixing "
            data_list = data_row.group(1).split('|')
            #print(data_list)
            bookie_name = self.bids[int(data_list[0])]
            matching_id = data_list[1]

            # 2.78 | 3.18 | 2.85 | 02 - 23 17: 58 | 1.00 | 0.95 | 0.98;
            # 2.67 | 3.22 | 2.89 | 02 - 23 16: 11 | 0.96 | 0.96 | 0.99;
            # 2.66 | 3.24 | 2.93 | 02 - 22 23: 12 | 0.96 | 0.96 | 1.00;
            # 2.67 | 3.22 | 2.9 | 02 - 22 00: 39 | 0.96 | 0.96 | 0.99;
            # 2.51 | 3.25 | 3.12 | 02 - 21 16: 33 | 0.90 | 0.97 | 1.07;
            # 2.51 | 3.26 | 3.12 | 02 - 20 16: 44 | 0.90 | 0.97 | 1.07;
            # 2.42 | 3.4 | 3.14 | 02 - 18 03: 11 | 0.87 | 1.01 | 1.08;
            # 2.43 | 3.38 | 3.14 | 02 - 18 02: 16 | 0.87 | 1.01 | 1.08;
            # 2.43 | 3.4 | 3.13 | 02 - 18 01: 18 | 0.87 | 1.01 | 1.07;
            # 2.42 | 3.42 | 3.13 | 02 - 17 23: 42 | 0.87 | 1.02 | 1.07;
            # 2.48 | 3.55 | 2.93 | 02 - 17 00: 26 | 0.89 | 1.06 | 1.00

            try:
                regexResult = re.findall('"' + matching_id + '\^(.+?)"', all_odds_data)
                if regexResult:
                    odds_at_eacch_tick = regexResult[0].split(';')
                else:
                    odds_at_eacch_tick = []
            except IndexError:
                raise StopIteration

            if odds_at_eacch_tick:
                for odds_tick in reversed(odds_at_eacch_tick[:-1]):
                    tmp_array = odds_tick.split('|')
                    tmp_timestamp = self._get_timestamp_from_string(gid, tmp_array[3])
                    # TODO: there must be a better way!!!
                    if bookie_name not in odds:
                        odds[bookie_name] = {}
                    if tmp_timestamp not in odds[bookie_name] or len(odds[bookie_name]) < 2:
                        odds[bookie_name][tmp_timestamp] = {}
                        odds[bookie_name][tmp_timestamp]["1"] = tmp_array[0]
                        odds[bookie_name][tmp_timestamp]["x"] = tmp_array[1]
                        odds[bookie_name][tmp_timestamp]["2"] = tmp_array[2]
                    else:
                        #print(bookie_name, tmp_array)
                        #print(bookie_name, odds[bookie_name][tmp_timestamp])
                        #print(bookie_name, sorted(odds[bookie_name].items()))
                        #print(bookie_name, float(list(collections.OrderedDict(sorted(odds[bookie_name].items())).values())[-2]["1"]), float(odds[bookie_name][tmp_timestamp]["1"]), float(tmp_array[0]))
                        overload = True
                        diff1 = abs(float(list(collections.OrderedDict(sorted(odds[bookie_name].items())).values())[-2]["1"]) - float(odds[bookie_name][tmp_timestamp]["1"]))
                        diff2 = abs(float(list(collections.OrderedDict(sorted(odds[bookie_name].items())).values())[-2]["1"]) - float(tmp_array[0]))
                        if diff1 > diff2:
                            odds[bookie_name][tmp_timestamp]["1"] = tmp_array[0]
                            odds[bookie_name][tmp_timestamp]["x"] = tmp_array[1]
                            odds[bookie_name][tmp_timestamp]["2"] = tmp_array[2]
                        #print(bookie_name, odds[bookie_name][tmp_timestamp])

                    # TODO: there must be a better way!!!
                    if bookie_name not in probability:
                        probability[bookie_name] = {}
                    probability[bookie_name][tmp_timestamp] = {}
                    implied_prob_1 = 1/float(odds[bookie_name][tmp_timestamp]["1"])
                    implied_prob_x = 1/float(odds[bookie_name][tmp_timestamp]["x"])
                    implied_prob_2 = 1/float(odds[bookie_name][tmp_timestamp]["2"])
                    overround = implied_prob_1 + implied_prob_x + implied_prob_2
                    probability[bookie_name][tmp_timestamp]["1"] = implied_prob_1/overround
                    probability[bookie_name][tmp_timestamp]["x"] = implied_prob_x/overround
                    probability[bookie_name][tmp_timestamp]["2"] = implied_prob_2/overround

            #if overload:
                #print(bookie_name, sorted(odds[bookie_name].items()))
        return odds, probability

    def _get_timestamp_from_string(self, gid, datetime_string_in_hk_time):
        kickoff_timestamp = self.get_game_metadata(gid)[0]

        kickoff_datetime = datetime.datetime.fromtimestamp(kickoff_timestamp)

        kickoff_datetime_in_utc = timezone('utc').localize(kickoff_datetime)
        kickoff_datetime_in_hk = kickoff_datetime_in_utc.astimezone(timezone('Hongkong'))

        # Assign the 'year' from kickoff time to the 'tick' as it doesn't have year.
        tmp_date_time_with_year = str (kickoff_datetime_in_hk.year) + '-' + datetime_string_in_hk_time
        # print (tmp_date_time_with_year)
        datetime_in_hk_time = datetime.datetime.strptime (tmp_date_time_with_year, '%Y-%m-%d %H:%M')

        datetime_in_utc = timezone ('Hongkong').localize (datetime_in_hk_time)

        # BUT if the a game is kicked off in Jan 2018 and the odds were given in Dec 2017, assign 2018 is wrong.
        # This is to fix it!
        if datetime_in_utc > kickoff_datetime_in_utc:
            datetime_in_hk_time = datetime.datetime.strptime(
                str(kickoff_datetime_in_hk.year-1) + '-' + datetime_string_in_hk_time,
                '%Y-%m-%d %H:%M'
            )
            datetime_in_utc = timezone('Hongkong').localize(datetime_in_hk_time)


        # Return timestamp in seconds
        return int(int(datetime_in_utc.timestamp()))
if __name__ == '__main__':
    print(GameInfoAndAllOddsSequence ({177: "pin"}).get_odds (1395288))
