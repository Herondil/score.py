# -*- coding: utf-8 -*-
# Programme de comptage de points
#
# Par Double Z & Herondil
# =============================================

import irclib
import ircbot

score = {}

nick = "Score"
description = "Bot de comptage de points en Python via ircBot"
room = "#scoreTest"
server = "irc.worldnet.net"
port = 6667
utilisateurs = ["Admin"]

score = {}

def modifScore(genre,nom,nbr):
  global score
  
  if genre == "add":
    try :
      score[nom]+=int(nbr)
    except :
      score[nom]=int(nbr)
      
  if genre == "sub":
    try :
      score[nom]-=int(nbr)
    except :
      score[nom]=-int(nbr)
      
  if genre == "set":
    score[nom] = int(nbr)
    
  if score[nom] == 0 :
    score.pop(nom)
      
   

class BotScore(ircbot.SingleServerIRCBot):
  def __init__(self):
    global nick
    global room
    global server
    global port
    
    ircbot.SingleServerIRCBot.__init__(self, [(server, port)],nick,description)
    
  def on_welcome(self,serv,ev):
    serv.join(room)
    
  def on_pubmsg(self,serv,ev):
    global score
    auteur = irclib.nm_to_n(ev.source())
    canal = ev.target()
    message = ev.arguments()[0].split(" ")
    nom = ""
    nbr = 0
    
    try :
      nbr = message[2]
    except :
      nbr = 1
      
    try :
      nom = message[1]
    except :
      for i in utilisateurs:
	if i == auteur :
	  if message[0] != "!score" and message[0][0] == "!" :
	    serv.privmsg(canal,"Erreur de commande")
	    nom = "érreur"	#orthographe volontairement fausse pour caser un caractere interdit dans les nick sur IRC
    
    try :
      for i in utilisateurs:
	if i == auteur :
	  if nom != "érreur" :	
	    if message[0] == "!add" :
	      modifScore("add",nom,nbr)
	      serv.privmsg(canal,str(nbr) + " points donné à " + nom)
	      
	    if message[0] == "!sub" :
	      modifScore("sub",nom,nbr)
	      serv.privmsg(canal,str(nbr) + " points retiré à " + nom)
	      
	    if message[0] == "!set" :
	      modifScore("set",nom,nbr)
	      serv.privmsg(canal,nom + " à maintenant "+ str(nbr) +" points")
	      
	    if message[0] == "!modo" :
	      try :
		utilisateurs.append(message[1])
		serv.privmsg(canal,message[1] + " peut maintenant utiliser les commandes du bot")
	      except :
		a = 0
		
	    if message[0] == "!nomodo" :
	      try :
		for index,name in enumerate(utilisateurs):
		  if name == message[1]:
		    utilisateurs.pop(index)
		    serv.privmsg(canal,message[1] + " ne peut plus utiliser les commandes du bot")
	      except :
		a = 0
	      
      
      if message[0] == "!score" :
	joueur = True
	try :
	  for i in utilisateurs:
	    if i == auteur:
	      joueur = False
	      for nom in sorted(score.items(),key=lambda d:d[1],reverse=False) :
		serv.privmsg(canal,nom[0] + " = " + str(nom[1]) +" points")
		
	  if joueur==True:
	    for nom in sorted(score.items(),key=lambda d:d[1],reverse=False) :
		serv.privmsg(auteur,nom[0] + " = " + str(nom[1]) +" points")
	except :
	  a = 0
    except:
      a = 0
    
if __name__ == "__main__":
  BotScore().start()
