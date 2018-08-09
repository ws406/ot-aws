from src.ops.game_qualifier.interface import GameQualifierInterface
from sklearn.externals import joblib

coefficient = 0.95
threshold = 1.83
benmarkProb = 0.53

def CalculateOdds(favTeamOdds, dnbOdds, dcOdds, betString):
    if favTeamOdds <= 1.83:
        betString = 'win'
        return favTeamOdds - 1
    elif dnbOdds < 1.5: # bet 0/0.5
        betString = '-0/0.5'
        return (favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2
    elif dcOdds < 1.5:
        betString = 'dnb'
        return dnbOdds - 1
    elif dcOdds <= 2:
        betString = 'double chance'
        return dcOdds - 1
    else:
        betString = '+0.5'
        return 0.3

def Returns(favTeamOdds, dnbOdds, dcOdds):
    if favTeamOdds <= threshold:
        return favTeamOdds - 1
    elif dnbOdds < 1.5: # bet 0/0.5
        return (favTeamOdds - 1) / 2 + (dnbOdds - 1) / 2
    elif dcOdds < 1.5:
        return dnbOdds - 1
    elif dcOdds <= 2:
        return dcOdds - 1
    else:
        return 0

def Operation(data1, data2):
    #return np.log(data1 / data2)
    #return (data1 - data2) / 100.0
    return data1 - data2

def GenFeatures(side, data, match):
    oppoSide = '1'
    if side == '1':
        oppoSide = '2'
    data.append(match['game_id'])

    macau_slot = GenerateProbData(match['probabilities']['macau_slot'], match['kickoff'], side)
    data.append(macau_slot[0]) # 1
    i = 1
    while i < len(macau_slot):
        if macau_slot[i] == 0:
            data.append(0)
        else:
            data.append(Operation(macau_slot[i - 1], macau_slot[i]))
        i += 1
    bet365 = GenerateProbData(match['probabilities']['bet365'], match['kickoff'], side)
    data.append(bet365[0])
    i = 1
    while i < len(bet365):
        if bet365[i] == 0:
            data.append(0)
        else:
            data.append(Operation(bet365[i - 1], bet365[i]))
        i += 1
    pinnacle = GenerateProbData(match['probabilities']['pinnacle'], match['kickoff'], side)
    data.append(pinnacle[0])
    i = 1
    while i < len(pinnacle):
        if pinnacle[i] == 0:
            data.append(0)
        else:
            data.append(Operation(pinnacle[i - 1], pinnacle[i]))
        i += 1
    will_hill = GenerateProbData(match['probabilities']['will_hill'], match['kickoff'], side)
    data.append(will_hill[0])
    i = 1
    while i < len(will_hill):
        if will_hill[i] == 0:
            data.append(0)
        else:
            data.append(Operation(will_hill[i - 1], will_hill[i]))
        i += 1

    hkjc = GenerateProbData(match['probabilities']['hkjc'], match['kickoff'], side)
    data.append(hkjc[0])
    i = 1
    while i < len(hkjc):
        if hkjc[i] == 0:
            data.append(0)
        else:
            data.append(Operation(hkjc[i - 1], hkjc[i]))
        i += 1

    interwetten = GenerateProbData(match['probabilities']['interwetten'], match['kickoff'], side)
    data.append(interwetten[0])

    if side == '1':
        data.append(1)
    else:
        data.append(0)

    data.append(float(match['rounds']) / float((match['size'] -1) * 2))

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
            data.append(Operation(awayTeamRank / match['size'], homeTeamRank / match['size']))
    else:
        if awayTeamRank == 0 or match['size'] == 0:
            data.append(0)
        else:
            data.append(Operation(homeTeamRank / match['size'], awayTeamRank / match['size']))

class RF6Leagus(GameQualifierInterface):

	kafka_topic = 'event-new-game'
	rf = None
	data = []
	preferred_team = None

	def __init__(self):
		# The ML model used for prediction
		self.rf = joblib.load('./src/ops/game_qualifier/rf_6_leagues.pkl')

	def is_game_qualified(self, game_data):
		# Input data:
		#       game_data is the one single game (only ONE game) in json
            from src.win007.observers.same_direction.qualification_check import QualificationCheck
            predict = QualificationCheck().is_qualified(game_data)
            dnb_odds = 0
            dc_odds = 0
            favTeamOdds = 0
            if predict == 'x':
                return False
            if predict == '1':
                dnb_odds = game_data['odds']['bet365']['final']['1'] * (game_data['odds']['bet365']['final']['x'] - 1) / game_data['odds']['bet365']['final']['x']
                dc_odds = game_data['odds']['bet365']['final']['1'] * game_data['odds']['bet365']['final']['x'] / (game_data['odds']['bet365']['final']['1'] + game_data['odds']['bet365']['final']['x'])
                favTeamOdds = game_data['odds']['bet365']['final']['1']
                if Returns(favTeamOdds, dnb_odds * coefficient, dc_odds * coefficient) < 0.5:
                   return False
                else:
                    self.preferred_team = 'home'
                    GenFeatures('1', self.data, game_data)
            if predict == '2':
                dnb_odds = game_data['odds']['bet365']['final']['2'] * (game_data['odds']['bet365']['final']['x'] - 1) / game_data['odds']['bet365']['final']['x']
                dc_odds = game_data['odds']['bet365']['final']['2'] * game_data['odds']['bet365']['final']['x'] / (game_data['odds']['bet365']['final']['2'] + game_data['odds']['bet365']['final']['x'])
                favTeamOdds = game_data['odds']['bet365']['final']['2']
                if Returns(favTeamOdds, dnb_odds * coefficient, dc_odds * coefficient) < 0.5:
                    return False
                else:
                    self.preferred_team = 'away'
                    GenFeatures('2', self.data, game_data)

                testData = matrix(self.data)
                testArr = testData[:,1:]
                probability = self.rf.predict_proba(testArr)
                for prob in probability:
                    if prob[1] > benmarkProb:
                        betString = None
                        result_odds = CalculateOdds(favTeamOdds, dnb_odds, dc_odds, betString)
                        return {
                            "game_id": game_data['game_id'],
                            "rounds": game_data['rounds'],
                            "league_id": game_data['league_id'],
                            "season": None,
                            "league_name": game_data['league_name'],
                            "kickoff": game_data['kickoff'],
                            "home_team_name": game_data['home_team_name'],
                            "away_team_name": game_data['away_team_name'],
                            "home_team_id": game_data['home_team_id'],
                            "away_team_id": game_data['away_team_id'],
                            "preferred_team": self.preferred_team,
                            "bet_on_market": betString,
                            "min_odds_to_bet_on": result_odds
                        }
                    else:
                        return False

