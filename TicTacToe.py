from tkinter import Tk,ttk,Button, StringVar, Listbox
from tkinter import messagebox
from random import randint
from tkinter import simpledialog
import  time


import threading
from tkinter.tix import Tree
semafor = threading.Semaphore()
exit_event = threading.Event()

from ZODB import  DB
from ZEO.ClientStorage import ClientStorage
from persistent import Persistent
import transaction
from persistent.list import PersistentList
from BTrees import OOBTree
from ZODB.POSException import ConflictError


class Igra(Persistent):
    def __init__(self, ploca, date):
        self.ploca = ploca
        self.winner = None
        self.date = date

class Ploca(Persistent):
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.live = False
        self.ActivePlayer = player1
        self.moves = {player1.nadimak: [], player2.nadimak: []}
        self.mov = 0

class korisnik(Persistent):
    def __init__(self, nadimak, lozinka):
        self.nadimak = nadimak
        self.lozinka = lozinka
        self.blog = PersistentList()
        self.inQueue = False
        self.inGame = False
        self.live = False

class Aplikacija:
    def __init__(self, root):
        self.conn = self.uspostaviVezu()
        self.rootDb = self.conn.root()
        self.root = root
        self.igra = None
        self.provjeraQueueThread = None
        self.provjeriActivPlayerThread = None

        if not 'korisnici' in self.rootDb.keys():
            print( 'Stvaram riječnik za sesije' )
            self.rootDb[ 'korisnici' ] = OOBTree.OOBTree()
        if not 'queue' in self.rootDb.keys():
            print( 'Stvaram riječnik za queue' )
            self.rootDb[ 'queue' ] = PersistentList()
        if not 'live' in self.rootDb.keys():
            print( 'Stvaram riječnik za live' )
            self.rootDb[ 'live' ] = OOBTree.OOBTree()
        if not 'games' in self.rootDb.keys():
            print( 'Stvaram riječnik za games' )
            self.rootDb[ 'games' ] = OOBTree.OOBTree()
        self.my_transaction_manager.commit()

    def uspostaviVezu(self):
        self.my_transaction_manager = transaction.TransactionManager()
        st = ClientStorage(('localhost', 2709))
        self.db = DB(st)
        conn = self.db.open(self.my_transaction_manager)
        return conn 

    def SetLayout(self, id, player_symbol):
        if id==1:
            self.b1.config(text= player_symbol)
            self.b1.state(['disabled'])
        elif id==2:
            self.b2.config(text= player_symbol)
            self.b2.state(['disabled'])
        elif id==3:
            self.b3.config(text= player_symbol)
            self.b3.state(['disabled'])
        elif id==4:
            self.b4.config(text= player_symbol)
            self.b4.state(['disabled'])
        elif id==5:
            self.b5.config(text= player_symbol)
            self.b5.state(['disabled'])
        elif id==6:
            self.b6.config(text= player_symbol)
            self.b6.state(['disabled'])
        elif id==7:
            self.b7.config(text= player_symbol)
            self.b7.state(['disabled'])
        elif id==8:
            self.b8.config(text= player_symbol)
            self.b8.state(['disabled'])
        elif id==9:
            self.b9.config(text= player_symbol)
            self.b9.state(['disabled'])

    def CheckWinner(self):
        mov = self.igra.ploca.mov
        self.p1 = self.igra.ploca.moves[self.igra.ploca.player1.nadimak]
        self.p2 = self.igra.ploca.moves[self.igra.ploca.player2.nadimak]
        winner = -1

        if(1 in self.p1) and (2 in self.p1) and (3 in self.p1):
            winner = 1
        if(1 in self.p2) and (2 in self.p2) and (3 in self.p2):
            winner = 2

        if(4 in self.p1) and (5 in self.p1) and (6 in self.p1):
            winner = 1
        if(4 in self.p2) and (5 in self.p2) and (6 in self.p2):
            winner = 2

        if(7 in self.p1) and (8 in self.p1) and (9 in self.p1):
            winner = 1
        if(7 in self.p2) and (8 in self.p2) and (9 in self.p2):
            winner = 2

        if(1 in self.p1) and (4 in self.p1) and (7 in self.p1):
            winner = 1
        if(1 in self.p2) and (4 in self.p2) and (7 in self.p2):
            winner = 2

        if(2 in self.p1) and (5 in self.p1) and (8 in self.p1):
            winner = 1
        if(2 in self.p2) and (5 in self.p2) and (8 in self.p2):
            winner = 2

        if(3 in self.p1) and (6 in self.p1) and ( 9 in self.p1):
            winner = 1
        if(3 in self.p2) and (6 in self.p2) and (9 in self.p2):
            winner = 2

        if(1 in self.p1) and (5 in self.p1) and ( 9 in self.p1):
            winner = 1
        if(1 in self.p2) and (5 in self.p2) and (9 in self.p2):
            winner = 2

        if(3 in self.p1) and (5 in self.p1) and ( 7 in self.p1):
            winner = 1
        if(3 in self.p2) and (5 in self.p2) and (7 in self.p2):
            winner = 2

        if winner == 1:
            messagebox.showinfo(title="Congratulations.", message="Player %s is the winner" % self.igra.ploca.player1.nadimak)
            self.igra.winner = self.igra.ploca.player1
            self.igra.ploca.player1.inGame = False
            self.igra.ploca.player2.inGame = False
            self.igra.live = False

        elif winner == 2:
            messagebox.showinfo(title="Congratulations.", message="Player %s is the winner" % self.igra.ploca.player2.nadimak)
            self.igra.winner = self.igra.ploca.player2
            self.igra.ploca.player1.inGame = False
            self.igra.ploca.player2.inGame = False
            self.igra.live = False

        elif mov == 9:
            messagebox.showinfo(title="Draw", message="It's a Draw!!")
            self.igra.winner = None
            self.igra.ploca.player1.inGame = False
            self.igra.ploca.player2.inGame = False
            self.igra.live = False

    def ButtonClick(self, id):
        """updateaj plocu iz baze"""
        self.conn.sync()
        rootDb = self.conn.root()
        self.igra = rootDb["games"][self.igra.date]
        player1 = self.igra.ploca.player1
        player2 = self.igra.ploca.player2
        ploca = self.igra.ploca
        if(ploca.ActivePlayer.nadimak == self.kor.nadimak):
            if(self.kor.nadimak == player1.nadimak):
                self.SetLayout(id, "X")
                ploca.moves[self.kor.nadimak].append(id)
                ploca.mov += 1
                ploca.ActivePlayer = player2
            elif(self.kor.nadimak == player2.nadimak):
                self.SetLayout(id, "O")
                ploca.moves[self.kor.nadimak].append(id)
                ploca.mov += 1
                ploca.ActivePlayer = player1
        """zapisi u bazu"""
        self.my_transaction_manager.commit()

    def updateBoard(self):
        p1_moves = self.igra.ploca.moves[self.igra.ploca.player1.nadimak]
        p2_moves = self.igra.ploca.moves[self.igra.ploca.player2.nadimak]
        for id in p1_moves:
            self.SetLayout(id, "X")
        for id in p2_moves:
            self.SetLayout(id, "O")

    def AutoPlay(self):
        global p1; global p2
        Empty = []
        for cell in range(9):
            if(not((cell +1 in p1) or (cell +1 in p2))):
                Empty.append(cell+1)
        try:
            RandIndex = randint(0,len(Empty) -1)
            ButtonClick(Empty[RandIndex])
        except:
            pass

    def EnableAll(self):

        self.b1.state(['!disabled'])

        self.b2.state(['!disabled'])

        self.b3.state(['!disabled'])

        self.b4.state(['!disabled'])

        self.b5.state(['!disabled'])

        self.b6.state(['!disabled'])

        self.b7.state(['!disabled'])

        self.b8.state(['!disabled'])

        self.b9.state(['!disabled'])

    def DisableAll(self):

        self.b1.state(['disabled'])

        self.b2.state(['disabled'])

        self.b3.state(['disabled'])

        self.b4.state(['disabled'])

        self.b5.state(['disabled'])

        self.b6.state(['disabled'])

        self.b7.state(['disabled'])

        self.b8.state(['disabled'])

        self.b9.state(['disabled'])

    def ClearTxt(self):
        self.b1.config(text= " ")
        self.b2.config(text= " ")
        self.b3.config(text= " ")
        self.b4.config(text= " ")
        self.b5.config(text= " ")
        self.b6.config(text= " ")
        self.b7.config(text= " ")
        self.b8.config(text= " ")
        self.b9.config(text= " ")

        self.bp1.configure(bg="white", text=" ")
        self.bp2.configure(bg="white", text=" ")

    def provjeriActivPlayer(self):
        self.conn.sync()
        rootDb = self.conn.root()
        self.igra = rootDb["games"][self.igra.date]
        while True:
            if self.igra.live:
                try:
                    t = self.my_transaction_manager.begin() 
                    """updateaj plocu iz baze"""
                    self.conn.sync()
                    rootDb = self.conn.root()
                    self.igra = rootDb["games"][self.igra.date]
                    player1 = self.igra.ploca.player1
                    player2 = self.igra.ploca.player2
                    ploca = self.igra.ploca

                    self.updateBoard()
                    self.CheckWinner()
                    if self.igra.winner != None and self.igra.winner.nadimak == self.kor.nadimak:
                        self.my_transaction_manager.commit()

                    if self.igra.live == False:
                        self.clearBoard()
                        continue
                    
                    if(ploca.ActivePlayer.nadimak == player2.nadimak):
                        self.bp2.configure(bg="Yellow")
                        self.bp1.configure(bg="white")
                    elif(ploca.ActivePlayer.nadimak == player1.nadimak):
                        self.bp1.configure(bg="Yellow")
                        self.bp2.configure(bg="white")
                    if(self.kor.nadimak == ploca.ActivePlayer.nadimak):
                        self.EnableAll()
                    else:
                        self.DisableAll()
                    time.sleep(0.5)
                except transaction.interfaces.TransientError:
                    print( 'trx abort' )
                    time.sleep( 1 )
                    pass
            time.sleep(0.5)

    def clearBoard(self):
        self.ClearTxt()
        self.DisableAll()

    def Restart(self, igra):
        pl1 = igra.ploca.player1.nadimak
        pl2 = igra.ploca.player2.nadimak

        self.bp1 = Button(text=pl1, font=('Papyrus', 22, 'bold'), bg='White', fg='black',border=0, width=4)
        self.bp1.grid(row=0, column=0, sticky="nwse", ipadx=10,ipady=10)

        self.bp2 = Button(text=pl2, font=('Papyrus', 22, 'bold'), bg='White', fg='black',border=0, width=4)
        self.bp2.grid(row=0, column=2, sticky="nwse", ipadx=10,ipady=10)

        if not isinstance(self.provjeriActivPlayerThread, threading.Thread) or self.provjeriActivPlayerThread == None:
            self.provjeriActivPlayerThread = threading.Thread( target=self.provjeriActivPlayer, daemon=True )
            self.provjeriActivPlayerThread.start()

    def CheckPlayerDb(self, user):
        if not user.nadimak in self.rootDb.users:
            return

    def closeConnection(conn):
        conn.close()

    def showPlayers(self, korisnici):
        list_items = StringVar(value=korisnici)
        self.txtLive = Listbox(
            self.root,
            listvariable=list_items,
            height=6,
            selectmode='extended')

    def setBoard(self, USER_INP):
        self.root.title("Tic Tac Toe : Player "+ USER_INP) 
        self.st = ttk.Style()
        self.st.configure("my.TButton", font=('Chiller',24,'bold'))

        self.b1 = ttk.Button(root, text=" ", style="my.TButton", )
        self.b1.grid(row=1, column=0, sticky="nwse", ipadx=50,ipady=50)
        self.b1.config(command = lambda : self.ButtonClick(1))

        self.b2 = ttk.Button(root, text=" ",style ="my.TButton")
        self.b2.grid(row=1, column=1, sticky="snew", ipadx=50, ipady=50)
        self.b2.config(command = lambda : self.ButtonClick(2))

        self.b3= ttk.Button(root, text=" ",style="my.TButton")
        self.b3.grid(row=1, column=2, sticky="snew", ipadx=50,
                ipady=50)
        self.b3.config(command = lambda : self.ButtonClick(3))

        self.b4 = ttk.Button(root, text=" ",style="my.TButton")
        self.b4.grid(row=2, column=0, sticky="snew", ipadx=50,
                ipady=50)
        self.b4.config(command = lambda : self.ButtonClick(4))

        self.b5 = ttk.Button(root, text=" ",style="my.TButton")
        self.b5.grid(row=2, column=1, sticky="snew", ipadx=50,
                ipady=50)
        self.b5.config(command = lambda : self.ButtonClick(5))

        self.b6 = ttk.Button(root, text=" ",style="my.TButton")
        self.b6.grid(row=2, column=2, sticky="snew", ipadx=50,
                ipady=50)
        self.b6.config(command = lambda : self.ButtonClick(6))

        self.b7 = ttk.Button(root, text=" ",style="my.TButton")
        self.b7.grid(row=3, column=0, sticky="snew", ipadx=50,
                ipady=50)
        self.b7.config(command = lambda : self.ButtonClick(7))

        self.b8 = ttk.Button(root, text=" ",style="my.TButton")
        self.b8.grid(row=3, column=1, sticky="snew", ipadx=50,
                ipady=50)
        self.b8.config(command = lambda : self.ButtonClick(8))

        self.b9 = ttk.Button(root, text=" ",style="my.TButton")
        self.b9.grid(row=3, column=2, sticky="snew", ipadx=50,
                ipady=50)
        self.b9.config(command = lambda : self.ButtonClick(9))


        self.bs = Button(text="Play..", font=('Papyrus', 22, 'bold'), bg='Purple', fg='white',    
            border=5, width=4,command = lambda : self.addToQueue())
        self.bs.grid(row=0, column=1, sticky="we")

        self.txtLive.grid(
            column=3,
            row=0,
            sticky='nwes',
            rowspan = 4
        )
        self.txtLive.insert( "anchor", '\n--- Otvaram kanal %s ---' )

        self.provjera = threading.Thread( target=self.provjeri )
        time.sleep(2)
        self.provjera.start()
        self.DisableAll()

    def login(self):
        print( 'Login korisnika' )
        USER_INP = simpledialog.askstring(title="Name",prompt="What's your Name?:")
        korisnici = self.dohvatiNaziveKorisnika()
        if not USER_INP in korisnici:
            self.kor = self.unesiKorisnika(USER_INP)
        
        try:
            t = self.my_transaction_manager.get()  
            self.kor = self.rootDb[ 'korisnici' ][USER_INP]
            self.kor.live = True
            self.rootDb[ 'live' ][USER_INP] = self.kor
            t.commit()
        except ConflictError or ValueError:
            print( 'trx abort' )
            t.abort()
            time.sleep( 1 )
            pass 
        return self.kor

    def unesiKorisnika(self, USER_INP):
        print( 'Unos novog korisnika' )
        try:
            t = self.my_transaction_manager.get()  

            noviKorisnik = korisnik(USER_INP, '123')
            self.rootDb[ 'korisnici' ][noviKorisnik.nadimak] = noviKorisnik
            
            t.commit()
        except ConflictError or ValueError:
            print( 'trx abort' )
            t.abort()
            time.sleep( 1 )
            pass            

        return self.rootDb[ 'korisnici' ][noviKorisnik.nadimak]

    def dohvatiNaziveKorisnika(self):
        self.conn.sync()
        korisnici = [v.nadimak for k,v in self.rootDb[ 'korisnici' ].iteritems()]
        return korisnici

    def dohvatiLiveKorisnike(self):
        self.conn.sync()
        korisnici = [v.nadimak for k,v in self.rootDb[ 'live' ].iteritems()]
        return korisnici

    def provjeri(self ):
        self.jos = True
        while self.jos:
            self.conn.sync()
            list_items = self.dohvatiLiveKorisnike()
            self.txtLive.delete(0, "end")
            for msg in list_items:
                self.txtLive.insert("end", msg )
                self.txtLive.yview("end")
            time.sleep( 1 )

    def addToQueue(self):
        while True:
            try:
                if self.kor.inQueue == False:
                    print( 'Unos u kor u queue' )

                    t = self.my_transaction_manager.get()
                    self.kor.inQueue = True
                    self.rootDb[ 'queue' ].extend([self.kor])
                    t.commit()
                    self.bs.config(text="Player searching...")

                    if not isinstance(self.provjeraQueueThread, threading.Thread) or self.provjeraQueueThread == None:
                        self.provjeraQueueThread = threading.Thread( target=self.provjeraQueue, daemon=True )
                        self.provjeraQueueThread.start()
                    
                    break
            except ConflictError or ValueError:
                print( 'trx abort' )
                self.kor.inQueue = False
                t.abort()
                pass   

    def provjeraQueue(self):
        print( 'Dohvat iz queue thread' )
        while True:
            if self.kor.inQueue:
                print("player seraching")
                self.conn.sync()
                self.rootDb = self.conn.root()
                self.kor = self.rootDb[ 'korisnici' ][self.kor.nadimak]

                nextPlayer = self.dohvatiQueueKorisnika()
                self.nextPlayer = nextPlayer

                if self.nextPlayer != [] and self.kor.inQueue == False:
                    self.bs.config(text="New Game")
                    self.makeGame(self.kor, self.nextPlayer)

                if self.kor.inGame and self.kor.inQueue:    
                    self.bs.config(text="New Game")
                    self.findGame()
            time.sleep( 1 )

    def dohvatiQueueKorisnika(self):
        print( 'Dohvat iz queue upitti' )
        try:
            if len(self.rootDb[ 'queue' ]) == 0:
                return []

            nextPlayer = self.rootDb[ 'queue' ][0]            
            if nextPlayer.nadimak == self.kor.nadimak or nextPlayer.inGame == True or self.kor.inGame == True:
                return []

            del self.rootDb[ 'queue' ][0]
            """delete sebe"""
            for i in range(len(self.rootDb[ 'queue' ])):
                if self.rootDb[ 'queue' ][i].nadimak == self.kor.nadimak:
                    del self.rootDb[ 'queue' ][i] 
                    break

            self.kor.inQueue = False
            self.kor._p_changed = True

            self.my_transaction_manager.commit()
            return nextPlayer
        except ConflictError or ValueError:
            print( 'trx abort' )
            time.sleep( 1 )
            pass   

    def makeGame(self, player1, player2):
        print("make game ")
        gameMaking = True
        while gameMaking:
            try:
                self.conn.sync()
                self.rootDb = self.conn.root()

                ploca = Ploca(player1, player2)
                igra = Igra(ploca, time.time())
                igra.live = True
                self.rootDb["games"][igra.date] = igra

                self.kor.inGame = True
                player2.inGame = True
                self.kor._p_changed = True
                player2._p_changed = True

                self.my_transaction_manager.commit()
                gameMaking = False
                self.igra = igra
                self.Restart(igra)
            except ConflictError or ValueError:
                print( 'trx abort' )
                time.sleep( 1 )
                pass   
            time.sleep(1)

    def findGame(self):
        print("find game ")
        gameFinding = True
        igra = None
        while gameFinding:

            self.conn.sync()
            self.rootDb = self.conn.root()
            self.kor = self.rootDb["korisnici"].get(self.kor.nadimak)
            
            try:
                igra = [g for k,g in self.rootDb["games"].items() if g.ploca.player2.nadimak == self.kor.nadimak and g.live == True][0]
                if igra != None:
                    if self.kor.inQueue == True and self.kor.inGame == True:
                        self.kor.inQueue = False
                        self.kor._p_changed = True
                        self.my_transaction_manager.commit()
                        self.igra = igra
                        gameFinding = False
                        self.Restart(igra)
            except IndexError:
                igra = None
                t.abort()
                time.sleep( 1 )
                pass
            time.sleep(1)

    def log(self, player):
        print("LOG " + player.nadimak)
        for k,v in self.rootDb[ 'korisnici' ].items():
            print("k"+player.nadimak+" " + str(v.inGame))

    def logOut(self):
        self.conn.sync()
        self.rootDb = self.conn.root()
        try:
            t = self.my_transaction_manager.get()  
            self.kor.live = False
            self.kor.inQueue = False
            self.kor.inGame = False
            self.kor._p_changed = True

            del self.rootDb[ 'live' ][self.kor.nadimak] 

            for i in range(len(self.rootDb[ 'queue' ])):
                if self.rootDb[ 'queue' ][i].nadimak == self.kor.nadimak:
                    del self.rootDb[ 'queue' ][i] 
                    break
            
            for k,g in self.rootDb["games"].items():
                del self.rootDb[ 'games' ][g.date]

            t.commit()
        except ConflictError or ValueError:
            print( 'trx abort' )
            t.abort()
            time.sleep( 1 )
            pass   

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.jos = False
            self.logOut()
            self.next = False
            self.root.destroy()

if __name__ == '__main__':
    root = Tk()
    ap = Aplikacija(root)
    kor = ap.login()
    if kor.nadimak != "":
        print("Ispis ploče")
        
        ap.showPlayers(ap.dohvatiNaziveKorisnika())
        ap.setBoard(kor.nadimak)
        
        root.resizable(0,0)
        root.protocol("WM_DELETE_WINDOW", ap.on_closing)
        root.mainloop() 




