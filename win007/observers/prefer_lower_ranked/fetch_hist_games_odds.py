from ot.win007.models.crawlers.odds.hist import Hist

ho = Hist()
try:
    ho.get_hist_odds(1365346, 60, 80)
    ho.close()
except Exception as inst:
    print(inst)
    ho.close()