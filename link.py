from random import randint as rand


output = ""
def get_output():
    global output
    x = output
    output = ""
    return x

def myprint(text,newline=True):
    global output
    output += text
    if newline:
        output += "\n"


def link(namn=""):

    room = "castle"
    while namn == "":
       myprint("<img src='img/Linkicon.jpg' width='300px'>")
       myprint( "Welcome to the Legend of Link!" )
       myprint( "What is your name?" )
       #namn = raw_input()
       namn = yield get_output()
       
    myprint( "Hello "+namn+"!" )
    myprint( "You are now ready to start the Legend of Link!" )
    myprint( "If you need help just type help" )
    items = {"castle":["note"], 
             "beach":["bucket"],
             "pier":["shovel"],
             "prison":[],
             "field":[ ],
             "courtyard":[ "sword"],
             "mountain": ["snow"],
             "cave":[ ],
             "hole":[ ],
             "water":["dirt"],
             "fightfield": []
             }
    map = {"castle":["prison"],
           "beach":["water","pier","field"],
           "field":[ ],
           "courtyard":["field"],
           "pier":["beach"],
           "prison":["castle"],
           "mountain":["field","cave"],
           "cave":["mountain"],
           "hole":["fightfield" ],
           "water":[ ],
           "fightfield":[ ]
           }
    inv = [ ]

    play = "yes"

    whistle_count = 0
    found_link = False
    field_trolls = 3

    player_power = 10
    boss_power = 10

    while play == "yes":
        myprint( "" )
        myprint( "You are in a " + room + "." )
        if room == "cave":
            myprint( "You hear someone calling for help at the other side..." )
            myprint( "It is Link!! " )
            if not "hole" in map["cave"]:
                myprint( "You must save him but it is a " )
                myprint( "big pile of stones blocking the path!" )
            myprint( ""  )
        myprint( "What have I to do?" )
        #command = raw_input()
        command = yield get_output()
        myprint( ""  )
        command = command.split()
        if len(command)==0: 
            command = [""]
        if len(command) == 1 and command[0]=="help":
            myprint( "You can type: " )
            myprint( "  look, inv, take (thing), drop (thing), go (place), " )
            myprint( "  unlock (thing), read (think), whistle, " )
            myprint( " ", newline=False)
            if "sword" in inv:
                 myprint( "attack,", newline=False )
            myprint( "help, or quit. " )
        if command[0] == "whistle":
            if room == "prison":
                whistle_count = whistle_count + 1
                if whistle_count == 1:
                    myprint( "You whisle 'Singing in the rain'. " )
                    myprint( " It starts to drip from the ceiling.'" )
                if whistle_count == 2:
                    myprint( "You whistle 'Pippi Longstocking'" )
                    myprint( "so badly that the ceiling starts to crack!" )
                if whistle_count == 3:
                    myprint( "TA DA DA DAAAAAA!  Click click click...." )
                    myprint( "A key appears!" )
                    items["prison"].append("key")
                if whistle_count > 3:
                    myprint( "Aaargh!  My ears are hurting!" )
            else:
                myprint( "Please!  Stop!  My nerves are going to break!" )
        if len(command) == 1 and command[0]=="look":
            myprint( "You can see " )
            for i in items[room]:
                myprint( "* " + i )
            if len(items[room]) == 0:
                myprint( "nothing special." )
            myprint( "" )
            myprint( "You can go to " )
            for i in map[room]:
                myprint( "* " + i )
            if room == "castle" and not "courtyard" in map["castle"]:
                myprint( "You can see a locked door." )
        if command == ["look", "stones"] and room == "cave":
            myprint( "The smallest stones must have a weight of a thousand tonnes!!" )
            myprint( " You must find another path... But where?" )

        if len(command) == 1 and command[0]=="inv":
            myprint( "You have" )
            if inv == [ ]:
                myprint( "nothing" )
            for i in inv:
                myprint( "* "+i )
        if  len(command) == 2 and command[0]=="drop":
             if command[1] in inv:
                  inv.remove(command[1])
                  items[room].append(command[1])
             else:
                  myprint( "You can't drop "+command[1] )
        if  len(command) == 2 and command[0]=="take":
            if command[1] in items[room]:
                if room == "hole" and command[1] in ["gold-sword", "gold-shield"]:
                    if "sword" in inv:
                         myprint( "It's too heavy!  You have to drop your old sword!" )
                    else:
                         items[room].remove(command[1])
                         inv.append(command[1])
                         myprint( "You took the " + command[1] + "." )
                elif room == "hole" and command[1] == "sword" and ("gold-sword" in inv or "gold-shield" in inv):
                    myprint( "You can't carry that much!" )
                else:
                    items[room].remove(command[1])
                    inv.append(command[1])
                    myprint( "You took the " + command[1] + "." )
            else:
                myprint( "I can't see a "+ command[1]+"." )
        if len(command) == 2 and command[0] == "go":
            if command[1] in map[room]:
                room = command[1]
            else:
                myprint( "you can not go there."     )
        if len(command) == 1 and command[0] == "quit":
            play = "no"
        if len(command) == 2 and command[0] == "unlock" and command[1] == "door":
            if not "key" in inv:
                myprint( "You need a key." )
            else:
                if not room == "castle":
                    myprint( "There is nothing to unlock" )
                else:
                    myprint( "You unlock the door" )
                    inv.remove("key")
                    map["castle"].append("courtyard")        
                    map["courtyard"].append("castle")        
        if len(command) == 1 and command[0] == "dig":
            if not "shovel" in inv:
                myprint( "You have nothing to dig with." )
            else:
                if not room == "cave":
                    myprint( "Nothing happens." )
                else:
                    myprint( "You found a secret passage!" )
                    map["cave"].append("hole")        
                    map["hole"].append("cave")        
        if len(command) == 2 and command[0] == "read" and command[1] == "note":
            if "note" in inv:
                myprint( "The note says:" )
                myprint( "" )
                myprint( "   Hi, " + namn )
                myprint( """   it's me, Link! 
       I am on a trip to the mountains. 
       We have been friends so long time 
       and i dont want to hurt your heart 
       but you slept so nice and i just 
       felt like eating my brown beans and 
       grandmas banana cream pie alone.

       From your friend 
       Link

       Ps. If you need the key, whistle three
       times in the prison cell, as usual.


    What! Banana cream pie! 
    The note makes you feel very jealous!
    Maybe you should find him and tell 
    him some words of truth!
    """)
            else:
                myprint( "You don't have a note to read." )
        if room == "mountain" and command == ["make", "snowball"]:
            inv.append("snowball")
            myprint( "The snowball is cold and hard." )
            myprint( "Maybe you should throw it on Link," )
            myprint( "if you can find him..." )
        if room == "water":
            myprint( "You can't swim. You drowned! " )
            play = "no" 
        if room == "hole" and found_link == False:
            found_link = True
            myprint( "You found Link!  He is saved!" )
            myprint( 'Link says "Whoa! Hi '+namn+'!! After a while the ground' )
            myprint( 'cracked under my feet and I fell down in this ****** ****** **** hole.' )
            myprint( "O I'm sorry that I'm swearing so much" )
            myprint( 'but I am so !#^@$*%(_*(*^((^%%^*$@#% angry."' )
            myprint( "Link makes an angry grimace to the ground" )
            myprint( 'of the hole and sticks out his tounge.' )
            myprint( 'Link continues "I heard a sign of hollows in a place in this hole.' )
            myprint( 'If you had a shovel I think you could dig the thin part' )
            myprint( ' but I dont think you have one so as consulation ' )
            myprint( 'you can get some brown conseved beans and some banana cream pie!."' )
            myprint( "TA DA DA DAAA you got some food." )
            myprint( 'You eat the food the fastest you can and say' )
            myprint( '"I acataly have a shovel"' )
            myprint( 'Link says "WHAT ACATALY!!"' )
            myprint( "Suddenly you hear a very loud noise." )
            myprint( "Then you hear a loud CRRACK" )
            myprint( "It begain to rain and 3 seconds later it rains undescribably much." )
            myprint( "The crack came from the secret passage" )
            myprint( 'it was time to take goodbye of it.' )
            myprint( "Link shows you a part of the wall and you break it with your shovel." )
            myprint( 'Link say "O for last thing take this"' )
            myprint( "TA DA DA DAA you got the gold sword and the gold shield." )
            myprint( "They are too heavy to carry!  You must drop your old sword." )
            myprint( 'Link say "Now you can go through the hollows in the mountain' )
            myprint( 'and discover the other side...Can I go with you?"' )
            myprint( 'You say "Always!"' )
            myprint( 'Link says "O ' + namn + '. You are the best friend in the world!."' )
            items[room].append("gold-sword")
            items[room].append("gold-shield")
        if room == "field":
            if command[0] == "attack":
                if field_trolls > 0 and "sword" in inv:
                    myprint( "You attack a troll with your sword. You win!" )
                    field_trolls = field_trolls - 1
                    if field_trolls == 0:
                        map[room].append("mountain")
                        map[room].append("beach")
                        map[room].append("courtyard")

            if field_trolls > 0:
                myprint( "You can see %d trolls!  Help!" % field_trolls )
                if not "sword" in inv:
                    myprint( "You need a sword!  The trolls attack you!  You lose!" )
                    play = "no"

        if command == ["go", "fightfield"]:
            myprint( "BOOOM!  A wall magically appears behind you! You can't go back!" )
            myprint( "You are trapped with Link!" )
            myprint( "BOOM! A flash lights up the fightfield! A terrible MONSTER appears!" )
            myprint( "It's front end is a big turtle!  It's back is a dragon!" )
            myprint( "And it is BIG!  Like a banana tree!  But definitively not as sweet!" )

        if room == "fightfield":
            if boss_power > 0:
                if "gold-shield" in inv:
                    damage = rand(0,2)
                else:
                    damage = rand(0,7)
                if damage > 0:
                    myprint( "The monster attacks you! You are hurt with %d" % damage )
                    player_power = player_power - damage
                    myprint(  "You have %d power left." % player_power )
                else:
                    myprint( "The monster attacks, but misses you!" )
            if command[0]=="attack":
                damage = rand(0,3)
                if damage > 0:
                   myprint( "You attack the monster with %d power!" % damage )
                   boss_power = boss_power - damage
                else:
                   myprint( "You attack but MISS the monster!  Help!" )
            if player_power <= 0:
                myprint( "You have lost all your power! The MONSTER has won!"  )
                myprint( "You and Link die...  The monster gets lunch!" )
                play = "no"
            elif boss_power <= 0:
                myprint( "You give the monster a blow with your sword and" )
                myprint( "the monster gets its last look on this world. For ever!" )
                myprint( "You win!" )
                myprint( "" )
                myprint( """ 
     24 days later you and Link arrive with a train to the royal palace of hyrule.
    The king's servant whaits for you on the station.
    'Welcome to the center of hyrule' He says.
    He takes you to a wagon with royal horses and you jump up in the royal wagon.
    Link tells jokes and you laugh all the way to the palace.
    In the royal hall the fabulous king sits on his throne.
    He says'Welcome heros of hyrule to my palace.
    You and Link bow down for the king.
    You discuss with Link if you will steal the kings shoes so you dont
    hear what the king says.
    Suddenly you hear the king say'Rise your heads heros of hyrule.
    You and Link rise you heads.
    'Now and forever' the king says 'are you two the biggest knights in hyrules history'

    """ + namn + " and Link" )
                play = "no"

    myprint( "" )
    myprint( "The end    (press RETURN)" )
    yield get_output()

    



