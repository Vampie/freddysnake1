import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
boardX= 0
boardY=0
myheadX=0
myheadY=0
goingUP = 0
goingDOWN = 0
goingLEFT=0
goingRIGHT=0
init=1

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "V-Ampie",  # TODO: Your Battlesnake Username
            "color": "#33cc33",  # TODO: Personalize
            "head": "bwc-rudolph",  # TODO: Personalize
            "tail": "hook",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        global init
        global goingUP
        global goingDOWN
        global goingLEFT
        global goingRIGHT

        
        data = cherrypy.request.json

        print("START")
        boardX= data["board"]["height"]
        boardY= data["board"]["width"]
        myheadX=data["you"]["head"]["x"]
        myheadY=data["you"]["head"]["y"]
        print(f"Het bord is {boardX}, {boardY} groot")
        print(f"ik sta op {myheadX}, {myheadY}")
        #we moeten naar 0,0, dus als x <> 0, gaan we naar rechts
        goingLEFT=0
        goingRIGHT=1
        goingDOWN=0
        goingUP=0
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        global init
        global goingUP
        global goingDOWN
        global goingLEFT
        global goingRIGHT

        data = cherrypy.request.json

        print("Board: %(height)s, %(width)s." % data["board"])
        print("Me: %(x)s, %(y)s." % data["you"]["head"])
        print("GOING: left:{goingLEFT}, right:{goingRIGHT}, up:{goingUP}, down:{goingDOWN}")
        

        if init==1:
          #init bezig, dus eerst naar 0,0 gaan
          if data["you"]["head"]["x"] >0:
            #X = horizontaal, eerst nar 0 gaan, dus naar links
            goingLEFT=1
            goingRIGHT=0
            goingDOWN=0
            goingUP=0
          else:
            if data["you"]["head"]["y"] >0:
              #Y = verticaal, eerst naar 0 gaan, dus naar beneden
              goingLEFT=0
              goingRIGHT=0
              goingDOWN=1
              goingUP=0
            else:
              #X en Y zijn nul, dus init is gedaan, we kome nvan boven, dus naar rechts gaan
              init=0
              goingLEFT=0
              goingRIGHT=1
              goingDOWN=0
              goingUP=0
        else:
          if goingUP == 1:
            #we zijn 1 naar boven geweest, dus de richting liks <> rechts wijzigen.
            goingUP=0
            goingLEFT=goingRIGHT
            goingRIGHT=not bool(goingRIGHT)
          else:
            if goingDOWN == 1:
              if data["you"]["head"]["y"] ==0:
                goingLEFT=goingRIGHT
                goingRIGHT=not bool(goingRIGHT)
                goingDOWN=0
            else:
              #we zitten NIET op de bovenste rij
              if data["you"]["head"]["y"] <data["board"]["height"]-1:
                if (data["you"]["head"]["x"] >=data["board"]["width"]-2 and goingRIGHT==1) or (data["you"]["head"]["x"] ==1 and goingLEFT==1):
                  goingUP=1
              else:
                #we zitten op de bovenste rij
                #we zitten op de voorlaatste kolom of op de eerste kolom
                if (data["you"]["head"]["x"] ==data["board"]["width"]-2 or data["you"]["head"]["x"] ==1 ):
                  goingUP=0
                  goingDOWN=0
                if (data["you"]["head"]["x"] ==data["board"]["width"]-1 or data["you"]["head"]["x"] ==0):
                  goingUP=0
                  goingDOWN=1

        
        if goingLEFT == 1:
          move="left"
        if goingRIGHT == 1:
          move="right"
        if goingUP == 1:
          move="up"
        if goingDOWN == 1:
          move="down"


        # Choose a random direction to move in
        #possible_moves = ["up", "right", "down", "left"]
        #move = possible_moves[data["turn"] % 4]
        

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
