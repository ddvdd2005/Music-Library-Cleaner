import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import EasyMP3
from mutagen.mp3 import MP3
from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import MP4
from tkinter import *
from tkinter import ttk
import io

def strip(string): #lower and remove bad characters from string
    return replace(string.lower(),[".","'",'"',"(",")","[","]","&"," ft "," feat "," vs ","featuring","original","remix","mix"," "])

def replace(string,replacing): #remove all bad characters from string
    for elem in replacing:
        string = string.replace(elem,"")
    return string

def combine(path): #create from the path of the song a string which includes artist and title when the song is a FLAC
    aa = mutagen.File(path)
    try:
        return aa["title"][0]+" "+aa["artist"][0]
    except KeyError:
        try:
            title= aa["title"][0]
            print path + " does not have an artist tag"
            return title
        except KeyError:
            print path + " does not have a title tag"
            try:
                return aa["artist"][0]
            except KeyError:
                print path + " does have neither a title tag nor an artist tag"

def mp3Combine(path): #create from the path of the song a string which includes artist and title when the song is a mp3
    aa= EasyMP3(path)
    try:
        return aa["title"][0]+" "+aa["artist"][0]
    except KeyError:
        try:
            title= aa["title"][0]
            print path + " does not have an artist tag"
            return title
        except KeyError:
            print path + " does not have a title tag"
            try:
                return aa["artist"][0]
            except KeyError:
                print path + " does have neither a title tag nor an artist tag"

def mp4Combine(path): #create from the path of the song a string which includes artist and title when the song is a mp4
    aa= EasyMP4(path)
    try:
        return aa["title"][0]+" "+aa["artist"][0]
    except KeyError:
        try:
            title= aa["title"][0]
            print path + " does not have an artist tag"
            return title
        except KeyError:
            print path + " does not have a title tag"
            try:
                return aa["artist"][0]
            except KeyError:
                print path + " does have neither a title tag nor an artist tag"

def compare(song,list,threshold=0.075): #compare the string with a list of strings of other songs
    for elem in list:
        try:
            if strcomp(song.name,elem.name)<threshold:
                if not(elem.isDupe): #if the song compared to is not a dupe
                    if not(song.isDupe):
                        song.duplicate(elem)
                        elem.duplicated(song)
                    else:
                        elem.duplicate(song.dupes[0])
                        song.dupes[0].duplicated(elem)
                elif elem.dupes[0] not in song.dupes:  #if the song compared to is a dupe, compare it to the original
                    song.duplicate(elem.dupes[0])
                    elem.dupes[0].duplicated(song)
        except AttributeError:
            print song.path + "does not have a name"

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
        elif ".m4a" in path:
            self.name=strip(mp4Combine(path))
            self.type="MP4"
        else:
            print path+"is of an unsupported format"
        self.isDupe=False #is it a duplicate of another song
        self.dupes=[] #if above is true, refer to the song it is a dupe of. If above is false, refer to a list of songs that are duplicates of it.
        self.bestBitrate=False #used later
        self.bestLength=False #used later
        self.bestSize=False #used later

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
        elif self.type=="MP4":
            return EasyMP4(self.path)["title"][0]

    def getArtist(self): #get the artist
        if self.type=="FLAC":
            return mutagen.File(self.path)["artist"][0]
        elif self.type=="MP3":
            return EasyMP3(self.path)["artist"][0]
        elif self.type=="MP4":
            return EasyMP4(self.path)["artist"][0]

    def getLength(self): #get the length
        if self.type=="FLAC":
            return FLAC(self.path).info.length
        elif self.type=="MP3":
            return MP3(self.path).info.length
        elif self.type=="MP4":
            return MP4(self.path).info.length

    def getSize(self): #get the size
        import os
        return float(os.path.getsize(self.path))

    def getBitrate(self): #get the bitrate
        return float(self.getSize()/1024)/float(self.getLength())

    def boldBitrate(self): #file with the best bitrate amongst the dupes
        self.bestBitrate=True

    def boldSize(self): #file with the best size amongst the dupes
        self.bestSize=True

    def boldLength(self): #file with the best length amongst the dupes
        self.bestLength=True

def read(filePath): #reading and putting all of the audio files' paths in a list
    with io.open(filePath, 'r', encoding='utf-8-sig') as file:
        data=file.read()
        list=data.split("\n")
        return list

def var_of_var(k,v): #create a song class named k from the path named v
    globals()[k]=Song(v)

def createList(list): #create a new list filled with all the song class
    total=len(list)
    i=1
    lead="a"
    newList=[]
    for elem in list:
        name=lead+"%07d" % (i,)
        var_of_var(name,elem)
        newList.append(globals()[name])
        print str(i)+"/"+str(total)+" Created"
        i+=1
    return newList

def compareEverything(list,list2): #compare every audio file in the list with one another
    i=1
    for elem in list:
        compare(elem,list2)
        list2.append(elem)
        print str(i)+"/"+str(len(list))+" done"
        i+=1

def createGUI(song): #create a GUI with choices of dupes
    root = Tk()
    root.title("Choose Which Ones to Keep")
    lchoices=[song]
    templist=findBestBitrate(song)
    for elem in templist:
        elem.boldBitrate()
    templist=findBestSize(song)
    for elem in templist:
        elem.boldSize()
    templist=findBestLength(song)
    for elem in templist:
        elem.boldLength()
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
        if elem.bestLength:
            ttk.Label(mainframe,text=timeConverter(elem.getLength()),wraplength=250,justify=CENTER,anchor=CENTER,font='Helvetica 10 bold',foreground="red").grid(column=i,row=5,sticky=(E,W))
        else:
            ttk.Label(mainframe,text=timeConverter(elem.getLength()),wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=5,sticky=(E,W))
        if elem.bestSize:
            ttk.Label(mainframe,text=str("%.2f" % round(elem.getSize()/1024/1024, 2)) + "MB",wraplength=250,justify=CENTER,anchor=CENTER,font='Helvetica 10 bold',foreground="red").grid(column=i,row=6,sticky=(E,W))
        else:
            ttk.Label(mainframe,text=str("%.2f" % round(elem.getSize()/1024/1024, 2)) + "MB",wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=6,sticky=(E,W))
        if elem.bestBitrate:
            ttk.Label(mainframe,text=str("%.2f" % round(elem.getBitrate(),2)) + "KB/s",wraplength=250,justify=CENTER,anchor=CENTER,font='Helvetica 10 bold',foreground="red").grid(column=i,row=7,sticky=(E,W))
        else:
            ttk.Label(mainframe,text=str("%.2f" % round(elem.getBitrate(),2)) + "KB/s",wraplength=250,justify=CENTER,anchor=CENTER).grid(column=i,row=7,sticky=(E,W))
        i=i+1
    ttk.Button(mainframe, text="Choose", command=root.destroy).grid(column=1,columnspan=len(lchoices)+1, row=8, sticky=N)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
    root.mainloop()
    for key,val in dictionnary.items():
        if globals()[key].get():
            endChoices.append(val)
    return endChoices

def compareDupes(list,choice): #check the list for dupes and send them to create GUI to let the user choose which one to keep and return a list with only selected dupes
    newList=[]
    total=str(countDupes(list))
    i=1
    for elem in list:
        chosenOnes=[]
        if not(elem.isDupe):
            if len(elem.dupes)!=0:
                if choice==1:
                    chosenOnes=createGUI(elem)
                    for elem2 in chosenOnes:
                        newList.append(elem2)
                elif choice==2:
                    newList.append(findBestBitrate(elem))
                elif choice==3:
                    newList.append(findBestLength(elem))
                elif choice==4:
                    newList.append(findBestSize(elem))
                print str(i)+"/"+total+" done"
                i+=1
            else:
                newList.append(elem)
    return newList

def countDupes(list): #count the number of choices to be made
    i=0
    for elem in list:
        if not(elem.isDupe):
            if len(elem.dupes)!=0:
                i+=1
    return i

def findBestBitrate(song): #amongst the dupes of one song, find the one with the biggest bitrate
    choices=[song]
    list2=[]
    end=[]
    for elem in song.dupes:
        choices.append(elem)
    for elem in choices:
        list2.append(elem.getBitrate())
    indices = [i for i, x in enumerate(list2) if x == max(list2)]
    for elem in indices:
        end.append(choices[elem])
    return end

def findBestLength(song): #amongst the dupes of one song, find the one with the biggest size
    choices=[song]
    list2=[]
    end=[]
    for elem in song.dupes:
        choices.append(elem)
    for elem in choices:
        list2.append(elem.getLength())
    indices = [i for i, x in enumerate(list2) if x == max(list2)]
    for elem in indices:
        end.append(choices[elem])
    return end

def findBestSize(song): #amongst the dupes of one song, find the one with the biggest length
    choices=[song]
    list2=[]
    end=[]
    for elem in song.dupes:
        choices.append(elem)
    for elem in choices:
        list2.append(elem.getSize())
    indices = [i for i, x in enumerate(list2) if x == max(list2)]
    for elem in indices:
        end.append(choices[elem])
    return end

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

print("Do you have a file with a list of audio files without dupes?\n")
List2=[]
Question0=raw_input("Y/N\n")
while Question0 not in ["Y","N","y","n"]:
    Question0=raw_input("The choice is not valid. Please choose again\n")
if Question0=="Y" or Question0=="y":
    Path1=raw_input("What is the location of that file?\n")
    List2=createList(read(Path1))
    Path=raw_input("What is the location of the audio files that need to be analysed?\n")
else:
    Path=raw_input("What is the location of the file with the list of audio files?\n")
Path2=raw_input("Where would you like to save the songs?\n")
print("How would you like to choose which files to keep when duplicates are met?\n")
print "1. Manually\n2. The one with the best bitrate\n3. The longest one\n4. The biggest one\n"
Question1=int(raw_input("Please choose a number\n"))
while Question1 not in [1,2,3,4]:
    Question1=int(raw_input("The choice is not valid. Please choose again\n"))
List=createList(read(Path))
List3=[]
for elem in List2:
    List3.append(elem)
compareEverything(List,List2)
List=compareDupes(List+List3,Question1)
createFile(List,Path2)
