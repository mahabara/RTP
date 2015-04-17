# -*- coding: cp936 -*-
#Created on 2015年3月19日

#@author: etbcffg

import wx,serial
import MessageQueue
from cmdDocPaser import *
from deviceConfigParser import *
from deviceAgentFactory import *
from log4 import log4



class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)
        
class inputPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.singleText = wx.TextCtrl(self, -1, u'Please input here', size=(175, 25),style=(wx.TE_PROCESS_ENTER))
        self.singleText.SetBackgroundColour('green')
        self.singleText.SetInsertionPoint(0)
        self.sizer.Add(self.singleText, 2)
        
        self.buttons = []
        self.lock = wx.Button(self,-1,'Lock',size=(85,25))
        self.load = wx.Button(self,-1,'Load',size=(85,25))
        self.save = wx.Button(self,-1,'Save',size=(85,25))
        self.buttons.append(self.lock)
        self.buttons.append(self.load)
        self.buttons.append(self.save)
        
        
        for i in range(3):
            
            self.sizer.Add(self.buttons[i])
        
        self.SetSizer(self.sizer)
        
    
            #self.parent.ser.write(data+'\n')
            #-------------------------------------------------- if len(data)!=0:
                #------------------------------ self.parent.ser.write(data+'\n')
        
    
        
class TabPage(wx.Notebook):
    def __init__(self,parent,cmddocument=None):
        wx.Notebook.__init__(self,parent)
        self.parent = parent
        self.tabs=[]
        if cmddocument == None:
            self.tab = cjlists(self)
            self.AddPage(self.tab, "new set")
        else:
            
            self.doc = cmddocument
            j = 0
            for i in self.doc.tabs:
                tab = cjlists(self,i.buttons)
##                for  k in i.buttons:
##                    print k.name
                self.tabs.append(tab)
                self.AddPage(self.tabs[j],i.tabname)
                j+=1
        
    
class cjlists(wx.Panel):
    def __init__(self,parent,btnvals=[]):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.sizer = wx.GridBagSizer(hgap=5, vgap=5)
        self.buttons = []
        self.btnvals = []
        self.bindpool = {}
        i = 0
        if len(btnvals) == 0:
            
            for row in range(4):
                for col in range(8):
                    btnvalue = buttontype(i)
                    self.btnvals.append(btnvalue)
                    button = wx.Button(self, -1,self.btnvals[i].name,size=(85,25))
                    self.buttons.append(button)
                    self.buttons[i].Bind(wx.EVT_LEFT_DOWN, self.OnClick)
                    self.buttons[i].Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
                    self.bindpool[self.buttons[i]] = self.btnvals[i]
                    self.sizer.Add(self.buttons[i], pos=(row,col))
                    i+=1
        else:
            #print 'buttons != 0'
            #print len(buttons)
##            for k in buttons:
##                print k.name
            for row in range(4):
                for col in range(8):
##                    print buttons[i].name 
                    
                    self.btnvals.append(btnvals[i])
                    button = wx.Button(self, -1,  self.btnvals[i].name,size=(85,25))
                    self.buttons.append(button)
                    
                    self.buttons[i].Bind(wx.EVT_LEFT_DOWN, self.OnClick)
                    self.buttons[i].Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
                    self.buttons[i].value = self.btnvals[i]
                    #self.bindpool[self.buttons[i]] = self.btnvals[i]
                    self.sizer.Add(self.buttons[i], pos=(row,col))
                    i+=1
        self.SetSizer(self.sizer)

    def SetButtons(self,tabcontent):
        
        self.buttons = []
        
        for j in tabcontent.buttons:
            self.buttons[i].SetLabel(j.buttonname)
            self.buttons[i].SetData(j.data)
            
        

    def SaveButtons(self):
        pass

    def OnClick(self,event):
        #print 'haha'
        #print self.parent.parent.prtname
        data = event.GetEventObject().value.data
        #print data
        if  len(event.GetEventObject().value.name.strip()) !=0:
            if len(data) == 1 and len(data[0].strip())==0:
                self.logger.logging('data contain space!')
                
                #------------------------------------ print 'data contain space'
            #execute command    
            else:
                for c in data:
                    if len(c.strip())!=0:
                        if '.' not in c:
                            self.parent.parent.ser.write(c+'\n')
                        
                        else:
                            if 'SA.Command' in c:   #process SA commands:'SA.Command::SYST:PRESET'
                                cmdstr = c.replace('SA.Command:','')
                                agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_SIGNALANALYZER)

                            elif 'SG.Command' in c:   #process SG commands:'SG.Command:SOURce1:BB:EUTR:STAT ON'
                                cmdstr = c.replace('SG.Command:','')
                                agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_SIGNALGENERATOR)
                            
                            elif 'RF-Box.' in c:   ##process RF-BOX commands
                                cmdstr = c.replace('RF-Box.','')
                                agent = deviceAgentFactory.get_DeviceAgent(constants.DEVICE_NAME_RFBOX)
                            
                            agent.cmd(c)
                #----- print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
                #---------------------------------------------- for r in retval:
                    #--------------------------------------------------- print r
    def OnRightClick(self,event):
        #print 'hehehehehe'
        #print self.bindpool[event.GetEventObject()].data
        
        dlg = CmdEditDialog(event.GetEventObject().value)
        dlg.ShowModal()


        
class CmdEditDialog(wx.Dialog):
    
    def __init__(self,btnval):
        
        wx.Dialog.__init__(self, None, -1, "Command Editor")
        self.btnval = btnval
        # Create the text controls
        

        # 绑定验证器
        
        self.name_t  = wx.TextCtrl(self, -1, size=(100, 25))
        self.data_t = wx.TextCtrl(self, -1,size=(200,200),style=(wx.TE_MULTILINE|wx.EXPAND|wx.TE_AUTO_SCROLL|wx.TE_DONTWRAP))
        
        self.name_t.write(btnval.name)
        for d in btnval.data:
            
            self.data_t.AppendText(d+'\n')
            
        # Use standard button IDs
        okay   = wx.Button(self, wx.ID_OK)
        okay.Bind(wx.EVT_BUTTON, self.SaveCmd)
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        # Layout with sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sizer.Add(self.name_t, 0, wx.EXPAND)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        
       
        self.sizer.Add(self.data_t, 0, wx.EXPAND)
        

        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        self.sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
    
    def SaveCmd(self,e):
        #datalist = []
        self.btnval.name=self.name_t.GetValue()
        datalist = self.data_t.GetValue().split(r'\n')
        self.btnval.data = []
        for d in datalist:
            if d != '':
                
                self.btnval.data.append(d)        
        self.Destroy()

class ConnEditDialog(wx.Dialog):
    
    def __init__(self,addrdict):
        
        wx.Dialog.__init__(self, None, -1, "Connection Editor")
        self.addrdict = addrdict
        # Create the text controls
        

        # 绑定验证器
        self.RRU_l = wx.StaticText(self,-1,constants.DEVICE_NAME_RRU)
        self.RRU_v  = wx.TextCtrl(self, -1, size=(100, 25))
        self.SIGNALANALYZER_l = wx.StaticText(self,-1,constants.DEVICE_NAME_SIGNALANALYZER)
        self.SIGNALANALYZER_v  = wx.TextCtrl(self, -1, size=(100, 25))
        self.SIGNALGENERATOR_l = wx.StaticText(self,-1,constants.DEVICE_NAME_SIGNALGENERATOR)
        self.SIGNALGENERATOR_v  = wx.TextCtrl(self, -1, size=(100, 25))
        self.RFBOX_l = wx.StaticText(self,-1,constants.DEVICE_NAME_RFBOX)
        self.RFBOX_v  = wx.TextCtrl(self, -1, size=(100, 25))
        self.RRU_v.SetValue(addrdict[constants.DEVICE_NAME_RRU])
        self.SIGNALANALYZER_v.SetValue(addrdict[constants.DEVICE_NAME_SIGNALANALYZER])
        self.SIGNALGENERATOR_v.SetValue(addrdict[constants.DEVICE_NAME_SIGNALGENERATOR])
        self.RFBOX_v.SetValue(addrdict[constants.DEVICE_NAME_RFBOX])    
        # Use standard button IDs
        okay   = wx.Button(self, wx.ID_OK)
        okay.Bind(wx.EVT_BUTTON, self.SaveConn)
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        # Layout with sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sizer.Add(self.RRU_l, 0)
        self.sizer.Add(self.RRU_v, 0, wx.EXPAND)
        self.sizer.Add(self.SIGNALANALYZER_l, 0)
        self.sizer.Add(self.SIGNALANALYZER_v, 0, wx.EXPAND)
        self.sizer.Add(self.SIGNALGENERATOR_l, 0)
        self.sizer.Add(self.SIGNALGENERATOR_v, 0, wx.EXPAND)
        self.sizer.Add(self.RFBOX_l, 0)
        self.sizer.Add(self.RFBOX_v, 0, wx.EXPAND)
        
        
        

        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        self.sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
    
    def SaveConn(self,event):
        self.addrdict[constants.DEVICE_NAME_RRU] = self.RRU_v.GetValue()
        self.addrdict[constants.DEVICE_NAME_SIGNALANALYZER] = self.SIGNALANALYZER_v.GetValue()
        self.addrdict[constants.DEVICE_NAME_SIGNALGENERATOR] = self.SIGNALGENERATOR_v.GetValue()
        self.addrdict[constants.DEVICE_NAME_RFBOX] = self.RFBOX_v.GetValue()
        
        
        #save connection info
        ccp = ConnectionsConfigParser()
        ccp.set_Address(self.addrdict)      
        self.Destroy()
    
                
class MultiText(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.control = wx.TextCtrl(self, -1,size=(250,350),style=(wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.EXPAND|wx.TE_READONLY|wx.TE_AUTO_SCROLL|wx.TE_DONTWRAP|wx.TE_RICH))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.control, -1)
        self.control.SetInsertionPoint(0)
        self.SetSizer(self.sizer)
        self.control.SetDefaultStyle(wx.TextAttr('#0000FF'))
        # redirect text here
        redir=RedirectText(self.control)
        sys.stdout=redir

    
        

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        
        self.dirname=''
        ccp = ConnectionsConfigParser()
        self.addressDict = ccp.addressDict
        self.logger = log4()
        
        
        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
##        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
##        self.multiLabel=wx.StaticText(self,-1,"Multi-Line:")
        
        self.stbar = self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.toolbar  = self.CreateToolBar()
        self.createToolbarItem_conn("conn", "icon/conn1.png", self.OnConnect)
        self.toolbar.Realize()
        #self.createSimpleTool()
        # Setting up the menu.
        
        #filemenu
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        #connection menu
        devicemenu = wx.Menu()
        menuconn = devicemenu.Append(-1,'&Conn','Open a Dialog to edit connection of devices')
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(devicemenu,"&Device")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        

        #MultiText
        self.MultiText = MultiText(self)
        #buttons
        self.inputPanel = inputPanel(self)
        
        #tab-buttons
        #file = r'C:\work\new-RPV\2208_tor_tx_20150113.ts'
        #self.cmdDoc = commandConfigParser().getCmdDoc(file)
        self.tabpage = TabPage(self)
##        self.nb = wx.Notebook(self)
##        self.nb.AddPage(cjlists(self.nb), "new set")
##        self.nb.AddPage(cjlists(self.nb), "new set")
##        self.nb.AddPage(cjlists(self.nb), "new set")


        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.MultiText, 2, wx.EXPAND)
        self.sizer.Add(self.inputPanel, 0, wx.EXPAND)
        
        self.sizer.Add(self.tabpage, 0, wx.EXPAND)
##        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()

    # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnConnMenu, menuconn)
        self.Bind(wx.EVT_BUTTON, self.LoadButtons, self.inputPanel.load)
        self.Bind(wx.EVT_BUTTON, self.OnLock, self.inputPanel.lock)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.inputPanel.save)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.inputPanel.singleText)
        
        #self.toolbar.EnableTool(wx.ID_CUT,False)
        #------------------------------- for t in range(self.tabpage.PageCount):
            #-------------------------------------- for self.tabpage.GetPage(t):
                
    #start RRU_trace_read_thread
        self.ser = None
        #-------------------------------------------------- if self.ser == None:
            #-------------------------------------------------------------- try:
                # self.ser = serial.Serial(int(self.addressDict[constants.DEVICE_NAME_RRU])-1,9600)
                #---------------------------------------- self.ser.timeout = 0.5
                # self.RRU_trace_display_thread = MessageQueue.RRU_trace_display_thread(self.ser)
                #------------------------- self.RRU_trace_display_thread.start()
#------------------------------------------------------------------------------ 
            #----------------------------------------------------------- except:
                # self.logger.logging('Wrong serial port, please check and reset the serial port!')
                #self.logger.logging(self.ser)
                #print 'Wrong serial port, please check and reset the serial port!'
                #print self.ser
        
        
        #self.RRU_trace_print_thread = MessageQueue.RRU_trace_print_thread(self.rru_trace_queue)
        #time.sleep(15)
        
        #self.RRU_trace_print_thread.start()
        
    def onEnter(self,e):
        data = self.inputPanel.singleText.GetValue()
        #------------------------------------------------------- b = bytearray()
        #-------------------------------------------- for item in data.encode():
            #--------------------------------------------------- print item,' 2'
            #---------------------------------------------------- b.append(item)
        #-------------------------------------------------------- print bytes(b)
        if self.ser != None: 
            if len(data.strip())!=0:
                #need encode!!!
                self.ser.write(data.rstrip().encode()+'\n')
            
                
    def OnSave(self,Event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            c = commandConfigParser()
            c.SaveCmdDoc(self.cmdDoc,self.dirname+os.path.sep+self.filename)
            
        dlg.Destroy()
        
        
    def OnLock(self,event):
        if self.inputPanel.lock.GetLabel() == 'Lock':
            #----------------------------- print self.inputPanel.lock.GetLabel()
            self.tabpage.Disable()
            self.inputPanel.lock.SetLabel('Unlock')
        else:
            #----------------------------- print self.inputPanel.lock.GetLabel()
            self.tabpage.Enable()
            self.inputPanel.lock.SetLabel('Lock')
        
        
    def LoadButtons(self,event):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            c = commandConfigParser()
            self.cmdDoc = c.getCmdDoc(self.dirname+os.path.sep+self.filename)
            self.sizer.Hide(self.tabpage, 3)
            self.sizer.Remove(self.tabpage)
            self.tabpage = TabPage(self,self.cmdDoc)
            self.sizer.Add(self.tabpage, 0, wx.EXPAND)
            self.sizer.Layout()
            self.Fit()
        dlg.Destroy()
    
    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " A simple tool to control device \n write with wxPython", "About RTP", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        
        self.Close(True)  # Close the frame.
        e.Skip()

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            c = commandConfigParser()
            self.cmdDoc = c.getCmdDoc(self.dirname+os.path.sep+self.filename)
            self.sizer.Hide(self.tabpage, 3)
            self.sizer.Remove(self.tabpage)
            self.tabpage = TabPage(self,self.cmdDoc)
            self.sizer.Add(self.tabpage, 0, wx.EXPAND)
            self.sizer.Layout()
            self.Fit()
        dlg.Destroy()
    
    
    


    def createToolbarItem_conn(self, label, imageName, method):
        self.toolbar.RemoveTool(1)
        self.toolbar.AddLabelTool(1, label, wx.Bitmap(imageName))
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, method, id=1)
        
    
    
             
    def OnConnect(self,e):
        
        if self.ser == None:
            try:
                self.ser = serial.Serial(int(self.addressDict[constants.DEVICE_NAME_RRU])-1,9600)
                self.ser.timeout = 0.5
                self.RRU_trace_display_thread = MessageQueue.RRU_trace_display_thread(self.ser)
                self.RRU_trace_display_thread.start()
                self.createToolbarItem_conn("Stop", "icon/cut1.png", self.OnDisConnect)
            except:
                self.logger.logging('Wrong serial port, please check and reset the serial port!')
                #self.logger.logging(self.ser)
                # print 'Wrong serial port, please check and reset the serial port!'
                #------------------------------------------------ print self.ser
    
        else:
            try:
                self.RRU_trace_display_thread = MessageQueue.RRU_trace_display_thread(self.ser)
                self.RRU_trace_display_thread.start()
                self.createToolbarItem_conn("Stop", "icon/cut1.png", self.OnDisConnect)
            except:
                self.logger.logging('Wrong serial port, please check and reset the serial port!')
                
    def OnDisConnect(self,e):
        if self.ser != None:
            try:
                self.RRU_trace_display_thread.stopFlag = True
                time.sleep(0.5)
                self.ser.close()
                self.createToolbarItem_conn("conn", "icon/conn1.png", self.OnConnect)
            except:
                self.logger.logging('Close serial port failed!')
        
        
    def OnConnMenu(self,e):
        dlg = ConnEditDialog(self.addressDict)
        dlg.ShowModal()
    
    def OnClose(self,e):
        if self.ser != None:
            self.RRU_trace_display_thread.stopFlag = True
            self.RRU_trace_display_thread.join(1)
            self.ser.close()
        
        e.Skip()

class MyApp(wx.App):

    def __init__(self):
        print "App __init__"
        wx.App.__init__(self)

    def OnInit(self):
        print "OnInit"    #输出到stdout
        
        self.frame = MainWindow(None, "RTP")  #创建框架
        self.frame.Show()
        self.SetTopWindow(self.frame)
        
        
        #print    sys.stderr, "A pretend error message"    #输出到stderr
        return True

           
        
app = MyApp()
#frame = MainWindow(None, "RTP")
app.MainLoop()
