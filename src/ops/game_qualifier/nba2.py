from src.ops.game_qualifier.interface import GameQualifierInterface
from sklearn.externals import joblib
from numpy import matrix
from numpy import array
import numpy as np
import math
import json

from src.win007.observers.same_direction.nba_qualification_check2 import QualificationCheck

min_odds = 1.5
max_odds = 1.0 + (2.0 / (min_odds - 1))
decayRatio = 0.618
benmarkProb1 = 0.5

class Nba (GameQualifierInterface):
	kafka_topic = 'event-new-game'
	rf = None
	data = []
	preferred_team = None

	def __init__ (self):
		self.rf = joblib.load ('./src/ops/game_qualifier/nba2.pkl')

	def Operation (self, data1, data2):
		number1 = float (data1)
		number2 = float (data2)
		if number1 > 0 and number2 > 0:
			return (number1 - number2) / 100.0
		else:
			return 0

	def Operation1 (self, data1):
		number = float (data1)
		if number > 0:
			return number * number
		else:
			return number

	def GenerateProbData (self, probList, kickoffTime, side):
		kickoffTimeinLong = int (kickoffTime)
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
		for key, value in probList.items ():
			if key == "final" or key == "open":
				continue
			itemTime = int (key)
			if probOpenTime > itemTime:
				probOpenTime = itemTime
				probOpen = value [side]
			if probFinalTime < itemTime:
				probFinalTime = itemTime
				probFinal = value [side]
			if itemTime >= kickoffTimeinLong - 3 * 60 * 60 and itemTime < kickoffTimeinLong - 60 * 60:
				if prob60minTime < itemTime:
					prob60minTime = itemTime
					prob60min = value [side]
			if itemTime >= kickoffTimeinLong - 60 * 60 and itemTime < kickoffTimeinLong - 30 * 60:
				if prob30minTime < itemTime:
					prob30minTime = itemTime
					prob30min = value [side]
		data = []
		data.append (probOpen)

		index = 0
		if prob60min == 0:
			if probOpenTime > kickoffTimeinLong - 60 * 60:
				data.append (0)
			else:
				data.append (data [index])
		else:
			data.append (prob60min)

		index += 1
		if prob30min == 0:
			if probOpenTime > kickoffTimeinLong - 30 * 60:
				data.append (0)
			else:
				data.append (data [index])
		else:
			data.append (prob30min)

		data.append (probFinal)
		return data

	def GenFeatures (self, side, data1, match, teamsDict, teamsRecentDict, teamsHomeDict, teamsAwayDict,
	                 teamsRecentHomeDict, teamsRecentAwayDict, teamsLastDate):
		data = []

		oppoSide = '1'
		if side == '1':
			oppoSide = '2'
		data.append (match ['game_id'])

		pinnacle = self.GenerateProbData (match ['probabilities'] ['pinnacle'], match ['kickoff'], side)
		will_hill = self.GenerateProbData (match ['probabilities'] ['will_hill'], match ['kickoff'], side)
		vcbet = self.GenerateProbData (match ['probabilities'] ['vcbet'], match ['kickoff'], side)
		easybet = self.GenerateProbData (match ['probabilities'] ['easybet'], match ['kickoff'], side)
		skybet = self.GenerateProbData (match ['probabilities'] ['skybet'], match ['kickoff'], side)
		ladbroke = self.GenerateProbData (match ['probabilities'] ['ladbroke'], match ['kickoff'], side)

		allBookieList = []
		allBookieList.append (pinnacle)
		allBookieList.append (vcbet)
		allBookieList.append (will_hill)
		allBookieList.append (easybet)
		allBookieList.append (skybet)
		allBookieList.append (ladbroke)

		startIndex = 0

		i = startIndex
		while i < len (pinnacle):
			if i == 1:
				i += 1
				continue
			data.append (self.Operation (vcbet [i], pinnacle [i]))  #
			data.append (self.Operation (easybet [i], pinnacle [i]))  #
			data.append (self.Operation (skybet [i], pinnacle [i]))  #
			data.append (self.Operation (ladbroke [i], pinnacle [i]))  #
			data.append (self.Operation (will_hill [i], pinnacle [i]))  #

			data.append (self.Operation (easybet [i], vcbet [i]))  #
			data.append (self.Operation (skybet [i], vcbet [i]))  #
			data.append (self.Operation (ladbroke [i], vcbet [i]))  #
			data.append (self.Operation (will_hill [i], vcbet [i]))  #

			data.append (self.Operation (skybet [i], easybet [i]))  #
			data.append (self.Operation (ladbroke [i], easybet [i]))  #
			data.append (self.Operation (will_hill [i], easybet [i]))  #

			data.append (self.Operation (will_hill [i], skybet [i]))  #
			data.append (self.Operation (ladbroke [i], skybet [i]))  #

			data.append (self.Operation (will_hill [i], ladbroke [i]))  #
			i += 1

		for bookie in allBookieList:
			data.append (bookie [0])
			i = 1
			while i < len (bookie):
				if bookie [i] == 0:
					data.append (0)
				else:
					data.append (self.Operation (bookie [i - 1], bookie [i]))
				i += 1

		for item in data:
			data1.append (item)

		if int (match ['home_team_id']) not in teamsDict or int (match ['away_team_id']) not in teamsDict:
			data1.append (0)
			data1.append (0)
			data1.append (0)
			data1.append (0)
			data1.append (0)
			data1.append (0)
			return

		if side == '1':
			favTeamId = int (match ['home_team_id'])
			favTeamTotalMatch = teamsDict [favTeamId] [0] + teamsDict [favTeamId] [1]
			if favTeamTotalMatch > 0 and teamsDict [favTeamId] [0] > 0:
				data1.append (self.Operation1 (teamsDict [favTeamId] [0] / favTeamTotalMatch))
			else:
				data1.append (0)
			data1.append ((favTeamTotalMatch + 1) / 82.0)

			recentWin = 0
			recentTotal = 0
			index = len (teamsRecentDict [favTeamId]) - 1
			for result in teamsRecentDict [favTeamId]:
				if result != -1:
					recentTotal = recentTotal + 1
				if result == 1:
					recentWin = recentWin + 1 * math.pow (decayRatio, index)
			if recentTotal == 0:
				data1.append (0)
			else:
				data1.append (recentWin / recentTotal)

			nonFavTeamId = int (match ['away_team_id'])
			nonFavTeamTotalMatch = teamsDict [nonFavTeamId] [0] + teamsDict [nonFavTeamId] [1]
			if nonFavTeamTotalMatch > 0 and teamsDict [nonFavTeamId] [0] > 0:
				data1.append (self.Operation1 (teamsDict [nonFavTeamId] [0] / nonFavTeamTotalMatch))
			else:
				data1.append (0)
			data1.append ((nonFavTeamTotalMatch + 1) / 82.0)

			recentWin = 0
			recentTotal = 0
			index = len (teamsRecentDict [nonFavTeamId]) - 1
			for result in teamsRecentDict [nonFavTeamId]:
				if result != -1:
					recentTotal = recentTotal + 1
				if result == 1:
					recentWin = recentWin + 1 * math.pow (decayRatio, index)
			if recentTotal == 0:
				data1.append (0)
			else:
				data1.append (recentWin / recentTotal)
		else:
			favTeamId = int (match ['away_team_id'])
			favTeamTotalMatch = teamsDict [favTeamId] [0] + teamsDict [favTeamId] [1]
			if favTeamTotalMatch > 0 and teamsDict [favTeamId] [0] > 0:
				data1.append (self.Operation1 (teamsDict [favTeamId] [0] / favTeamTotalMatch))
			else:
				data1.append (0)
			data1.append ((favTeamTotalMatch + 1) / 82.0)

			recentWin = 0
			recentTotal = 0
			index = len (teamsRecentDict [favTeamId]) - 1
			for result in teamsRecentDict [favTeamId]:
				if result != -1:
					recentTotal = recentTotal + 1
				if result == 1:
					recentWin = recentWin + 1 * math.pow (decayRatio, index)
			if recentTotal == 0:
				data1.append (0)
			else:
				data1.append (recentWin / recentTotal)

			nonFavTeamId = int (match ['home_team_id'])
			nonFavTeamTotalMatch = teamsDict [nonFavTeamId] [0] + teamsDict [nonFavTeamId] [1]
			if nonFavTeamTotalMatch > 0 and teamsDict [nonFavTeamId] [0] > 0:
				data1.append (self.Operation1 (teamsDict [nonFavTeamId] [0] / nonFavTeamTotalMatch))
			else:
				data1.append (0)
			data1.append ((nonFavTeamTotalMatch + 1) / 82.0)

			recentWin = 0
			recentTotal = 0
			index = len (teamsRecentDict [nonFavTeamId]) - 1
			for result in teamsRecentDict [nonFavTeamId]:
				if result != -1:
					recentTotal = recentTotal + 1
				if result == 1:
					recentWin = recentWin + 1 * math.pow (decayRatio, index)
			if recentTotal == 0:
				data1.append (0)
			else:
				data1.append (recentWin / recentTotal)

	def UpdateRecord (self, teamsDict, homeId, awayId, result):
		if result == '1':
			teamsDict [homeId] [0] = teamsDict [homeId] [0] + 1
			teamsDict [awayId] [1] = teamsDict [awayId] [1] + 1
		elif result == '2':
			teamsDict [homeId] [1] = teamsDict [homeId] [1] + 1
			teamsDict [awayId] [0] = teamsDict [awayId] [0] + 1
		else:
			print ("This is totally wrong! There must be a winner")

	def UpdateHomeRecord (self, curDict, curId, result):
		if result == '1':
			curDict [curId] [0] = curDict [curId] [0] + 1
		elif result == '2':
			curDict [curId] [1] = curDict [curId] [1] + 1
		else:
			print ("This is totally wrong! There must be a winner")

	def UpdateAwayRecord (self, curDict, curId, result):
		if result == '1':
			curDict [curId] [1] = curDict [curId] [1] + 1
		elif result == '2':
			curDict [curId] [0] = curDict [curId] [0] + 1
		else:
			print ("This is totally wrong! There must be a winner")

	def UpdateKickoffTime (self, teamsLastDate, homeId, awayId, time):
		teamsLastDate [homeId] [0] = time
		teamsLastDate [awayId] [1] = time

	def UpdateRecentHomeOrAwayRecord (self, teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId, result):
		if result == '1':
			teamsRecentHomeDict [homeId] [0] = teamsRecentHomeDict [homeId] [1]
			teamsRecentHomeDict [homeId] [1] = teamsRecentHomeDict [homeId] [2]
			teamsRecentHomeDict [homeId] [2] = teamsRecentHomeDict [homeId] [3]
			teamsRecentHomeDict [homeId] [3] = teamsRecentHomeDict [homeId] [4]
			teamsRecentHomeDict [homeId] [4] = 1
			teamsRecentAwayDict [awayId] [0] = teamsRecentAwayDict [awayId] [1]
			teamsRecentAwayDict [awayId] [1] = teamsRecentAwayDict [awayId] [2]
			teamsRecentAwayDict [awayId] [2] = teamsRecentAwayDict [awayId] [3]
			teamsRecentAwayDict [awayId] [3] = teamsRecentAwayDict [awayId] [4]
			teamsRecentAwayDict [awayId] [4] = 0
		elif result == '2':
			teamsRecentHomeDict [homeId] [0] = teamsRecentHomeDict [homeId] [1]
			teamsRecentHomeDict [homeId] [1] = teamsRecentHomeDict [homeId] [2]
			teamsRecentHomeDict [homeId] [2] = teamsRecentHomeDict [homeId] [3]
			teamsRecentHomeDict [homeId] [3] = teamsRecentHomeDict [homeId] [4]
			teamsRecentHomeDict [homeId] [4] = 0
			teamsRecentAwayDict [awayId] [0] = teamsRecentAwayDict [awayId] [1]
			teamsRecentAwayDict [awayId] [1] = teamsRecentAwayDict [awayId] [2]
			teamsRecentAwayDict [awayId] [2] = teamsRecentAwayDict [awayId] [3]
			teamsRecentAwayDict [awayId] [3] = teamsRecentAwayDict [awayId] [4]
			teamsRecentAwayDict [awayId] [4] = 1
		else:
			print ("This is totally wrong! There must be a winner")

	def UpdateRecentRecord (self, teamsRecentDict, homeId, awayId, result):
		if result == '1':
			teamsRecentDict [homeId] [0] = teamsRecentDict [homeId] [1]
			teamsRecentDict [homeId] [1] = teamsRecentDict [homeId] [2]
			teamsRecentDict [homeId] [2] = teamsRecentDict [homeId] [3]
			teamsRecentDict [homeId] [3] = teamsRecentDict [homeId] [4]
			teamsRecentDict [homeId] [4] = teamsRecentDict [homeId] [5]
			teamsRecentDict [homeId] [5] = teamsRecentDict [homeId] [6]
			teamsRecentDict [homeId] [6] = teamsRecentDict [homeId] [7]
			teamsRecentDict [homeId] [7] = teamsRecentDict [homeId] [8]
			teamsRecentDict [homeId] [8] = teamsRecentDict [homeId] [9]
			teamsRecentDict [homeId] [9] = 1
			teamsRecentDict [awayId] [0] = teamsRecentDict [awayId] [1]
			teamsRecentDict [awayId] [1] = teamsRecentDict [awayId] [2]
			teamsRecentDict [awayId] [2] = teamsRecentDict [awayId] [3]
			teamsRecentDict [awayId] [3] = teamsRecentDict [awayId] [4]
			teamsRecentDict [awayId] [4] = teamsRecentDict [awayId] [5]
			teamsRecentDict [awayId] [5] = teamsRecentDict [awayId] [6]
			teamsRecentDict [awayId] [6] = teamsRecentDict [awayId] [7]
			teamsRecentDict [awayId] [7] = teamsRecentDict [awayId] [8]
			teamsRecentDict [awayId] [8] = teamsRecentDict [awayId] [9]
			teamsRecentDict [awayId] [9] = 0
		elif result == '2':
			teamsRecentDict [homeId] [0] = teamsRecentDict [homeId] [1]
			teamsRecentDict [homeId] [1] = teamsRecentDict [homeId] [2]
			teamsRecentDict [homeId] [2] = teamsRecentDict [homeId] [3]
			teamsRecentDict [homeId] [3] = teamsRecentDict [homeId] [4]
			teamsRecentDict [homeId] [4] = teamsRecentDict [homeId] [5]
			teamsRecentDict [homeId] [5] = teamsRecentDict [homeId] [6]
			teamsRecentDict [homeId] [6] = teamsRecentDict [homeId] [7]
			teamsRecentDict [homeId] [7] = teamsRecentDict [homeId] [8]
			teamsRecentDict [homeId] [8] = teamsRecentDict [homeId] [9]
			teamsRecentDict [homeId] [9] = 0
			teamsRecentDict [awayId] [0] = teamsRecentDict [awayId] [1]
			teamsRecentDict [awayId] [1] = teamsRecentDict [awayId] [2]
			teamsRecentDict [awayId] [2] = teamsRecentDict [awayId] [3]
			teamsRecentDict [awayId] [3] = teamsRecentDict [awayId] [4]
			teamsRecentDict [awayId] [4] = teamsRecentDict [awayId] [5]
			teamsRecentDict [awayId] [5] = teamsRecentDict [awayId] [6]
			teamsRecentDict [awayId] [6] = teamsRecentDict [awayId] [7]
			teamsRecentDict [awayId] [7] = teamsRecentDict [awayId] [8]
			teamsRecentDict [awayId] [8] = teamsRecentDict [awayId] [9]
			teamsRecentDict [awayId] [9] = 1
		else:
			print ("This is totally wrong! There must be a winner")

	def is_game_qualified (self, file_name, game_data):
		teamsDict = dict ()
		teamsHomeDict = dict ()
		teamsAwayDict = dict ()
		teamsRecentDict = dict ()
		teamsRecentHomeDict = dict ()
		teamsRecentAwayDict = dict ()
		teamsLastDate = dict ()
		curMatchIndex = 0
		with open (file_name) as json_file:
			matches = json.load (json_file)
			for match in matches:
				predict = QualificationCheck ().is_qualified (match)
				homeId = int (match ['home_team_id'])
				awayId = int (match ['away_team_id'])
				kickoffTime = float (match ['kickoff'])
				if homeId not in teamsLastDate:
					results = []
					results.append (0)
					results.append (0)
					teamsLastDate [homeId] = results
				if awayId not in teamsLastDate:
					results = []
					results.append (0)
					results.append (0)
					teamsLastDate [awayId] = results
				if homeId not in teamsDict:
					results = []
					results.append (0)
					results.append (0)
					teamsDict [homeId] = results
				if awayId not in teamsDict:
					results = []
					results.append (0)
					results.append (0)
					teamsDict [awayId] = results
				if homeId not in teamsHomeDict:
					results = []
					results.append (0)
					results.append (0)
					teamsHomeDict [homeId] = results
				if awayId not in teamsAwayDict:
					results = []
					results.append (0)
					results.append (0)
					teamsAwayDict [awayId] = results
				if homeId not in teamsRecentHomeDict:
					results = []
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					teamsRecentHomeDict [homeId] = results
				if awayId not in teamsRecentAwayDict:
					results = []
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					teamsRecentAwayDict [awayId] = results
				if homeId not in teamsRecentDict:
					results = []
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					teamsRecentDict [homeId] = results
				if awayId not in teamsRecentDict:
					results = []
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					results.append (-1)
					teamsRecentDict [awayId] = results
				if choice == 'bottom' and curMatchIndex < 615:
					self.UpdateRecord (teamsDict, homeId, awayId, match ['result'])
					self.UpdateHomeRecord (teamsHomeDict, homeId, match ['result'])
					self.UpdateAwayRecord (teamsAwayDict, awayId, match ['result'])
					self.UpdateRecentHomeOrAwayRecord (teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId,
					                                   match ['result'])
					self.UpdateRecentRecord (teamsRecentDict, homeId, awayId, match ['result'])
					self.UpdateKickoffTime (teamsLastDate, homeId, awayId, kickoffTime)
					curMatchIndex = curMatchIndex + 1
					continue
				if choice == 'top' and curMatchIndex >= 615:
					curMatchIndex = curMatchIndex + 1
					continue
				curMatchIndex = curMatchIndex + 1
				self.UpdateRecord (teamsDict, homeId, awayId, match ['result'])
				self.UpdateHomeRecord (teamsHomeDict, homeId, match ['result'])
				self.UpdateAwayRecord (teamsAwayDict, awayId, match ['result'])
				self.UpdateRecentHomeOrAwayRecord (teamsRecentHomeDict, teamsRecentAwayDict, homeId, awayId,
				                                   match ['result'])
				self.UpdateRecentRecord (teamsRecentDict, homeId, awayId, match ['result'])
				self.UpdateKickoffTime (teamsLastDate, homeId, awayId, kickoffTime)
				continue
		data = []
		predict = QualificationCheck ().is_qualified (game_data)
		if predict == 'x':
			print ("trend wrong")
			return False
		if game_data ['odds'] ['pinnacle'] ['final'] ['1'] < min_odds or game_data ['odds'] ['pinnacle'] ['final'] [
			'2'] < min_odds:
			print ("return not enough", game_data ['odds'] ['pinnacle'] ['final'] ['1'], "vs",
			       game_data ['odds'] ['pinnacle'] ['final'] ['2'])
			return False
		favTeamOdds = 0
		nonFavTeamOdds = 0
		if predict == '1':
			self.preferred_team = 'home'
			game_data ['predict'] = '1'
			self.data = []
			favTeamOdds = game_data ['odds'] ['pinnacle'] ['final'] ['1']
			nonFavTeamOdds = game_data ['odds'] ['pinnacle'] ['final'] ['2']
			self.GenFeatures ('1', self.data, game_data, teamsDict, teamsRecentDict, teamsHomeDict,
			                  teamsAwayDict, teamsRecentHomeDict, teamsRecentAwayDict,
			                  teamsLastDate)
		elif predict == '2':
			self.preferred_team = 'away'
			game_data ['predict'] = '2'
			self.data = []
			favTeamOdds = game_data ['odds'] ['pinnacle'] ['final'] ['2']
			nonFavTeamOdds = game_data ['odds'] ['pinnacle'] ['final'] ['1']
			self.GenFeatures ('2', self.data, game_data, teamsDict, teamsRecentDict, teamsHomeDict,
			                  teamsAwayDict, teamsRecentHomeDict, teamsRecentAwayDict,
			                  teamsLastDate)

		testData = matrix (self.data)
		testArr = testData [:, 1:]
		probability = self.rf.predict_proba (testArr)
		for prob in probability:
			if ((game_data ['predict'] == '1' and prob[1] > match['probabilities']['pinnacle']['final']['1']) or\
                            (game_data ['predict'] == '2' and prob[1] > match['probabilities']['pinnacle']['final']['2'])) and\
			    prob [1] >= benmarkProb1:
				return {
					"gid": game_data ['game_id'],
					"league_id": game_data ['league_id'],
					"league_name": game_data ['league_name'],
					"kickoff": game_data ['kickoff'],
					"home_team_name": game_data ['home_team_name'],
					"away_team_name": game_data ['away_team_name'],
					"home_team_id": game_data ['home_team_id'],
					"away_team_id": game_data ['away_team_id'],
					"preferred_team": self.preferred_team,
					"bet_on_market": 'preferred team win',
					"min_odds_to_bet_on": favTeamOdds
				}
			elif ((game_data ['predict'] == '1' and prob[0] > match['probabilities']['pinnacle']['final']['2']) or\
                              (game_data ['predict'] == '2' and prob[0] > match['probabilities']['pinnacle']['final']['1'])) and\
                              prob [0] >= benmarkProb1:
				return {
					"gid": game_data ['game_id'],
					"league_id": game_data ['league_id'],
					"league_name": game_data ['league_name'],
					"kickoff": game_data ['kickoff'],
					"home_team_name": game_data ['home_team_name'],
					"away_team_name": game_data ['away_team_name'],
					"home_team_id": game_data ['home_team_id'],
					"away_team_id": game_data ['away_team_id'],
					"preferred_team": self.preferred_team,
					"bet_on_market": 'preferred team lose',
					"min_odds_to_bet_on": nonFavTeamOdds
				}
			else:
				print ("prob does not qualify", prob)
				return False
