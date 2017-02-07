#!/usr/bin/python3.5

from tweepy import StreamListener
from tweepy import Stream
import tweepy
import os
import json
import time
import random
import datetime

here = os.path.dirname(os.path.abspath(__file__))

f = open(os.path.join(here,'credentials.txt'), 'r')
CONSUMER_KEY = f.readline().strip()
CONSUMER_SECRET = f.readline().strip()
ACCESS_KEY = f.readline().strip()
ACCESS_SECRET = f.readline().strip()
f.close()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

id_str_to_follow = ["112754792"]

prefixe = ["On sent l'amour du journalisme objectif. ", "Affligeant de bêtise. ", "Osef. ", "Comme si on en avait quoi que ce soit à faire. ", "Lol. ", "Et ça se dit journaliste. ", "Non mais sérieusement. ", "Ça doit être ça, oui. "]
suffixe = [", torchon.", ", abruti.", ". Tu veux pas la fermer définitivement ?", " stp.", ". SUPPRIIIIIME.", ". C'est incroyable cette mauvaise foi.", ". Tocards."]
sondages = ["Pas du tout à charge, tranquille ?", "Un sondage bien neutre comme on les aime.", "Wow. On va certainement atteindre un échantillon représentatif avec ça.", "Vous aviez pas plus biaisé comme question ?", "Je crois que la réponse attendue est dans la question. ", "Même les simples sondages vous les faites comme de la merde."]

def insulte():
    case = random.randint(0, int( (len(prefixe)+len(suffixe))*1.2 ) )
    if case < len(suffixe):
        text = "Supprime" + random.choice(suffixe)
    elif case < len(suffixe)+len(prefixe):
        text = random.choice(prefixe) + "Supprime."
    else:
        text = "Supprime."
    return text
    
minutes = random.randint(2,58)
if datetime.date.today().isoweekday() in [6, 7]:
	wakeUpTime = datetime.time(9 + random.randint(0,1), minutes)
else:
	wakeUpTime = datetime.time(7, minutes)
	

class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        if not data["text"].startswith("RT "):
            print(data["user"]["screen_name"], data["text"], "\n")
        if data["retweeted"] == False and data["user"]["id_str"] in id_str_to_follow :
            time.sleep(random.randint(20, 180))
            if "SONDAGE" in data["text"]:
                api.update_status("@"+data["user"]["screen_name"]+" "+random.choice(sondages)+" Supprime.", data["id"])
            else:
                api.update_status("@"+data["user"]["screen_name"]+" "+insulte(), data["id"])
            print("-------HOP, BIM.-------\n")

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
	while True:
		if datetime.datetime.now().time() > wakeUpTime:
			break
		else:
			time.sleep(60*random.randint(10, 45))
	
    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    twitterStream.filter(follow=id_str_to_follow)
