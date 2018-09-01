from src.ops.game_qualifier.interface import GameQualifierInterface
from sklearn.externals import joblib
from numpy import matrix
from numpy import array

coefficient = 0.95
threshold = 1.83
benmarkProb = 0.53
# min odds is 1.5
min_return = 0.5

from src.win007.observers.same_direction.qualification_check2 import QualificationCheck


class RF6Leagus(GameQualifierInterface):
	kafka_topic = 'event-new-game'
	rf = None
	data = []
	preferred_team = None
	
	def __init__(self):
		self.rf = joblib.load('./src/ops/game_qualifier/new_rf_6_leagues_no_hkjc.pkl')

	def Operation(self, data1, data2):
            if data1 > 0 and data2 > 0:
                return data1 - data2
            else:
                return 0
	
	def GenerateProbData(self, probList, kickoffTime, side):
		kickoffTimeinLong = int(kickoffTime)
		probOpenTime = 9999999999
		probOpen = 0
		probFinalTime = 0
		probFinal = 0
		prob15minTime = 0
		prob15min = 0
		prob30minTime = 0
		prob30min = 0
		prob60minTime = 0
		prob60min = 0
		prob3hourTime = 0
		prob3hour = 0
		prob6hourTime = 0
		prob6hour = 0
		prob9hourTime = 0
		prob9hour = 0
		prob12hourTime = 0
		prob12hour = 0
		prob18hourTime = 0
		prob18hour = 0
		prob24hourTime = 0
		prob24hour = 0
		prob48hourTime = 0
		prob48hour = 0
		for key, value in probList.items():
                    if key == "final" or key == "open":
                        continue
                    itemTime = int(key)
                    if probOpenTime > itemTime:
                        probOpenTime = itemTime
                        probOpen = value[side]
                    if probFinalTime < itemTime:
                        probFinalTime = itemTime
                        probFinal = value[side]
                    if itemTime >= kickoffTimeinLong - 3 * 60 * 60 and itemTime < kickoffTimeinLong - 60 * 60:
                        if prob60minTime < itemTime:
                            prob60minTime = itemTime
                            prob60min = value[side]
                    if itemTime >= kickoffTimeinLong - 60 * 60 and itemTime < kickoffTimeinLong - 30 * 60:
                        if prob30minTime < itemTime:
                            prob30minTime = itemTime
                            prob30min = value[side]
		data = []
		data.append(probOpen)
		
		index = 0
		if prob60min == 0:
			if probOpenTime > kickoffTimeinLong - 60 * 60:
				data.append(0)
			else:
				data.append(data[index])
		else:
			data.append(prob60min)
		
		index += 1
		if prob30min == 0:
			if probOpenTime > kickoffTimeinLong - 30 * 60:
				data.append(0)
			else:
				data.append(data[index])
		else:
			data.append(prob30min)

		data.append(probFinal)
		return data

	def GenFeatures(self, side, data, match):
            oppoSide = '1'
            if side == '1':
                oppoSide = '2'
            data.append(match['game_id'])
                    
            homeTeamRank = 0
            awayTeamRank = 0
            if match['home_team_rank'] is None or match['home_team_rank'] > 100:
                homeTeamRank = 0
            else:
                homeTeamRank = match['home_team_rank']
            if match['away_team_rank'] is None or match['away_team_rank'] > 100:
                awayTeamRank = 0
            else:
                awayTeamRank = match['away_team_rank']
            if side == '1':
                data.append(homeTeamRank / match['size'])
            else:
                data.append(awayTeamRank / match['size'])

            if side == '1':
                if homeTeamRank == 0 or match['size'] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(awayTeamRank / match['size'], homeTeamRank / match['size']))
            else:
                if awayTeamRank == 0 or match['size'] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(homeTeamRank / match['size'], awayTeamRank / match['size']))
            
            bet365 = self.GenerateProbData(match['probabilities']['bet365'], match['kickoff'], side)
            pinnacle = self.GenerateProbData(match['probabilities']['pinnacle'], match['kickoff'], side)
            will_hill = self.GenerateProbData(match['probabilities']['will_hill'], match['kickoff'], side)
            interwetten = self.GenerateProbData(match['probabilities']['interwetten'], match['kickoff'], side)
            macau_slot = self.GenerateProbData(match['probabilities']['macau_slot'], match['kickoff'], side)

            startIndex = 0

            i = startIndex
            while i < len(bet365):
                data.append(self.Operation(will_hill[i], pinnacle[i])) # 2, 15, 28, 41, 54
                data.append(self.Operation(bet365[i], pinnacle[i])) # 3, 16, 29, 42, 55
                data.append(self.Operation(interwetten[i], pinnacle[i])) # 4, 17, 30, 43, 56
                data.append(self.Operation(macau_slot[i], pinnacle[i])) # 5, 18, 31, 44, 57
                data.append(self.Operation(will_hill[i], bet365[i])) # 7, 20, 33, 46, 59
                data.append(self.Operation(macau_slot[i], bet365[i])) # 9, 22, 35, 48, 61
                data.append(self.Operation(will_hill[i], macau_slot[i])) # 10, 23, 36, 49, 62
                data.append(self.Operation(interwetten[i], bet365[i])) # 8, 21, 34, 47, 60
                data.append(self.Operation(interwetten[i], macau_slot[i])) # 11, 24, 37, 50, 63
                data.append(self.Operation(interwetten[i], will_hill[i]))
                i += 1

            #data.append(macau_slot[0])
            data.append(macau_slot[len(macau_slot) - 1])
            i = 1
            while i < len(macau_slot):
                if macau_slot[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(macau_slot[i - 1], macau_slot[i]))
                i += 1

            #data.append(bet365[0])
            data.append(bet365[len(bet365) - 1])
            i = 1
            while i < len(bet365):
                if bet365[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(bet365[i - 1], bet365[i]))
                i += 1

            data.append(pinnacle[0])
            #data.append(pinnacle[len(pinnacle) - 1])
            i = 1
            while i < len(pinnacle):
                if pinnacle[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(pinnacle[i - 1], pinnacle[i]))
                i += 1

            #data.append(will_hill[0])
            data.append(will_hill[len(will_hill) - 1])
            i = 1
            while i < len(will_hill):
                if will_hill[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(will_hill[i - 1], will_hill[i]))
                i += 1

            data.append(interwetten[0])
            data.append(interwetten[len(interwetten) - 1])



            bet365 = self.GenerateProbData(match['probabilities']['bet365'], match['kickoff'], oppoSide)
            pinnacle = self.GenerateProbData(match['probabilities']['pinnacle'], match['kickoff'], oppoSide)
            will_hill = self.GenerateProbData(match['probabilities']['will_hill'], match['kickoff'], oppoSide)
            interwetten = self.GenerateProbData(match['probabilities']['interwetten'], match['kickoff'], oppoSide)
            macau_slot = self.GenerateProbData(match['probabilities']['macau_slot'], match['kickoff'], oppoSide)

            startIndex = 0

            i = startIndex
            while i < len(bet365):
                data.append(self.Operation(will_hill[i], pinnacle[i])) # 2, 15, 28, 41, 54
                data.append(self.Operation(bet365[i], pinnacle[i])) # 3, 16, 29, 42, 55
                data.append(self.Operation(interwetten[i], pinnacle[i])) # 4, 17, 30, 43, 56
                data.append(self.Operation(macau_slot[i], pinnacle[i])) # 5, 18, 31, 44, 57
                data.append(self.Operation(will_hill[i], bet365[i])) # 7, 20, 33, 46, 59
                data.append(self.Operation(macau_slot[i], bet365[i])) # 9, 22, 35, 48, 61
                data.append(self.Operation(will_hill[i], macau_slot[i])) # 10, 23, 36, 49, 62
                data.append(self.Operation(interwetten[i], bet365[i])) # 8, 21, 34, 47, 60
                data.append(self.Operation(interwetten[i], macau_slot[i])) # 11, 24, 37, 50, 63
                data.append(self.Operation(interwetten[i], will_hill[i]))
                i += 1

            #data.append(macau_slot[0])
            data.append(macau_slot[len(macau_slot) - 1])
            i = 1
            while i < len(macau_slot):
                if macau_slot[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(macau_slot[i - 1], macau_slot[i]))
                i += 1

            #data.append(bet365[0])
            data.append(bet365[len(bet365) - 1])
            i = 1
            while i < len(bet365):
                if bet365[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(bet365[i - 1], bet365[i]))
                i += 1

            #data.append(pinnacle[0])
            data.append(pinnacle[len(pinnacle) - 1])
            i = 1
            while i < len(pinnacle):
                if pinnacle[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(pinnacle[i - 1], pinnacle[i]))
                i += 1

            #data.append(will_hill[0])
            data.append(will_hill[len(will_hill) - 1])
            i = 1
            while i < len(will_hill):
                if will_hill[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(will_hill[i - 1], will_hill[i]))
                i += 1

            data.append(interwetten[0])
            data.append(interwetten[len(interwetten) - 1])



            bet365 = self.GenerateProbData(match['probabilities']['bet365'], match['kickoff'], 'x')
            pinnacle = self.GenerateProbData(match['probabilities']['pinnacle'], match['kickoff'], 'x')
            will_hill = self.GenerateProbData(match['probabilities']['will_hill'], match['kickoff'], 'x')
            interwetten = self.GenerateProbData(match['probabilities']['interwetten'], match['kickoff'], 'x')
            macau_slot = self.GenerateProbData(match['probabilities']['macau_slot'], match['kickoff'], 'x')

            startIndex = 0

            i = startIndex
            while i < len(bet365):
                data.append(self.Operation(will_hill[i], pinnacle[i])) # 2, 15, 28, 41, 54
                data.append(self.Operation(bet365[i], pinnacle[i])) # 3, 16, 29, 42, 55
                data.append(self.Operation(interwetten[i], pinnacle[i])) # 4, 17, 30, 43, 56
                data.append(self.Operation(macau_slot[i], pinnacle[i])) # 5, 18, 31, 44, 57
                data.append(self.Operation(will_hill[i], bet365[i])) # 7, 20, 33, 46, 59
                data.append(self.Operation(macau_slot[i], bet365[i])) # 9, 22, 35, 48, 61
                data.append(self.Operation(will_hill[i], macau_slot[i])) # 10, 23, 36, 49, 62
                data.append(self.Operation(interwetten[i], bet365[i])) # 8, 21, 34, 47, 60
                data.append(self.Operation(interwetten[i], macau_slot[i])) # 11, 24, 37, 50, 63
                data.append(self.Operation(interwetten[i], will_hill[i]))
                i += 1

            #data.append(macau_slot[0])
            data.append(macau_slot[len(macau_slot) - 1])
            i = 1
            while i < len(macau_slot):
                if macau_slot[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(macau_slot[i - 1], macau_slot[i]))
                i += 1

            #data.append(bet365[0])
            data.append(bet365[len(bet365) - 1])
            i = 1
            while i < len(bet365):
                if bet365[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(bet365[i - 1], bet365[i]))
                i += 1

            #data.append(pinnacle[0])
            data.append(pinnacle[len(pinnacle) - 1])
            i = 1
            while i < len(pinnacle):
                if pinnacle[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(pinnacle[i - 1], pinnacle[i]))
                i += 1

            #data.append(will_hill[0])
            data.append(will_hill[len(will_hill) - 1])
            i = 1
            while i < len(will_hill):
                if will_hill[i] == 0:
                    data.append(0)
                else:
                    data.append(self.Operation(will_hill[i - 1], will_hill[i]))
                i += 1

            data.append(interwetten[0])
            data.append(interwetten[len(interwetten) - 1])

            pIndex = 0
            curSide = side
            while pIndex < 3:
                pIndex = pIndex + 1

                if pIndex == 2:
                    curSide = oppoSide
                elif pIndex == 3:
                    curSide = 'x'
                    continue

                bet365 = self.GenerateProbData(match['odds']['bet365'], match['kickoff'], curSide)
                pinnacle = self.GenerateProbData(match['odds']['pinnacle'], match['kickoff'], curSide)
                will_hill = self.GenerateProbData(match['odds']['will_hill'], match['kickoff'], curSide)
                interwetten = self.GenerateProbData(match['odds']['interwetten'], match['kickoff'], curSide)
                macau_slot = self.GenerateProbData(match['odds']['macau_slot'], match['kickoff'], curSide)

                startIndex = 0

                i = startIndex
                while i < len(bet365):
                    if i == 1 or i == 2:
                        i += 1
                        continue
                    data.append(self.Operation(will_hill[i], pinnacle[i])) # 2, 15, 28, 41, 54
                    data.append(self.Operation(bet365[i], pinnacle[i])) # 3, 16, 29, 42, 55
                    data.append(self.Operation(interwetten[i], pinnacle[i])) # 4, 17, 30, 43, 56
                    data.append(self.Operation(macau_slot[i], pinnacle[i])) # 5, 18, 31, 44, 57
                    data.append(self.Operation(will_hill[i], bet365[i])) # 7, 20, 33, 46, 59
                    data.append(self.Operation(macau_slot[i], bet365[i])) # 9, 22, 35, 48, 61
                    data.append(self.Operation(will_hill[i], macau_slot[i])) # 10, 23, 36, 49, 62
                    data.append(self.Operation(interwetten[i], bet365[i])) # 8, 21, 34, 47, 60
                    data.append(self.Operation(interwetten[i], macau_slot[i])) # 11, 24, 37, 50, 63
                    data.append(self.Operation(interwetten[i], will_hill[i]))
                    i += 1

                data.append(macau_slot[0])
                data.append(macau_slot[len(macau_slot) - 1])

                data.append(bet365[0])
                data.append(bet365[len(bet365) - 1])

                data.append(pinnacle[0])
                data.append(pinnacle[len(pinnacle) - 1])

                data.append(will_hill[0])
                data.append(will_hill[len(will_hill) - 1])

                data.append(interwetten[0])
                data.append(interwetten[len(interwetten) - 1])
	
	def is_game_qualified(self, game_data):
		predict = QualificationCheck().is_qualified(game_data)
		dnb_odds = 0
		dc_odds = 0
		favTeamOdds = 0
		if predict == 'x':
			print("trend wrong")
			return False
		if predict == '1':
			dnb_odds = game_data['odds']['bet365']['final']['1'] * (game_data['odds']['bet365']['final']['x'] - 1) / \
					   game_data['odds']['bet365']['final']['x']
			dc_odds = game_data['odds']['bet365']['final']['1'] * game_data['odds']['bet365']['final']['x'] / (
					game_data['odds']['bet365']['final']['1'] + game_data['odds']['bet365']['final']['x'])
			favTeamOdds = game_data['odds']['bet365']['final']['1']
			if self.Returns(favTeamOdds, dnb_odds * coefficient, dc_odds * coefficient) < 0.5:
				print("buy return not enough", self.Returns(favTeamOdds, dnb_odds * coefficient, dc_odds * coefficient))
				return False
			else:
				self.preferred_team = 'home'
				self.data = []
				self.GenFeatures('1', self.data, game_data)
		if predict == '2':
			dnb_odds = game_data['odds']['bet365']['final']['2'] * (game_data['odds']['bet365']['final']['x'] - 1) / \
					   game_data['odds']['bet365']['final']['x']
			dc_odds = game_data['odds']['bet365']['final']['2'] * game_data['odds']['bet365']['final']['x'] / (
					game_data['odds']['bet365']['final']['2'] + game_data['odds']['bet365']['final']['x'])
			favTeamOdds = game_data['odds']['bet365']['final']['2']
			if self.Returns(favTeamOdds, dnb_odds * coefficient, dc_odds * coefficient) < min_return:
				print("away return not enough",
					  self.Returns(favTeamOdds, dnb_odds * coefficient, dc_odds * coefficient))
				return False
			else:
				self.preferred_team = 'away'
				self.data = []
				self.GenFeatures('2', self.data, game_data)
		
		testData = matrix(self.data)
		testArr = testData[:, 1:]
		probability = self.rf.predict_proba(testArr)
		for prob in probability:
			if prob[1] > benmarkProb:
				result_odds, bet_string = self.GetOddsAndMarket(favTeamOdds, dnb_odds, dc_odds)
				return {
					"gid": game_data['game_id'],
					"league_id": game_data['league_id'],
					"league_name": game_data['league_name'],
					"kickoff": game_data['kickoff'],
					"home_team_name": game_data['home_team_name'],
					"away_team_name": game_data['away_team_name'],
					"home_team_id": game_data['home_team_id'],
					"away_team_id": game_data['away_team_id'],
					"preferred_team": self.preferred_team,
					"bet_on_market": bet_string,
					"min_odds_to_bet_on": result_odds
				}
			else:
				print("prob is not enough", prob[1])
				return False
	
	def GetOddsAndMarket(self, favTeamOdds, dnbOdds, dcOdds):
		if favTeamOdds <= threshold:
			return favTeamOdds, 'win'
		elif dnbOdds < 1.5:  # bet 0/0.5
			return (favTeamOdds + dnbOdds) / 2, '-0/0.5'
		elif dcOdds < 1.5:
			return dnbOdds, 'dnb'
		elif dcOdds <= 2:
			return dcOdds, 'double chance'
		else:
			return 1.3, '+0.5'
	
	def Returns(self, favTeamOdds, dnbOdds, dcOdds):
		if favTeamOdds <= threshold:
			return favTeamOdds - 1
		elif dnbOdds < 1.5:  # bet 0/0.5
			return (favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2
		elif dcOdds < 1.5:
			return dnbOdds - 1
		elif dcOdds <= 2:
			return dcOdds - 1
		else:
			return 0
