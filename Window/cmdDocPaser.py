
class tabcontent():
    def __init__(self,tabname):
        self.tabname = tabname
        self.buttons = []
        for i in range(32):
            
            self.buttons.append(buttontype(i,''))

    

    

class buttontype():
    def __init__(self,buttonnumber=0,buttonname=''):
        self.number = buttonnumber
        self.name = buttonname
##        print self.name
        self.data = []

    def SetData(self,data):
        self.data = data
        
        

class cmddocument():
    def __init__(self):
        self.tabs = []
        
        
class commandConfigParser():
    def __init__(self):
        pass
            

        
    def getCmdDoc(self,file):
        f = open(file).read()
        self.doc = cmddocument()
        contentall = f.splitlines()
        tabstart = 0
        tablength = []
        i = 0
        for c in contentall:
            if  c.startswith('<tab'):
            
                tabstart = i
                tabname = c[c.find('{')+1:c.find('}')]
                tab = tabcontent(tabname)
                j = 0
                #print 'tabname',tabname
                #print 'tabstart',tabstart
                tablength = contentall[tabstart:]
##                print tablength
                for t in tablength:
                    if t.startswith('</tab'):
                        
                        #print 'tab.buttons is ',len(tab.buttons)
                        break
                    else:
                        if t.startswith('<button'):
                            btstart = j
                            button = buttontype(t[t.find('{')+1:t.find('}')],t[t.rfind('{')+1:t.rfind('}')])
                            #print button.name
                            k = 0
                            btlength = tablength[btstart+1:]
                            for b in btlength:
                                if b.startswith('</button'):
                                    
                                    break
                                else:
                                    if b.startswith('<data')==False and b.startswith('</data')==False:
                                        if b != '<icon>' and b != '</icon>' and b!='<desc>' and b!= '</desc>':
                                            button.data.append(b)
                                
                                k+=1
                            tab.buttons[int(button.number)]=button
                            #print 'j==',j
                    
                    j+=1
                
                self.doc.tabs.append(tab)
            i+=1
        return self.doc
    
    def SaveCmdDoc(self,cmddocument,file):
        f = open(file,'w')
        for tab in cmddocument.tabs:
            f.writelines('<tab {'+tab.tabname+'}>\n')
            for bt in tab.buttons:
                if len(bt.data)!=0:
                    
                    f.writelines('<button {'+str(bt.number)+'}'+' {'+bt.name+'}>\n')
                    f.writelines('<data>\n')
                    for dt in bt.data:
                        f.writelines(dt+'\n')
                    f.writelines('</data>\n')
                    f.writelines('</button>\n')
            f.writelines('</tab>\n')
        f.close()
            
if __name__=="__main__":
                 
    c = commandConfigParser()
    c.getCmdDoc(r'C:\work\new-RPV\2216-rpv.ts')
    c.SaveCmdDoc(c.doc,r'C:\work\new-RPV\new-rpv.ts')
    for i in  c.doc.tabs:
        print 'tabname is=======================',i.tabname
        for j in i.buttons:
            print 'button name is-----------------------',j.name

