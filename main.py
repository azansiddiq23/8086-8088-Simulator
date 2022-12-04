def memory_block(self, memorylist, highlighter):
        root = self.root

        tempFr = Frame(root, width=480, height=585, bg="#162121")
        tempFr.place(x=852, y=122, anchor="nw")

        MemFrame = Frame(root, width=480, height=585,
                         bg="#294040",
                         highlightthickness=2,
                         highlightbackground="#528080")
        MemFrame.place(x=850, y=120, anchor="nw")

        memoryLbl = Label(MemFrame, text="Memory Block", fg="#93dbd8",
                          font="Arial 14 bold", bg="#294040")
        memoryLbl.place(x=30, y=18, anchor="nw")

        hexArray = ["A", "B", "C", "D", "E", "F"]

        MemBlocksUpper = [0, 0, 0, 0, 0, 0, 0, 0]
        MemBlocksLower = [0, 0, 0, 0, 0, 0, 0, 0]

        LowerMemBlocks = [memorylist[i] for i in range(0, 8)]
        UpperMemBlocks = [memorylist[i] for i in range(8, 16)]

        Memlabels = []
        for i in range(8):
            j = "0000"+str(i)

            MemBlocksUpper[i] = Label(MemFrame, text=j, bg="#294040",
                                      fg="#61baba", font="Arial 13 bold",)
            MemBlocksUpper[i].place(x=25, y=80+(i*63), anchor="nw")

            MemLabel = Label(MemFrame, text=LowerMemBlocks[i],
                             height=2, width=11, font="Arial 14 bold",
                             bg="#476b6a", fg="white")
            MemLabel.place(x=85, y=68+(i*63), anchor="nw")
            Memlabels.append(MemLabel)

            if(i == highlighter[2] or i == highlighter[3]):
                MemLabel.config(bg='yellow', fg='black')

            j = "0000"+str(i+8)
            if (i > 1):
                j = "0000"+hexArray[i-2]
            MemBlocksLower[i] = Label(MemFrame, text=j, bg="#294040",
                                      fg="#61baba", font="Arial 13 bold",)
            MemBlocksLower[i].place(x=245, y=80+(i*63), anchor="nw")

            MemLabelx = Label(MemFrame, text=UpperMemBlocks[i],
                              height=2, width=11, font="Arial 14 bold",
                              bg="#476b6a", fg="white")
            MemLabelx.place(x=310, y=68+(i*63), anchor="nw")
            
            if(8+i == highlighter[2] or 8+i == highlighter[3]):
                MemLabelx.config(bg='yellow', fg='black')

            Memlabels.append(MemLabelx)


    def nextIR(self, event='NULL'):
        self.stateObj = self.DataObj
        if (type(self.DataObj) == str):
            self.error_screen("Syntax Error")

        if (self.DataObj.priority == 0):
            self.Mtemp1 = [i for i in self.DataObj.memorylist]
            self.Rtemp1 = [i for i in self.DataObj.regList]
            self.DataObj.PCReg = self.MemLabelText[0]

        if (self.DataObj.priority == 1):
            self.current_ins = self.myQ.execute()
            self.DataObj.PCReg = self.MemLabelText[1]
            self.DataObj.IRReg = self.current_ins.upper()

        if (self.DataObj.priority == 2):
            self.myQ.dequeue()
  
            new = processing.Instruction(self.current_ins, self.DataObj)
            x = new.split_string()
            if (type(x) == str):
                self.error_screen(x)

            else:
                self.DataObj = new.working(x)
                if (type(self.DataObj) == str):
                    self.error_screen(self.DataObj)
                else:
                    self.Rtemp2 = [i for i in self.DataObj.regList]
                    self.Mtemp2 = [i for i in self.DataObj.memorylist]
                
                    self.DataObj.memorylist = [i for i in self.Mtemp1]
                    self.DataObj.regList = [i for i in self.Rtemp1]

        if(self.DataObj.priority == 3):
            self.DataObj.highlighter = ['','','','','','']
            self.DataObj.memorylist = [i for i in self.Mtemp2]
            self.DataObj.regList = [i for i in self.Rtemp2]

        if (type(self.DataObj) == str):
            self.error_screen(self.DataObj)
        
        else:
            if(self.DataObj.priority <= 3):
                self.DataObj.priority += 1
            elif not(self.myQ.size == 0):
                self.DataObj.priority = 0

        self.run(self.DataObj.regList, self.DataObj.memorylist,
        self.DataObj.PCReg, self.DataObj.IRReg, self.myQ.array, self.DataObj.priority, self.DataObj.highlighter)

  
    def error_screen(self, x):
        errorLabel = Label(self.root, height=2, width=25,bg='#1f2a2e',
                           fg='red', font="Arial 12 bold", text=x)
        errorLabel.place(x=700, y=60, anchor='nw')
        self.root.after(1500, errorLabel.destroy)
        self.DataObj = self.stateObj
        self.DataObj.priority = 0
        self.current_ins = self.myQ.execute()
        pass



    def run(self, regList, memorylist, PC, IR, memoryblockarray, priority, highlighter):
        self.control_unit(PC, IR, priority)
        self.registers_screen(regList, highlighter)
        self.memory_block(memorylist, highlighter)
        self.memory_queue(memoryblockarray)


data = processing.Data()
mic = Microprocessor(data)
mic.basic_screen()
mic.run(data.regList, data.memorylist, data.PCReg, data.IRReg, mic.myQ.array, data.priority, data.highlighter)
mic.root.mainloop()
