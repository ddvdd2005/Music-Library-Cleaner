import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import EasyMP3 as EasyMP3
from mutagen.mp3 import MP3
from tkinter import *
from tkinter import ttk

def strip(string): #lower and remove bad characters from string
    return replace(string.lower(),[".","'",'"',"(",")","[","]","&"," ft "," feat "," vs ","featuring","original","remix","mix"," "])

def replace(string,replacing): #remove all bad characters from string
    for elem in replacing:
        string = string.replace(elem,"")
    return string

def combine(path): #create from the path of the song a string which includes artist and title when the song is a FLAC
    aa = mutagen.File(path)
    return str(aa["title"][0])+" "+str(aa["artist"][0])

def mp3Combine(path): #create from the path of the song a string which includes artist and title when the song is a mp3
    aa= EasyMP3(path)
    return str(aa["title"][0])+" "+str(aa["artist"][0])

def compare(song,list,threshold=0.075): #compare the string with a list of strings of other songs
    for elem in list:
        if strcomp(song.name,elem.name)<threshold:
            if not(elem.isDupe): #if the song compared to is not a dupe
                song.duplicate(elem)
                elem.duplicated(song)
            elif elem.dupes[0] not in song.dupes:  #if the song compared to is a dupe, compare it to the original
                song.duplicate(elem.dupes[0])
                elem.dupes[0].duplicated(song)

def strcomp(str1,str2): #compare one string with another and find how alike they are
    total_length=len(str1)+len(str2)
    for char in str1:
        if char in str2:
            str1=str1.replace(char,"",1)
            str2=str2.replace(char,"",1)
    return float(len(str1)+len(str2))/total_length

class Song: #every song is a class by itself

    def __init__(self,path):
        self.path=path #path
        if ".flac" in path: #name
            self.name=strip(combine(path))
            self.type="FLAC" #type
        elif ".mp3" in path:
            self.name=strip(mp3Combine(path))
            self.type="MP3"
        else:
            print path+"is of an unsupported format"
        self.isDupe=False #is it a duplicate of another song
        self.dupes=[] #if above is true, refer to the song it is a dupe of. If above is false, refer to a list of songs that are duplicates of it.

    def duplicate(self,otherSong): #if the song is discovered to be a duplicate of another song
        self.isDupe=True
        self.dupes.append(otherSong)

    def duplicated(self,otherSong): #if another song is discovered to be a duplicate of it
        self.dupes.append(otherSong)

    def getTitle(self): #get the title of the song
        if self.type=="FLAC":
            return mutagen.File(self.path)["title"][0]
        elif self.type=="MP3":
            return EasyMP3(self.path)["title"][0]

    def getArtist(self): #get the artist
        if self.type=="FLAC":
            return mutagen.File(self.path)["artist"][0]
        elif self.type=="MP3":
            return EasyMP3(self.path)["artist"][0]

    def getLength(self): #get the length
        if self.type=="FLAC":
            return FLAC(self.path).info.length
        elif self.type=="MP3":
            return MP3(self.path).info.length

    def getSize(self): #get the size
        import os
        return float(os.path.getsize(self.path))

    def getBitrate(self): #get the bitrate
        return "%.2f" % round(float(self.getSize()/1024)/float(self.getLength()), 2)

def read(filePath): #reading and putting all of the audio files' paths in a list
    f=open(filePath,"r")
    message=f.read()
    list=message.split("\n")
    return list

def var_of_var(k,v): #create a song class named k from the path named v
    globals()[k]=Song(v)

def createList(list): #create a new list filled with all the song class
    i=1
    lead="a"
    newList=[]
    for elem in list:
        str=lead+"%07d" % (i,)
        var_of_var(str,elem)
        i+=1
        newList.append(globals()[str])
    return newList

def compareEverything(list): #compare every audio file in the list with one another
    list2=[]
    for elem in list:
        compare(elem,list2)
        list2.append(elem)

def createGUI(song): #create a GUI with choices of dupes
    root = Tk()
    root.title("Choose Which Ones to Keep")
    lchoices=[song]
    endChoices=[]
    for elem in song.dupes:
        lchoices.append(elem)
    dictionnary={}
    boolvar="var"
    num=1
    for elem in lchoices:
        temp=boolvar+str(num)
        globals()[temp]=BooleanVar()
        globals()[temp].set(False)
        dictionnary[temp]=elem
        num+=1
    num=1
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    ttk.Label(mainframe, text="Placeholder").grid(column=1, row=1, sticky=(E))
    ttk.Label(mainframe, text="Path").grid(column=1, row=2, sticky=(E))
    ttk.Label(mainframe, text="Title").grid(column=1, row=3, sticky=(E))
    ttk.Label(mainframe, text="Artist").grid(column=1, row=4, sticky=(E))
    ttk.Label(mainframe, text="Length").grid(column=1, row=5, sticky=(E))
    ttk.Label(mainframe, text="Size").grid(column=1, row=6, sticky=(E))
    ttk.Label(mainframe, text="Bitrate").grid(column=1, row=7, sticky=(E))
    i=2
    for elem in lchoices:
        ttk.Checkbutton(mainframe,text="#"+str(i-1),variable=globals()[boolvar+str(num)]).grid(column=i,row=1,sticky=(N))
        num+=1
        ttk.Label(mainframe,text=elem.path,wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=2,sticky=(E,W))
        ttk.Label(mainframe,text=elem.getTitle(),wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=3,sticky=(E,W))
        ttk.Label(mainframe,text=elem.getArtist(),wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=4,sticky=(E,W))
        ttk.Label(mainframe,text=timeConverter(elem.getLength()),wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=5,sticky=(E,W))
        ttk.Label(mainframe,text=str("%.2f" % round(elem.getSize()/1024/1024, 2)) + "MB",wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=6,sticky=(E,W))
        ttk.Label(mainframe,text=str(elem.getBitrate()) + "KB/s",wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=7,sticky=(E,W))
        i=i+1
    ttk.Button(mainframe, text="Choose", command=root.destroy).grid(column=len(lchoices)+1, row=8, sticky=W)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
    root.mainloop()
    for key,val in dictionnary.items():
        if globals()[key].get():
            endChoices.append(val)
    return endChoices

def compareDupes(list): #check the list for dupes and send them to create GUI to let the user choose which one to keep and return a list with only selected dupes
    newList=[]
    for elem in list:
        chosenOnes=[]
        if not(elem.isDupe):
            if len(elem.dupes)!=0:
                chosenOnes=createGUI(elem)
                for elem2 in chosenOnes:
                    newList.append(elem2)
            else:
                newList.append(elem)
    return newList

def createFile(list,path): #Create a m3u file at the selected path
    f= open(path,"w+")
    for elem in list:
        f.write(elem.path+"\n")
    f.close()

def timeConverter(time): #converts a time from seconds to hours, minutes and seconds
    if time>3600:
        return str(int(time/3600)) + ":" + str("%02d" % (int(time%3600/60)),) + ":" + str("%02d" % (int(time%60)),)
    else:
        return str("%02d" % (int(time/60)),) + ":" + str("%02d" % (int(time%60)),)

Path=raw_input("What is the location of the file with the list of audio songs?\n")
Path2=raw_input("Where would you like to save the songs?\n")
List=createList(read(Path))
compareEverything(List)
List=compareDupes(List)
createFile(List,Path2)