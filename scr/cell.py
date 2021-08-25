NORMAL     = '#FFFFFF'
DEAD       = '#1D1D1D'
CONTAMITED = '#ff5252'
HEALED     = '#71ff61'
CRITICAL   = '#8a0000'
ISOLATED   = '#d1d1d1' 

class Cells:
    def __init__(self, canvas):
        self.cells  = []
        self.canvas = canvas

        self._newinfected = []
        self._newhealed   = []
        self._newcritical = []
        self._newdeath    = []

    #cell state definitons
    def __changeState(self, cell, state):
        self.canvas.itemconfig(cell, fill=state)

    def updateCellsState(self, population):

        print('='*10)

        self._newinfected = list(set(population.infected).difference(self._newinfected))
        self._newhealed   = list(set(population._healed).difference(self._newhealed))
        self._newcritical = list(set(population._critical_stage).difference(self._newcritical))
        self._newdeath    = list(set(population._death).difference(self._newdeath))

        print(f'd intessec h: {set(self._newdeath).intersection(self._newhealed)}')

        for infected in self._newinfected:
            self.__changeState(self.cells[infected[0]][infected[1]], CONTAMITED)

        for healed in self._newhealed:
            self.__changeState(self.cells[healed[0]][healed[1]], HEALED)

        for critical in self._newcritical:
            self.__changeState(self.cells[critical[0]][critical[1]], CRITICAL)

        for death in self._newdeath:
            self.__changeState(self.cells[death[0]][death[1]], DEAD)

        self.canvas.update()
        #print('='*10)
        #print(f'death: {len(self._newdeath)}')
        #print(f'infectados: {len(self._newinfected)}')
        #print(f'healed: {len(self._newhealed)}')
        #print(f'criticos: {len(self._newcritical)}')

    def initializeCells(self, population):
        i = 0
        j = 0


        for group in self.cells:
            for cell in group:
                self.__changeState(cell, NORMAL)                

        for isolated in population._isolated:
            self.__changeState(self.cells[isolated[0]][isolated[1]], ISOLATED)

        self._newinfected = []
        self._newhealed   = []
        self._newcritical = []
        self._newdeath    = []
    
    #draw grid
    def drawPopulation(self, square_size):
        self.canvas.delete('all')

        i = 0

        canvas_sizex = 2*self.canvas.winfo_screenmmwidth()
        canvas_sizey = self.canvas.winfo_screenheight()


        for line in range(0, canvas_sizex+1, square_size):
            self.cells.append([])

            for column in range(0, canvas_sizey+1, square_size):
                self.cells[i].append(self.canvas.create_rectangle(line, column, line+square_size, 
                                                                column + square_size, outline='black', width=1))
            i += 1

        self.canvas.update()