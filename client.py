import socket
import pickle
import threading
import time

import os
from tkinter import *
from tkinter import font
from tkinter import ttk

PORT = 5000
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '192.168.1.26'
ADDRESS = (SERVER, PORT)

#client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#client.connect(ADDRESS)


 
# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
        self.name = None
        self.client = None
        self.isConnected = False
        self.hand = []

        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.createLoginWindow()
        #self.goAhead('Mauricio')
        self.Window.mainloop()
 

    def connectToServer(self):
        while True:
            try:
                self.addMsgToBroadcastMsgBox('Connection to server...')
                 
                self.client = socket.socket(socket.AF_INET,
                                      socket.SOCK_STREAM)
                
                self.client.connect(ADDRESS)
                self.isConnected = True
                print('Connected to the server\n')
                break
            except:
                time.sleep(1)
                pass
        self.sendMessage({'NAME': self.name})

    def createLoginWindow(self):
        print('Creating loggin window\n')
        # login window
        self.loginWindow = Toplevel()
        # set the title
        self.loginWindow.title("Login")
        self.loginWindow.resizable(width = False,
                             height = False)
        self.loginWindow.configure(width = 400,
                             height = 300)
        # create a Label
        pls = Label(self.loginWindow,
                       text = "Please login to continue",
                       justify = CENTER,
                       font = "Helvetica 14 bold")
         
        pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
        # create a Label
        labelName = Label(self.loginWindow,
                               text = "Name: ",
                               font = "Helvetica 12")
         
        labelName.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.2)
         
        # create a entry box for
        # tyoing the message
        entryName = Entry(self.loginWindow,
                             font = "Helvetica 14")
         
        entryName.place(relwidth = 0.4,
                        relheight = 0.12,
                        relx = 0.35,
                        rely = 0.2)
         
        # set the focus of the cursor
        entryName.focus()
         
        # create a Continue Button
        # along with action
        new = Button(self.loginWindow,
                    text = "New",
                    font = "Helvetica 14 bold",
                    command = lambda: self.newGame(entryName.get()))
         
        new.place(relx = 0.3,
                 rely = 0.55)

        join = Button(self.loginWindow,
                    text = "Join",
                    font = "Helvetica 14 bold",
                    command = lambda: self.joinGame(entryName.get()))
         
        join.place(relx = 0.5,
                 rely = 0.55)

        self.loginWindow.mainloop()

    def createNumPlayerWindow(self):
        print('Creating Number of Players Window\n')
        self.nPlayerWindow = Toplevel()
        self.nPlayerWindow.title("Number of Players")
        self.nPlayerWindow.resizable(width = False,
                             height = False)
        self.nPlayerWindow.configure(width = 400,
                             height = 300)
        pls = Label(self.nPlayerWindow,
                       text = "Please enter the number of players",
                       justify = CENTER,
                       font = "Helvetica 14 bold")
        pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
        labelNumPlayer = Label(self.nPlayerWindow,
                               text = "Number: ",
                               font = "Helvetica 12")
         
        labelNumPlayer.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.2)
        entryNumPlayer = Entry(self.nPlayerWindow,
                             font = "Helvetica 14")
         
        entryNumPlayer.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
        entryNumPlayer.focus()
         
        # create a Continue Button
        # along with action
        
        go = Button(self.nPlayerWindow,
                    text = "CONTINUE",
                    font = "Helvetica 14 bold",
                    command = lambda: self.getNumOfPlayer(entryNumPlayer.get()))
         
        go.place(relx = 0.4,
                 rely = 0.55)

    def createBetWindow(self):
        print('Creating Bet Window\n')
        self.betWindow = Toplevel()
        self.betWindow.title("Bet")
        self.betWindow.resizable(width = False,
                             height = False)
        self.betWindow.configure(width = 400,
                             height = 300)
        pls = Label(self.betWindow,
                       text = "Please enter your bet",
                       justify = CENTER,
                       font = "Helvetica 14 bold")
        pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
        labelBet = Label(self.betWindow,
                               text = "Number: ",
                               font = "Helvetica 12")
         
        labelBet.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.2)
        entryBet = Entry(self.betWindow,
                             font = "Helvetica 14")
         
        entryBet.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
        entryBet.focus()
         
        # create a Continue Button
        # along with action
        
        go = Button(self.betWindow,
                    text = "CONTINUE",
                    font = "Helvetica 14 bold",
                    command = lambda: self.getBet(entryBet.get()))
         
        go.place(relx = 0.4,
                 rely = 0.55)
                 
    def getBet(self, num):
        self.Window.deiconify()
        print('Destroying Number of Players Window\n')
        self.betWindow.destroy()
        
        msg = {"BET":int(num)}
        snd= threading.Thread(target = self.sendMessage,
                              args = (msg,))
        snd.start()

    def getNumOfPlayer(self, num):
        self.Window.deiconify()
        print('Destroying Number of Players Window\n')
        #self.nPlayerWindow.destroy()
        
        msg = {"N_PLAYERS":int(num)}
        snd= threading.Thread(target = self.sendMessage,
                              args = (msg,))
        snd.start()
        
    def newGame(self, name):
        print('Destroying logging window\n')
        self.loginWindow.destroy()
        self.name = name
        self.layout()
        
        conect = threading.Thread(target=self.connectToServer)
        conect.start()
        
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def joinGame(self, name):
        print('Destroying logging window\n')
        self.loginWindow.destroy()
        self.name = name
        self.layout()
        
        conect = threading.Thread(target=self.connectToServer)
        conect.start()

        rcv = threading.Thread(target=self.receive)
        rcv.start()
        
    def creatScoreBox(self):
        self.scoreBox = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.scoreBox.place(relheight = 0.5,
                            relwidth = 0.2,
                            rely = 0.1,
                            relx = 0.8)
        self.addMsgToScoreBox([])

    def creatHandBox(self):
        self.handBox = Canvas(self.Window)
        self.handBox.place(relheight = 0.25,
                            relwidth = 0.8,
                            rely = 0.75,
                            relx = 0)
        self.imgCards = os.listdir('images/')
        for i,imagem in enumerate(self.imgCards):
            self.imgCards[i] = PhotoImage(name=imagem[:-4],
                                          file='images/'+imagem)
                                          
    def creatTableBox(self):
        self.tableBox = Canvas(self.Window)
        self.tableBox.place(relx = 0.2,
                            rely = 0.10,
                            relheight = 0.55,
                            relwidth = 0.4)
                            
        self.imgTable = PhotoImage(file="table.png")
        self.tableBox.create_image(0,0,anchor=NW, image=self.imgTable)
                            
        self.imgCardsTable = os.listdir('images_table/')
        for i,imagem in enumerate(self.imgCardsTable):
            self.imgCardsTable[i] = PhotoImage(name=imagem[:-4]+'_table',
                                          file='images_table/'+imagem)
        
    def creatBroadcastMsgBox(self):
        self.broadcastMsgBox = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.broadcastMsgBox.place(relheight = 0.35,
                            relwidth = 0.2,
                            rely = 0.6,
                            relx = 0.8)
        self.broadcastMsgBox.config(cursor = "arrow")
        scrollbar = Scrollbar(self.broadcastMsgBox)
        scrollbar.place(relheight = 1,
                        relx = 0.974)
        scrollbar.config(command = self.broadcastMsgBox.yview)
        self.broadcastMsgBox.config(state = DISABLED)

    def creatEntryMsg(self):    
        self.entryMsg = Entry(self.Window,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
        self.entryMsg.place(relwidth = 0.15,
                            relheight = 0.05,
                            rely = 0.95,
                            relx = 0.8)
         
        self.entryMsg.focus()

    def creatSendButton(self):
        self.buttonMsg = Button(self.Window,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx = 0.95,
                             rely = 0.95,
                             relheight = 0.05,
                             relwidth = 0.05)

    # The main layout of the chat
    def layout(self):
        print('Creating main window\n')
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.state('zoomed')
        self.Window.configure(bg = "#17202A")
        
        self.labelHead = Label(self.Window,
                             bg = "#17202A",
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
         
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
         
        self.creatScoreBox()
        self.creatBroadcastMsgBox()
        self.creatEntryMsg()
        self.creatSendButton()
        self.creatHandBox()
        self.creatTableBox()
        
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        print(f'Sending msg to the server = {msg}\n')
        msg = {"CHAT": f"{self.name}: {msg}"}
        self.entryMsg.delete(0, END)
        snd= threading.Thread(target = self.sendMessage,
                              args = (msg,))
        snd.start()
 
    def addMsgToScoreBox(self, players):
        print(f'addMsgToScoreBox\n')
        self.scoreBox.config(state = NORMAL)
        self.scoreBox.delete(1.0,END)
        self.scoreBox.insert(END,'-------------------SCORE------------------\n')
        for player in players:
            self.scoreBox.insert(END,player+'\n')
        self.scoreBox.config(state = DISABLED)
        self.scoreBox.see(END)

    def addMsgToBroadcastMsgBox(self, msg):
        print(f'addMsgToBroadcastMsgBox\n')
        self.broadcastMsgBox.config(state = NORMAL)
        self.broadcastMsgBox.insert(END,msg+"\n\n")
        self.broadcastMsgBox.config(state = DISABLED)
        self.broadcastMsgBox.see(END)
      
    
    def updateTableBox(self, table):
        self.tableBox.delete("all")
        self.tableBox.create_image(0,0,anchor=NW, image=self.imgTable)
        for i,card in enumerate(table):
            for imagem in self.imgCardsTable:
                print(f'{imagem.name} == {card.value}_of_{card.suit}_table')
                if imagem.name == f'{card.value}_of_{card.suit}_table':
                    self.tableBox.create_image(i*75+150,150, anchor=NW, image=imagem)
    
    def updateHandBox(self, hand):
        self.handBox.delete("all")
        self.hand = hand
        for i,card in enumerate(hand):
            for imagem in self.imgCards:
                print(f'{imagem.name} == {card.value}_of_{card.suit}')
                if imagem.name == f'{card.value}_of_{card.suit}':
                    self.handBox.create_image(i*150,20, anchor=NW, image=imagem)
    
    
    def canvas_click_event(self, event):
        carta = event.x//150
        if carta < len(self.hand):
            print('card selected')
            self.sendMessage({"PICK": self.hand[carta]})
            self.entryMsg.focus()

    
    def chooseCard(self):
        self.handBox.bind('<Button-1>', self.canvas_click_event)
        self.handBox.focus_set()
    
    # function to receive messages
    def receive(self):
        while True:
            time.sleep(0.01)
            if self.isConnected:
                try:
                    msg = self.client.recv(1024)
                    print(msg)
                    message = pickle.loads(msg)
                    print(f'Message from server = {message}\n') 
                    for key, value in message.items():
                        if key == 'NAME':
                            self.sendMessage({"NAME": self.name})
                        elif key == 'N_PLAYERS':
                            self.getNumOfPlayer(2)
                            #self.Window.iconify()
                            #conect = threading.Thread(target=self.createNumPlayerWindow)
                            #conect.start()
                            #time.sleep(5)
                        elif key == 'CHAT':
                            print('adding to chat')
                            self.addMsgToBroadcastMsgBox(value)
                        elif key == 'SCORES':
                            self.addMsgToScoreBox(value)
                        elif key == 'HAND':
                            self.updateHandBox(value)
                        elif key == 'TABLE':
                            self.updateTableBox(value)
                        elif key == 'PICK':
                            #self.sendMessage({"PICK": self.hand[0]})
                            self.addMsgToBroadcastMsgBox("Pick your CARD!!!")
                            self.chooseCard()
                        elif key == 'BET':
                            #self.getBet(1)
                            #self.Window.iconify()
                            conect = threading.Thread(target=self.createBetWindow)
                            conect.start()
                            time.sleep(5)
                        else:
                            print(key, value)
                except:
                    # an error will be printed on the command line or console if there's an error
                    print("An error occured!")
                    self.client.close()
                    break
         
    # function to send messages
    def sendMessage(self, msg):
        print(f'Sending message to server = {msg}\n') 
        if self.isConnected:
            while True:
                self.client.send(pickle.dumps(msg))
                break   
 
# create a GUI class object
g = GUI()
