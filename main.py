import re
import os
from tkinter import * # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter import ttk, messagebox
from tkinter import filedialog
from functools import partial
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class PokemonWindow(Toplevel): #this literally exists just to shortcut the process of making this menu and i dont even know if it saves any time
    def setuppokemonwindow(self):
        m = Menu()
        m_file = Menu(m)
        #make the file menu this is all mostly self explanatory
        #right now most of it doesnt work tho saving data is a problem for future me
        m.add_cascade(menu=m_file,label="File")
        m_file.add_command(label="New Blank Pokemon Sheet")
        m_file.add_command(label="New Generated Pokemon Sheet")
        m_file.add_command(label="Open...",command=lambda: self.event_generate(openFile(currentMon,viewer)))
        m_file.add_separator()
        m_file.add_command(label="Save")
        m_file.add_command(label="Save As...")
        m_file.add_separator()
        m_file.add_command(label="Reload Dex",command=reloadDexData)
        m_file.add_separator()
        m_file.add_command(label="Exit",command=self.destroy) #you should. now.
        self['menu'] = m

width = "640"
height = "480"
customdata = FALSE
class tkinterholder:
    pass

class char:     #class which holds a pokemon's data
    #ughhhh this init is so longggg
    #but its whatever this takes all the pokemon stuff
    #later im probably gonna go 'oh i should make trainers too' and then grumble at myself abt calling this class 'char' but whatever
    #the pokemon are the real characters yknow
    def __init__(self,name = "Name",species = "Species",type = "Type",level = 0,exp = [0,100],nature = "Quirky",size = "Medium",weight = "Medium",hp = [0,0,"Average"],ATK = [0,0,0],DEF = [0,0,0],SPA = [0,0,0],SPD = [0,0,0],SPE = [0,0,0],movespeed = ["30ft Walk"],abilities = [["",""]],moves = [["","","","","",""]],talents = [""],diet = "Omnivore",habitat = "Urban",egggroups = ["Field"],evolution = ["This Pokemon cannot evolve."],notes = ""):
        self.name = name
        self.species = species
        self.type = type
        self.level = level
        self.exp = exp
        self.nature = nature
        self.size = size
        self.weight = weight
        self.height = height
        self.hp = hp
        self.ATK = ATK
        self.DEF = DEF
        self.SPA = SPA
        self.SPD = SPD
        self.SPE = SPE
        self.movespeed = movespeed
        self.abilities = abilities
        self.moves = moves
        self.talents = talents
        self.diet = diet
        self.habitat = habitat
        self.egggroups = egggroups
        self.evolution = evolution
        self.notes = notes
        return
    #this exists bc i didnt want to fuck up by overwriting things wrong with = so you get an entire extra method and a hand cramp
    def copy(self, other):
        self.name = other.name
        self.species = other.species
        self.type = other.type
        self.level = other.level
        self.exp = other.exp
        self.nature = other.nature
        self.size = other.size
        self.weight = other.weight
        self.height = other.height
        self.hp = other.hp
        self.ATK = other.ATK
        self.DEF = other.DEF
        self.SPA = other.SPA
        self.SPD = other.SPD
        self.SPE = other.SPE
        self.movespeed = other.movespeed
        self.abilities = other.abilities
        self.moves = other.moves
        self.talents = other.talents
        self.diet = other.diet
        self.habitat = other.habitat
        self.egggroups = other.egggroups
        self.evolution = other.evolution
        self.notes = other.notes
        return



def parsepokedex(custom):   #this doesnt even like actually parse it does it it just loads it. whatever. later.
    parser = open(os.path.join(__location__, 'PokedexData.csv'), 'r')
    pokedex = []
    linesplit = []
    line = re.split('\n',parser.readline())[0]  #there's a line at the start that we want to clear. this maybe could just be 'parser.readline()'.
    while True:     #go through the whole file.
        line = re.split('\n', parser.readline())[0]
        if(line == ""):
            break   #thats the end of the file.
        linesplit = re.split(",",line)
        pokedex.append(linesplit)   #we're not doing anything crazy because this is a sane and normal csv. unlike the rest.
    parser.close
    if(custom):
        try:
            parser = open(os.path.join(__location__,'CustomPokemon.csv'),'r')
            while True:
                line = re.split('\n', parser.readline())[0]
                if(line == ""):
                    break
                linesplit = re.split(",",line)
                pokedex.append(linesplit)
            parser.close
        except:
            print("No custom pokedex data found!")  #sometimes theyll only have some custom data so this is here for that
    return pokedex

def parseabilitydex(custom):    #load ability data from files
    parser = open(os.path.join(__location__,'Abilitydex.csv'),'r')
    abilitydex = [[],[]]
    linesplit = []
    i = 0
    while True:
        line = re.split('\n',parser.readline())[0]
        if(line == ""):
            break   #end of file
        if(line[len(line)-1]=="\""):    #so this checks if there's a quote at the end and gets rid of it first
            line = line[:-1]
        linesplit = re.split(",\"",line)    #cut on ',"' so as to get rid of the quote
        if(len(linesplit)==1):
            linesplit = re.split(",",line)  #if theres no quote just cut on the comma
        #print("added "+linesplit[0]+" to abilitydex with description "+linesplit[1])
        abilitydex[0].append(linesplit[0])
        abilitydex[1].append(linesplit[1])
    parser.close
    if(custom):
        try:
            parser = open(os.path.join(__location__,'CustomAbilities.csv'),'r')
            while True:
                line = re.split('"\n',parser.readline())[0]
                if(line == ""):
                    break
                linesplit = re.split(r"\|",line)    #there might be commas in the description. go my pipes
                abilitydex[0].append(linesplit[0])
                abilitydex[1].append(linesplit[1])
            parser.close
        except:
            print("No custom ability data found!")  #sometimes theyll only have some custom data so do this instead
    return(abilitydex)

def parseitemdex(custom):   #load item data from files
    parser = open(os.path.join(__location__,"Itemdex.csv"),'r')
    itemdex = []
    linesplit = []
    line = re.split('\n',parser.readline())[0]
    while True:
        line = re.split('\n',parser.readline())[0]
        if(line == ""):
            break
        linesplit = re.split(",",line)  #yaaay this csv is normal
        itemdex.append(linesplit)
    parser.close
    if(custom):
        try:
            parser = open(os.path.join(__location__,"CustomItems.csv"),'r')
            while True:
                line = re.split('\n',parser.readline())[0]
                if(line == ""):
                    break
                linesplit = re.split(",",line)
                itemdex.append(linesplit)
            parser.close
        except:
            print("No custom item data found!") #in case there's no custom item data this is so it doesn't crash
    return itemdex

def parsemovedex(custom):   #load move data from files
    parser = open(os.path.join(__location__,"Movedex.csv"),'r')
    movedex = [[],[],[],[],[],[]]
    linesplit = []
    temp = []
    move = [] 
    
    while True:
        line = re.split('\n',parser.readline())[0]
        desc = ""
        move = []   #gotta keep clearing this thing
        if(line == ""):
            break   #end of file
        linesplit = re.split(";",line)  #ok this breaks it into three sections because this file is *fucked* but im not remaking it
        temp = re.split(",",linesplit[0])   #break the first section [name and pp]
        move.append(temp[0][1:])    #there's a quote at the start. get rid of that.
        if(len(temp)!=1): 
            move.append(temp[1][1:])
        else:
            move.append("SPECIAL")   #these are just listed with no pp value which i get but thats gonna break shit
        temp = re.split(",",linesplit[1])   #break the second section [category and type]
        move.append(temp[0][1:])    #leading space bad
        move.append(temp[1][1:])    #also a leading space
        temp = re.split(r"\. ",linesplit[2])    #break the third section [range and description]
        if(len(temp)==2):   #if it broke cleanly....
            move.append(temp[0][1:])    #leading space
            move.append(temp[1][:-1])   #trailing quote
        else:               #if it didn't break cleanly we gotta stitch it back
            move.append(temp[0][1:])
            for sentence in temp[1:]:   #this is a little janky but it works so w/e
                desc+=sentence+". "     #stitch all the sentences back together
            move.append(desc[:-3])  #this clears out the trailing quote and the '. ' we added
        #print("adding move "+move[0]+ " with "+move[1]+", category "+move[2]+", type "+move[3]+", range "+move[4]+" and description "+move[5]+" to movedex.")
        for i in range(6):
            movedex[i].append(move[i])
    parser.close
    if(custom):
        try:
            parser = open(os.path.join(__location__,"CustomMoves.csv"),'r')
            while True:
                line = re.split('\n',parser.readline())[0]
                if(line == ""):
                    break
                linesplit = re.split(r"\|",line)    #i'm making my own file and its gonna be NORMAL this time rahh
                for i in range(6):
                    movedex[i].append(move[i])
            parser.close
        except:
            print("No custom move data found!")     #sometimes no custom moves so this is here to not brick the program
    return movedex

def init(): #initialise some important stuff. this maybe doesnt need to be a function? it's ok.
    parser = open(os.path.join(__location__,"settings.txt"),'r')    #we're gonna read the settings file here.
    temp = []
    # this is why maybe this shouldnt be a function
    global width
    global height
    global customdata
    global Pokedex
    global Abilitydex
    global Itemdex
    global Movedex
    while True:     #iterate through the settings file and read the settings
        line = re.split('\n',parser.readline())[0]
        if(line == ""):
            break #to the end of the file!
        linesplit = re.split(" = ",line)
        if(linesplit[0]=="Size"):   #there *might* be a more elegant way to do this but this helps in case someone messed up the order
            temp = re.split("x",linesplit[1])
            width = temp[0]
            height = temp[1]
        if(linesplit[0]=="Custom Data"):
            customdata = bool(linesplit[1])
    Pokedex = parsepokedex(customdata)  #we have functions for these so just run those
    Abilitydex = parseabilitydex(customdata)
    Itemdex = parseitemdex(customdata)
    Movedex = parsemovedex(customdata)
    return

def saveCheck(loaded):  #this is gonna check if you want to save data before closing a window but it doesnt work rn because saving doesnt work
    if(loaded.name!="EMPTY"):   #if the name is EMPTY that means nothing's loaded or someone's being a little shit.
        print("check if the user wants to save the current mon")
    return

def openFile(currentMon,viewer):    #this does the actual loading of a file into a character object part, then calls loadMonView to make the window.
    temp = char()   #make this a temp bc if we have a problem we don't want to kill the currentmon. i should also fix this later, we don't want to have 1 universal 'currentmon' now that we're running multiple windows.
    linesplit = []
    subsplit = []
    saveCheck(currentMon)   #this is maybe not important anymore? check if the user wants to save before opening a new file.
    filename = filedialog.askopenfilename()     #let the user pick the file to open
    parser = open(filename,'r')
    try:
        #the first ones are pretty simple, since they're simple strings on their own lines
        temp.name = re.split('\n',parser.readline())[0] 
        temp.species = re.split('\n',parser.readline())[0]
        temp.type = re.split('\n',parser.readline())[0]
        temp.level = int(re.split('\n',parser.readline())[0])
        #exp is stored as current|threshold, so parse that correctly
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.exp = [int(linesplit[0]),int(linesplit[1])]
        #more simple stuff
        temp.nature = re.split('\n',parser.readline())[0]
        temp.size = re.split('\n',parser.readline())[0]
        temp.weight = re.split('\n',parser.readline())[0]
        #hp is stored as current|max|class. current and max should be numbers for later, but class isn't a number at all. It *could* be but I want the saves to be human-readable, kinda.
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.hp = [int(linesplit[0]),int(linesplit[1]),linesplit[2]]
        #all stats are stored as base|invested|stage for data validation reasons. i could have chosen not to store stage but i figured i'd do it just in case.
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.ATK = [int(linesplit[0]),int(linesplit[1]),int(linesplit[2])]
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.DEF = [int(linesplit[0]),int(linesplit[1]),int(linesplit[2])]
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.SPA = [int(linesplit[0]),int(linesplit[1]),int(linesplit[2])]
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.SPD = [int(linesplit[0]),int(linesplit[1]),int(linesplit[2])]
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.SPE = [int(linesplit[0]),int(linesplit[1]),int(linesplit[2])]
        #movespeeds are now like abilities [below] so we're doing the same thing
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        for movespeed in linesplit:
            subsplit.append(re.split(';',movespeed))
        temp.movespeed = subsplit
        subsplit = []   # we're using this again in a sec
        #each ability is its own array of strings for Reasons, and we want this to work no matter how many abilities they have.
        #granted they shouldn't have more than 2, but we're being cautious here. i'd rather have too much flexibility than not enough.
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        for ability in linesplit:
            subsplit.append(re.split(';',ability))
        temp.abilities = subsplit
        #moves are stored just like abilities except that they have more parts each, but that doesn't actually affect this function.
        #i have particular reason to want flexibility here rather than solidly restricting to 4. thanks, daniel.
        subsplit = []   #clear subsplit again since we need it once more this loop and with an 'append' function
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        for move in linesplit:
            subsplit.append(re.split(';',move))
        temp.moves = subsplit
        #talents is just an array of strings for now until the lead dev tells me im wrong as fuck which i think i might be
        temp.talents = re.split(r'\|',re.split('\n',parser.readline())[0])
        #habitat and diet are stored together in the file but not in the object? why did evie do this is she stupid
        linesplit = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.habitat = linesplit[0]
        temp.diet = linesplit[1]
        #eggroups another array of strings thankfully. should also be a max of 2 but w/e
        temp.egggroups = re.split(r'\|',re.split('\n',parser.readline())[0])
        temp.notes = re.split('\n',parser.readline())[0] #notes are just one long string and i don't give a shit what's there. if the user enters newlines we'll parse them into something ourselves.

        currentMon.copy(temp)   #okay, now that you've gone through all of the file with no errors, load that.
    except:
        messagebox.showerror(message="Something went wrong processing "+filename+".")   #happens if you load a file that's, yknow, not an actual file. this is actually probably still too permissive.
    viewer.append(tkinterholder())
    viewer[-1].mon=temp
    parser.close()  #we don't need this still open
    window = PokemonWindow()    #create the new menu so that you can have multiple characters open at once [say, i dunno, your whole team]
    window.setuppokemonwindow() #sets up the 'File' menu. i might have it do more later.
    loadMonView(viewer[-1],window,viewer[-1].mon)   #this actually initialises the new window.
    return

def check_num(newval): #this thing checks if entry is all numbers so people don't say their level is over 9000 or some crap
    return re.match('^[0-9]*$', newval) is not None


def reloadDexData(): #this just calls all the dex functions in case you have a change [usually custom data] midway through running the program.
    global Pokedex
    global Abilitydex
    global Itemdex
    global Movedex
    Pokedex = parsepokedex
    Abilitydex = parseabilitydex
    Itemdex = parseitemdex
    Movedex = parsemovedex
    return

def updateHPClass(hp,classvalue,*args): #updates the HP Class label
    print(hp.get())
    if(hp.get()=="Weak"):
        classvalue.set("(+1d4 / level)")
    elif(hp.get()=="Average"):
        classvalue.set("(+1d6 / level)")
    elif(hp.get()=="Above Average"):
        classvalue.set("(+1d8 / level)")
    elif(hp.get()=="Bulky"):
        classvalue.set("(+1d10 / level)")
    elif(hp.get()=="Tank"):
        classvalue.set("(+1d12 / level)")
    return

def natureStats(viewer,*args): #updates the stat-boosts granted by the pokemon's nature.
    nature = viewer.nature.get()
    naturesarray =[["Hardy","Lonely","Adamant","Naughty","Brave"],["Bold","Docile","Impish","Lax","Relaxed"],["Modest","Mild","Bashful","Rash","Quiet"],["Calm","Gentle","Careful","Quirky","Sassy"],["Timid","Hasty","Jolly","Naive","Serious"]]
    helperarray=[viewer.natureatk,viewer.naturedef,viewer.naturespa,viewer.naturespd,viewer.naturespe]
    j = -1
    for helper in helperarray:
        helper.set("")
    for i in range(len(naturesarray)):
        try:
            j = naturesarray[i].index(nature)
        except ValueError:
            pass
        if j==-1 or j==i:
            j=-1
        else:   
            j+=i*10
            break
    
    if(j!=-1):
        # print(j)
        helperarray[math.floor(j/10)].set("+2")
        helperarray[j%10].set("-2")
    return

def updateStats(viewer,*args): #update the stats window when something changes//when it's initially set up
    natureStats(viewer)
    viewer.totalatk.set(str(int(viewer.baseatk.get())+int(viewer.addedatk.get())))
    if(viewer.natureatk.get()!=""):
        viewer.totalatk.set(str(int(viewer.totalatk.get())+int(viewer.natureatk.get())))
    mod = math.floor((int(viewer.totalatk.get())-1)/7)+1
    if(int(viewer.totalatk.get())==49):
        mod+=1
    mod+=int(viewer.stageatk.get())
    if(mod>=0):
        viewer.modifieratk.set("+"+str(mod))
    else:
        viewer.modifieratk.set(str(mod))

    viewer.totaldef.set(str(int(viewer.basedef.get())+int(viewer.addeddef.get())))
    if(viewer.naturedef.get()!=""):
        viewer.totaldef.set(str(int(viewer.totaldef.get())+int(viewer.naturedef.get())))
    mod = math.floor((int(viewer.totaldef.get())-1)/7)+1
    if(int(viewer.totaldef.get())==49):
        mod+=1
    mod+=int(viewer.stagedef.get())
    if(mod>=0):
        viewer.modifierdef.set("+"+str(mod))
    else:
        viewer.modifierdef.set(str(mod))

    viewer.totalspa.set(str(int(viewer.basespa.get())+int(viewer.addedspa.get())))
    if(viewer.naturespa.get()!=""):
        viewer.totalspa.set(str(int(viewer.totalspa.get())+int(viewer.naturespa.get())))
    mod = math.floor((int(viewer.totalspa.get())-1)/7)+1
    if(int(viewer.totalspa.get())==49):
        mod+=1
    mod+=int(viewer.stagespa.get())
    if(mod>=0):
        viewer.modifierspa.set("+"+str(mod))
    else:
        viewer.modifierspa.set(str(mod))

    viewer.totalspd.set(str(int(viewer.basespd.get())+int(viewer.addedspd.get())))
    if(viewer.naturespd.get()!=""):
        viewer.totalspd.set(str(int(viewer.totalspd.get())+int(viewer.naturespd.get())))
    mod = math.floor((int(viewer.totalspd.get())-1)/7)+1
    if(int(viewer.totalspd.get())==49):
        mod+=1
    mod+=int(viewer.stagespd.get())
    if(mod>=0):
        viewer.modifierspd.set("+"+str(mod))
    else:
        viewer.modifierspd.set(str(mod))
    
    viewer.totalspe.set(str(int(viewer.basespe.get())+int(viewer.addedspe.get())))
    if(viewer.naturespe.get()!=""):
        viewer.totalspe.set(str(int(viewer.totalspe.get())+int(viewer.naturespe.get())))
    mod = math.floor((int(viewer.totalspe.get())-1)/7)+1
    if(int(viewer.totalspe.get())==49):
        mod+=1
    mod+=int(viewer.stagespe.get())
    if(mod>=0):
        viewer.modifierspe.set("+"+str(mod))
    else:
        viewer.modifierspe.set(str(mod))

    return

def loadMonView(viewer, root, mon: char): #initialise the pokemon character sheet window. viewer is just a holder to keep these accessible in other functions. needs to be altered for multiwindow.
    root.geometry("1080x720")
    root.title(mon.name+"'s Character Sheet") #this won't update dynamically but that's fine
    root.grid_columnconfigure(0,weight=1)
    global defaultlabel
    defaultlabel.destroy()
    viewer.root = root
    viewer.overviewholder = ttk.Frame(root,height=200)
    viewer.overviewholder.grid(column=0,row=0,sticky='ew')
    # Now we start with actually loading the data into a viewable form. conveniently if these already exist it should just overwrite them with the new values.
    # everything loads from the mon filtered in here so that if i want i can pull this to another window if i ever do multi-window functionality
    # Load the Name and place it above everything else.
    viewer.namelabel = Label(viewer.overviewholder,text="Name:")
    viewer.namelabel.grid()
    viewer.name = StringVar()
    viewer.name.set(mon.name)
    viewer.nameentry = Entry(viewer.overviewholder,textvariable=viewer.name) 
    viewer.nameentry.grid(row=0,column=1,columnspan=3)
    # Start the next line with the Species. We'll already have set up currentMon beforehand for auto-generated sheets, so dw abt it.
    viewer.specieslabel = Label(viewer.overviewholder,text="Species:")
    viewer.specieslabel.grid(row=1,column=0)
    viewer.species = StringVar()
    viewer.species.set(mon.species)
    viewer.speciesentry = Entry(viewer.overviewholder,textvariable=viewer.species)
    viewer.speciesentry.grid(row=1,column=1,columnspan=3)
    # type.
    viewer.typelabel = Label(viewer.overviewholder,text="Type:")
    viewer.typelabel.grid(row=1,column=4)
    viewer.type = StringVar()
    viewer.type.set(mon.type)
    viewer.typeentry = Entry(viewer.overviewholder,textvariable=viewer.type)
    viewer.typeentry.grid(row=1,column=5)
    # level. 
    viewer.levellabel = Label(viewer.overviewholder,text="Level:")
    viewer.levellabel.grid(row=1,column=6)
    viewer.level = StringVar()
    viewer.level.set(str(mon.level))
    # doing something slightly different here so the user can only enter numbers bc letters wouldnt make sense
    viewer.levelentry = Entry(viewer.overviewholder,textvariable=viewer.level,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.levelentry.grid(row=1,column=7)
    #exp. this has to be in the form [no.]/[no.] because you can have a threshold other than 100. doing the same thing as level these should only be numbers
    viewer.explabel = Label(viewer.overviewholder,text="Exp:")
    viewer.explabel.grid(row=1,column=8)
    viewer.exp = StringVar()
    viewer.exp.set(str(mon.exp[0])) #these are integers for a reason i will understand eventually thanks past me
    viewer.expthreshold = StringVar()
    viewer.expthreshold.set(str(mon.exp[1]))
    viewer.expslash = Label(viewer.overviewholder,text="/")
    viewer.expslash.grid(row=1,column=10) 
    viewer.expentry = Entry(viewer.overviewholder,textvariable=viewer.exp,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.expentry.grid(row=1,column=9)
    viewer.expthresholdentry = Entry(viewer.overviewholder,textvariable=viewer.expthreshold,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.expthresholdentry.grid(row=1,column=11)
    # nature. still on the same line. not validating this to only accept real natures or blank because i can't be assed rn
    viewer.naturelabel = Label(viewer.overviewholder,text="Nature:")
    viewer.naturelabel.grid(row=1,column=12)
    viewer.nature = StringVar()
    viewer.nature.set(mon.nature)
    viewer.natureentry = Entry(viewer.overviewholder,textvariable=viewer.nature)
    viewer.natureentry.grid(row=1,column=13)
    # size class. we don't ever need to work with raw height anymore.
    viewer.sizelabel = Label(viewer.overviewholder,text="Size:")
    viewer.sizelabel.grid(row=1,column=14)
    viewer.size = StringVar()
    viewer.size.set(mon.size)
    viewer.sizeentry = Entry(viewer.overviewholder,textvariable=viewer.size)
    viewer.sizeentry.grid(row=1,column=15)
    # weight class. same as above.
    viewer.weightlabel = Label(viewer.overviewholder,text="Weight:")
    viewer.weightlabel.grid(row=1,column=16)
    viewer.weight = StringVar()
    viewer.weight.set(mon.weight)
    viewer.weightentry = Entry(viewer.overviewholder,textvariable=viewer.weight)
    viewer.weightentry.grid(row=1,column=17)
    # hp time. Actually have to parse some data here. this also starts our next line.
    viewer.hplabel = Label(viewer.overviewholder,text="HP:")
    viewer.hplabel.grid(row=2,column=0)
    viewer.hp = StringVar()
    viewer.hp.set(str(mon.hp[0])) #these being integers actually makes sense except for the part where i can't use that. fuck.
    viewer.hpmax = StringVar()
    viewer.hpmax.set(str(mon.hp[1]))
    viewer.hpslash = Label(viewer.overviewholder,text="/")
    viewer.hpslash.grid(row=2,column=2) 
    viewer.hpentry = Entry(viewer.overviewholder,textvariable=viewer.hp,validate="key",validatecommand=check_num_wrapper,width=4)
    viewer.hpentry.grid(row=2,column=1)
    viewer.hpmaxentry = Entry(viewer.overviewholder,textvariable=viewer.hpmax,validate="key",validatecommand=check_num_wrapper,width=4)
    viewer.hpmaxentry.grid(row=2,column=3) 
    viewer.hpclass = StringVar() #this is already a string, thankfully.
    viewer.hpclass.set(mon.hp[2])
    #we want the user to only be able to choose from the actual hp classes.
    viewer.hpclassentry = ttk.Combobox(viewer.overviewholder,textvariable=viewer.hpclass,values=["Weak","Average","Above Average","Bulky","Tank"],width=13)
    viewer.hpclassentry.state(["readonly"])
    viewer.hpclassdefinition = StringVar()
    viewer.hpclassentry.bind('<<ComboboxSelected>>',partial(updateHPClass,viewer.hpclass,viewer.hpclassdefinition)) #why the fuck is this broken i hate bind
    #viewer.hpclass.trace_add('write',isthisshitworking)
    viewer.hpclassdefinitionlabel = Label(viewer.overviewholder,textvariable=viewer.hpclassdefinition)
    updateHPClass(viewer.hpclass,viewer.hpclassdefinition)  #this part actually does seem to work?
    viewer.hpclassentry.grid(row=2,column=4)
    viewer.hpclassdefinitionlabel.grid(row=2,column=5)
    # makes a frame for the regular stats so they don't have to deal with the above grid
    viewer.statholder = ttk.Frame(root,height=200)
    viewer.statholder.grid(row=1,column=0,sticky='ew')
    # set up the labels for the columns
    viewer.basestatlabel = Label(viewer.statholder,text="Base:")
    viewer.basestatlabel.grid(row=0,column=1)
    viewer.addedstatlabel = Label(viewer.statholder,text="Invested:")
    viewer.addedstatlabel.grid(row=0,column=2)
    viewer.naturestatlabel = Label(viewer.statholder,text="Nature:")
    viewer.naturestatlabel.grid(row=0,column=3)
    viewer.totalstatlabel = Label(viewer.statholder,text="Total:")
    viewer.totalstatlabel.grid(row=0,column=4)
    viewer.stagestatlabel = Label(viewer.statholder,text="Stage:")
    viewer.stagestatlabel.grid(row=0,column=5)
    viewer.modifierstatlabel = Label(viewer.statholder,text="Modifier:")
    viewer.modifierstatlabel.grid(row=0,column=6)
    # attack first
    # base attack, then invested, then show nature boosts, then show total, then display stage, then show modifier.
    viewer.atklabel = Label(viewer.statholder,text="Attack:")
    viewer.atklabel.grid(row=1,column=0)
    viewer.baseatk = StringVar()
    viewer.baseatk.set(str(mon.ATK[0]))
    viewer.baseatkentry = Entry(viewer.statholder,textvariable=viewer.baseatk,validate="key",validatecommand=check_num_wrapper,width=2)
    viewer.baseatkentry.grid(row=1,column=1)
    viewer.addedatk = StringVar()
    viewer.addedatk.set(str(mon.ATK[1]))
    viewer.addedatkentry = Entry(viewer.statholder,textvariable=viewer.addedatk,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.addedatkentry.grid(row=1,column=2)
    viewer.natureatk = StringVar()
    viewer.natureatk.set("")
    viewer.natureatkshow = Label(viewer.statholder,textvariable=viewer.natureatk)
    viewer.natureatkshow.grid(row=1,column=3)
    viewer.totalatk = StringVar()
    viewer.totalatkshow = Label(viewer.statholder,textvariable=viewer.totalatk)
    viewer.totalatkshow.grid(row=1,column=4)
    viewer.stageatk = StringVar()
    viewer.stageatk.set(str(mon.ATK[2]))
    viewer.stageatkentry = ttk.Combobox(viewer.statholder,textvariable=viewer.stageatk,values=["+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6"],width=4)
    viewer.stageatkentry.state(["readonly"])
    viewer.stageatkentry.grid(row=1,column=5)
    viewer.modifieratk = StringVar()
    viewer.modifieratkshow = Label(viewer.statholder,textvariable=viewer.modifieratk)
    viewer.modifieratkshow.grid(row=1,column=6)

    viewer.deflabel = Label(viewer.statholder,text="Defense:")
    viewer.deflabel.grid(row=2,column=0)
    viewer.basedef = StringVar()
    viewer.basedef.set(str(mon.DEF[0]))
    viewer.basedefentry = Entry(viewer.statholder,textvariable=viewer.basedef,validate="key",validatecommand=check_num_wrapper,width=2)
    viewer.basedefentry.grid(row=2,column=1)
    viewer.addeddef = StringVar()
    viewer.addeddef.set(str(mon.DEF[1]))
    viewer.addeddefentry = Entry(viewer.statholder,textvariable=viewer.addeddef,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.addeddefentry.grid(row=2,column=2)
    viewer.naturedef = StringVar()
    viewer.naturedef.set("")
    viewer.naturedefshow = Label(viewer.statholder,textvariable=viewer.naturedef)
    viewer.naturedefshow.grid(row=2,column=3)
    viewer.totaldef = StringVar()
    viewer.totaldefshow = Label(viewer.statholder,textvariable=viewer.totaldef)
    viewer.totaldefshow.grid(row=2,column=4)
    viewer.stagedef = StringVar()
    viewer.stagedef.set(str(mon.DEF[2]))
    viewer.stagedefentry = ttk.Combobox(viewer.statholder,textvariable=viewer.stagedef,values=["+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6"],width=4)
    viewer.stagedefentry.state(["readonly"])
    viewer.stagedefentry.grid(row=2,column=5)
    viewer.modifierdef = StringVar()
    viewer.modifierdefshow = Label(viewer.statholder,textvariable=viewer.modifierdef)
    viewer.modifierdefshow.grid(row=2,column=6)

    viewer.spalabel = Label(viewer.statholder,text="Special Attack:")
    viewer.spalabel.grid(row=3,column=0)
    viewer.basespa = StringVar()
    viewer.basespa.set(str(mon.SPA[0]))
    viewer.basespaentry = Entry(viewer.statholder,textvariable=viewer.basespa,validate="key",validatecommand=check_num_wrapper,width=2)
    viewer.basespaentry.grid(row=3,column=1)
    viewer.addedspa = StringVar()
    viewer.addedspa.set(str(mon.SPA[1]))
    viewer.addedspaentry = Entry(viewer.statholder,textvariable=viewer.addedspa,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.addedspaentry.grid(row=3,column=2)
    viewer.naturespa = StringVar()
    viewer.naturespa.set("")
    viewer.naturespashow = Label(viewer.statholder,textvariable=viewer.naturespa)
    viewer.naturespashow.grid(row=3,column=3)
    viewer.totalspa = StringVar()
    viewer.totalspashow = Label(viewer.statholder,textvariable=viewer.totalspa)
    viewer.totalspashow.grid(row=3,column=4)
    viewer.stagespa = StringVar()
    viewer.stagespa.set(str(mon.SPA[2]))
    viewer.stagespaentry = ttk.Combobox(viewer.statholder,textvariable=viewer.stagespa,values=["+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6"],width=4)
    viewer.stagespaentry.state(["readonly"])
    viewer.stagespaentry.grid(row=3,column=5)
    viewer.modifierspa = StringVar()
    viewer.modifierspashow = Label(viewer.statholder,textvariable=viewer.modifierspa)
    viewer.modifierspashow.grid(row=3,column=6)

    viewer.spdlabel = Label(viewer.statholder,text="Special Defense:")
    viewer.spdlabel.grid(row=4,column=0)
    viewer.basespd = StringVar()
    viewer.basespd.set(str(mon.SPD[0]))
    viewer.basespdentry = Entry(viewer.statholder,textvariable=viewer.basespd,validate="key",validatecommand=check_num_wrapper,width=2)
    viewer.basespdentry.grid(row=4,column=1)
    viewer.addedspd = StringVar()
    viewer.addedspd.set(str(mon.SPD[1]))
    viewer.addedspdentry = Entry(viewer.statholder,textvariable=viewer.addedspd,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.addedspdentry.grid(row=4,column=2)
    viewer.naturespd = StringVar()
    viewer.naturespd.set("")
    viewer.naturespdshow = Label(viewer.statholder,textvariable=viewer.naturespd)
    viewer.naturespdshow.grid(row=4,column=3)
    viewer.totalspd = StringVar()
    viewer.totalspdshow = Label(viewer.statholder,textvariable=viewer.totalspd)
    viewer.totalspdshow.grid(row=4,column=4)
    viewer.stagespd = StringVar()
    viewer.stagespd.set(str(mon.SPD[2]))
    viewer.stagespdentry = ttk.Combobox(viewer.statholder,textvariable=viewer.stagespd,values=["+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6"],width=4)
    viewer.stagespdentry.state(["readonly"])
    viewer.stagespdentry.grid(row=4,column=5)
    viewer.modifierspd = StringVar()
    viewer.modifierspdshow = Label(viewer.statholder,textvariable=viewer.modifierspd)
    viewer.modifierspdshow.grid(row=4,column=6)

    viewer.spelabel = Label(viewer.statholder,text="Speed:")
    viewer.spelabel.grid(row=5,column=0)
    viewer.basespe = StringVar()
    viewer.basespe.set(str(mon.SPE[0]))
    viewer.basespeentry = Entry(viewer.statholder,textvariable=viewer.basespe,validate="key",validatecommand=check_num_wrapper,width=2)
    viewer.basespeentry.grid(row=5,column=1)
    viewer.addedspe = StringVar()
    viewer.addedspe.set(str(mon.SPE[1]))
    viewer.addedspeentry = Entry(viewer.statholder,textvariable=viewer.addedspe,validate="key",validatecommand=check_num_wrapper,width=3)
    viewer.addedspeentry.grid(row=5,column=2)
    viewer.naturespe = StringVar()
    viewer.naturespe.set("")
    viewer.naturespeshow = Label(viewer.statholder,textvariable=viewer.naturespe)
    viewer.naturespeshow.grid(row=5,column=3)
    viewer.totalspe = StringVar()
    viewer.totalspeshow = Label(viewer.statholder,textvariable=viewer.totalspe)
    viewer.totalspeshow.grid(row=5,column=4)
    viewer.stagespe = StringVar()
    viewer.stagespe.set(str(mon.SPE[2]))
    viewer.stagespeentry = ttk.Combobox(viewer.statholder,textvariable=viewer.stagespe,values=["+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6"],width=4)
    viewer.stagespeentry.state(["readonly"])
    viewer.stagespeentry.grid(row=5,column=5)
    viewer.modifierspe = StringVar()
    viewer.modifierspeshow = Label(viewer.statholder,textvariable=viewer.modifierspe)
    viewer.modifierspeshow.grid(row=5,column=6)

    # let's make those stage boxes automatically run the stat update command to show the changed modifier.
    viewer.stageatkentry.bind('<<ComboboxSelected>>',partial(updateStats,viewer))
    viewer.stagedefentry.bind('<<ComboboxSelected>>',partial(updateStats,viewer))
    viewer.stagespaentry.bind('<<ComboboxSelected>>',partial(updateStats,viewer))
    viewer.stagespdentry.bind('<<ComboboxSelected>>',partial(updateStats,viewer))
    viewer.stagespeentry.bind('<<ComboboxSelected>>',partial(updateStats,viewer))

    #okay. now that that's out of the way...
    #this box is just to make things not weird.
    viewer.movementholder = ttk.Frame(root,height=200)
    viewer.movementholder.grid(column=0,row=2,sticky='ew')
    viewer.movements = []
    for i in range(len(mon.movespeed)):  #dynamic length for this bc some mons will have more unique movespeeds than others
        viewer.movements.append([])     #holds an individual movespeed
        viewer.movements[i].append(StringVar())
        viewer.movements[i][0].set(mon.movespeed[i][0])
        viewer.movements[i].append(StringVar())
        viewer.movements[i][1].set(mon.movespeed[i][1])
        viewer.movements[i].append(Entry(viewer.movementholder,textvariable=viewer.movements[i][0],width=10))
        viewer.movements[i][2].grid(row=0,column=(2*i))     #i think this is the simplest way to do this
        viewer.movements[i].append(ttk.Combobox(viewer.movementholder,textvariable=viewer.movements[i][1],values=["Walk","Climb","Hover","Swim","Fly","Burrow","Phase"],width=10))
        viewer.movements[i][3].grid(row=0,column=(2*i)+1)   #next to the other one
    viewer.addmovementspeed = Button(viewer.movementholder,text="+",command=partial(addmovespeed,viewer))
    viewer.addmovementspeed.grid(row=0,column=2*len(viewer.movements))
    viewer.removemovementspeed = Button(viewer.movementholder,text="-",command=partial(removemovespeed,viewer))
    viewer.removemovementspeed.grid(row=0,column=2*len(viewer.movements)+1)

    #TODO: add: talents, habitat//diet, egg group, evolution(s)
    # call me insane cant i do literally the same thing with abilities as with movementspeeds bc they're both
    # mm no actually i want to format them slightly differently
    # close, though. very close.
    viewer.abilityholder = ttk.Frame(root,height=200)
    viewer.abilityholder.grid(column=0,row=3,sticky='ew')
    viewer.abilities = []
    for i in range(len(mon.abilities)):
        viewer.abilities.append([])
        viewer.abilities[i].append(StringVar())
        viewer.abilities[i][0].set(mon.abilities[i][0])
        viewer.abilities[i].append(Entry(viewer.abilityholder,textvariable=viewer.abilities[i][0],width=20))
        viewer.abilities[i][1].grid(row=2*i,column=0,sticky='w',columnspan=2)     #i think this is the simplest way to do this
        viewer.abilities[i].append(Text(viewer.abilityholder,width=100,height=2,wrap="word"))
        viewer.abilities[i][2].insert('1.0',mon.abilities[i][1])
        viewer.abilities[i][2].grid(row=2*i+1,column=0,columnspan=3)
        viewer.abilities[i].append(Button(viewer.abilityholder,text="Lookup",command=partial(abilitylookupbutton,viewer.abilities[i])))
        viewer.abilities[i][3].grid(row=2*i,column=2,sticky='w')
    viewer.addability = Button(viewer.abilityholder,text="+",command=partial(addnewability,viewer))
    viewer.addability.grid(column=0,row=2*len(viewer.abilities),sticky='w')
    viewer.removeability = Button(viewer.abilityholder,text="-",command=partial(removelastability,viewer))
    viewer.removeability.grid(column=1,row=2*len(viewer.abilities),sticky='w')
    # ok moves are basically the same as abilities except there's more boxes gwuhh
    viewer.moveholder = ttk.Frame(root)
    viewer.moveholder.grid(column=0,row=4,sticky='ew')
    viewer.moves = []
    for i in range(len(mon.moves)):
        viewer.moves.append([])
        for j in range(6):
            viewer.moves[i].append(StringVar())
            viewer.moves[i][j].set(mon.moves[i][j])
        viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][0],width=20))
        viewer.moves[i][6].grid(row=3*i,column=0,sticky='w',columnspan=2)
        viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][1],width=3))
        viewer.moves[i][7].grid(row=3*i,column=2,sticky='w')
        viewer.moves[i].append(Label(viewer.moveholder,text="/"))
        viewer.moves[i][8].grid(row=3*i,column=3,sticky='w')
        viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][2],width=10))
        viewer.moves[i][9].grid(row=3*i,column=4,sticky='w')
        viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][3],width=20))
        viewer.moves[i][10].grid(row=3*i+1,column=0,sticky='w',columnspan=2)
        viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][4],width=15))
        viewer.moves[i][11].grid(row=3*i+1,column=2,sticky='w',columnspan=3)
        viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][5],width=15))
        viewer.moves[i][12].grid(row=3*i+1,column=5,sticky='w')
        viewer.moves[i].append(Text(viewer.moveholder,width=100,height=2,wrap="word"))
        viewer.moves[i][13].grid(row=3*i+2,column=0,sticky='ew',columnspan=6)
        viewer.moves[i][13].insert('1.0',mon.moves[i][6])
        viewer.moves[i].append(Button(viewer.moveholder,text="Lookup",command=partial(movelookupbutton,viewer.moves[i])))
        viewer.moves[i][14].grid(row=3*i,column=5,sticky='w')
    viewer.addmove = Button(viewer.moveholder,text="+",command=partial(addnewmove,viewer))
    viewer.addmove.grid(row=3*len(viewer.moves),column=0,sticky='w')
    viewer.removemove = Button(viewer.moveholder,text="-",command=partial(removelastmove,viewer))
    updateStats(viewer)
    # tell the thing to do its job
    root.bind("<Return>",partial(updateStats,viewer))
    root.update_idletasks()
    return

def movelookupbutton(moveblock,*args):
    global Movedex
    try:
        i = Movedex[0].index(moveblock[0].get())
        text = Movedex[5][i]
        moveblock[2].set(Movedex[1][i])
        moveblock[3].set(Movedex[2][i])
        moveblock[4].set(Movedex[3][i])
        moveblock[5].set(Movedex[4][i])
        moveblock[13].delete('1.0','end')
        moveblock[13].insert('1.0',text)
    except:
        print("fuck")
        print(i)
        print(text)
        pass
    return

def addnewmove(viewer,*args):
    i=len(viewer.moves)
    viewer.moves.append([])
    for j in range(6):
        viewer.moves[i].append(StringVar())
        viewer.moves[i][j].set("")
    viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][0],width=20))
    viewer.moves[i][6].grid(row=3*i,column=0,sticky='w',columnspan=2)
    viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][1],width=3))
    viewer.moves[i][7].grid(row=3*i,column=2,sticky='w')
    viewer.moves[i].append(Label(viewer.moveholder,text="/"))
    viewer.moves[i][8].grid(row=3*i,column=3,sticky='w')
    viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][2],width=10))
    viewer.moves[i][9].grid(row=3*i,column=4,sticky='w')
    viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][3],width=20))
    viewer.moves[i][10].grid(row=3*i+1,column=0,sticky='w',columnspan=2)
    viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][4],width=15))
    viewer.moves[i][11].grid(row=3*i+1,column=2,sticky='w',columnspan=3)
    viewer.moves[i].append(Entry(viewer.moveholder,textvariable=viewer.moves[i][5],width=15))
    viewer.moves[i][12].grid(row=3*i+1,column=5,sticky='w')
    viewer.moves[i].append(Text(viewer.moveholder,width=100,height=2,wrap="word"))
    viewer.moves[i][13].grid(row=3*i+2,column=0,sticky='ew',columnspan=6)
    viewer.moves[i][13].insert('1.0',"")
    viewer.moves[i].append(Button(viewer.moveholder,text="Lookup",command=partial(movelookupbutton,viewer.moves[i])))
    viewer.moves[i][14].grid(row=3*i,column=5,sticky='w')
    viewer.addmove.grid(row=3*len(viewer.moves))
    viewer.removemove.grid(row=3*len(viewer.moves))

def removelastmove(viewer,*args):
    for i in range(len(viewer.moves[-1])):
        try:
            viewer.moves[-1][i].destroy()
        except:
            pass
    del viewer.moves[-1]
    viewer.addmove.grid(row=3*len(viewer.moves))
    viewer.removemove.grid(row=3*len(viewer.moves))

def abilitylookupbutton(abilityblock,*args):
    global Abilitydex
    try:
        i = Abilitydex[0].index(abilityblock[0].get())
        text = Abilitydex[1][i]
        abilityblock[2].delete('1.0','end')
        abilityblock[2].insert('1.0',text)
    except:
        pass
    return

def addnewability(viewer,*args):    #add a new ability block.
    i = len(viewer.abilities)
    viewer.abilities.append([])
    viewer.abilities[i].append(StringVar())
    viewer.abilities[i][0].set("")
    viewer.abilities[i].append(Entry(viewer.abilityholder,textvariable=viewer.abilities[i][0],width=20))
    viewer.abilities[i][1].grid(row=2*i,column=0,columnspan=2,sticky='w')     #i think this is the simplest way to do this
    viewer.abilities[i].append(Text(viewer.abilityholder,width=100,height=6,wrap="word"))
    viewer.abilities[i][2].insert('1.0',"")
    viewer.abilities[i][2].grid(row=2*i+1,column=0,columnspan=3)
    viewer.abilities[i].append(Button(viewer.abilityholder,text="Lookup",command=partial(abilitylookupbutton,viewer.abilities[i])))
    viewer.abilities[i][3].grid(row=2*i,column=2,sticky='w')
    viewer.addability.grid(row=2*len(viewer.abilities))
    viewer.removeability.grid(row=2*len(viewer.abilities))
    return

def removelastability(viewer,*args):    #removes the last ability block in the list.
    if(len(viewer.abilities)==1):
        return
    viewer.abilities[-1][1].destroy()
    viewer.abilities[-1][2].destroy()
    viewer.abilities[-1][3].destroy()
    del viewer.abilities[-1]
    viewer.addability.grid(row=2*len(viewer.abilities))
    viewer.removeability.grid(row=2*len(viewer.abilities))
    return

def addmovespeed(viewer,*args):     #add a new movement speed block.
    i = len(viewer.movements)
    viewer.movements.append([])     #holds an individual movespeed
    viewer.movements[i].append(StringVar())
    viewer.movements[i][0].set("")
    viewer.movements[i].append(StringVar())
    viewer.movements[i][1].set("")
    viewer.movements[i].append(Entry(viewer.movementholder,textvariable=viewer.movements[i][0],width=10))
    viewer.movements[i][2].grid(row=0,column=(2*i))     #i think this is the simplest way to do this
    viewer.movements[i].append(ttk.Combobox(viewer.movementholder,textvariable=viewer.movements[i][1],values=["Walk","Climb","Hover","Swim","Fly","Burrow","Phase"],width=10))
    viewer.movements[i][3].grid(row=0,column=(2*i)+1)   #next to the other one
    viewer.addmovementspeed.grid(row=0,column=2*i+2)    #gotta move these too can't forget
    viewer.removemovementspeed.grid(row=0,column=(2*i)+3)
    return

def removemovespeed(viewer,*args):  #remove the furthest right movement speed block.
    viewer.movements[-1][2].destroy()
    viewer.movements[-1][3].destroy()
    del viewer.movements[-1]
    viewer.addmovementspeed.grid(row=0,column=2*len(viewer.movements))
    viewer.removemovementspeed.grid(row=0,column=2*len(viewer.movements)+1)
    viewer.root.update_idletasks()
    return

init()  #run the initialisation.
currentMon = char(name="EMPTY",notes="IF YOU'RE SEEING THIS SOMETHING'S BROKEN")    #default currentmon. might phase this out later.
viewer = [] #ok call me crazy but im doing it this way now
root = Tk()
root.option_add('*tearOff', FALSE)  #apparently this is just. on by default? why is it like that?
root.title("Iibui's Comprehensive Region Rovers Pokemon Helper")
root.geometry(width+"x"+height)

#start makin' the menus
m = Menu(root)
#file menu
m_file = Menu(m)
m.add_cascade(menu=m_file,label="File")
m_file.add_command(label="New Blank Pokemon Sheet")
m_file.add_command(label="New Generated Pokemon Sheet")
m_file.add_command(label="Open...",command=lambda: root.event_generate(openFile(currentMon,viewer)))
m_file.add_separator()
m_file.add_command(label="Save")
m_file.add_command(label="Save As...")
m_file.add_separator()
m_file.add_command(label="Reload Dex",command=reloadDexData)
m_file.add_separator()
m_file.add_command(label="Settings",command=lambda: root.event_generate("<<OpenSettingsDialog>>"))
m_file.add_command(label="Exit",command=root.destroy)
#view menu
m_view = Menu(m)
m.add_cascade(menu=m_view,label="View")
m_view.add_command(label="View Item Dex")
m_view.add_command(label="View Ability Dex")
m_view.add_command(label="View Move Dex")
m_debug = Menu(m)
m.add_cascade(menu=m_debug,label="Debug")



#m_debug.add_command(label="Print Current Name to Console",command=lambda: root.event_generate(quickdebugname(viewer)))
#actually assign the menus to the window
root['menu'] = m

def customtoggle(): #this just actually makes the custom data button work
    global customdata
    if(customdata):
        customdata = False
    else:
        customdata = True
    print(customdata)
    return

def launchsettingsmenu(*args): #launch the settings menu!
    global customdata
    w_settings = Toplevel(root) #it's ok because we don't actually need the settings menu for anything else i think maybe ill regret this later
    w_settings.title("Settings")
    w_settings.geometry('640x480')
    custom = BooleanVar()
    custom.set(customdata)
    settings_customdata = ttk.Checkbutton(w_settings,text="Enable Custom Data (Requires Dex Reload to take effect.)",command=customtoggle,variable=custom,onvalue=True,offvalue=False)
    settings_customdata.grid()
    settings_save = ttk.Button(w_settings,text="Save Settings",command=savesettings)
    settings_save.grid(row=1)
    w_settings.mainloop()
    return

def savesettings(): #save settings!
    global customdata
    global height
    global width
    settingsfile = open(os.path.join(__location__,'settings.txt'),'w')
    settingsfile.write("Size = "+str(width)+"x"+str(height)+"\nCustomData = "+str(customdata))



root.bind("<<OpenSettingsDialog>>",launchsettingsmenu)  #do i actually need to do this this way?
check_num_wrapper = (root.register(check_num), '%P')

defaultlabel = Label(root, text = "Choose an item from the top menu to get started!")
defaultlabel.grid()


root.mainloop()