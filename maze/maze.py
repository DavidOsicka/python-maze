# coding: utf-8 

# Vzhledem k tomu, že nebylo nikde specifikované indexování políček v bludišti, ze kterého rohu začít,
# zvolil sem si, že levý horní roh má souřadnice (0,0) a dále zvyšuji o 1 v obou směrech.
# Souřadnice buňky si uchovávám ve formátu (řádek, sloupec)
# Metoda getSize() má podle testů vracet velikost bludiště ve tvaru (šířka, výška), proto tyhle hodnoty v metodě prohazuji.
# Přijde mi lepší prohodit až hodnoty, které vracím, než abych si například uchovával invertovanou matici pro bludiště,
# to mi přijde nepřehledné pro psaní i debugování kódu. Doufám tedy, že kvůli tomu nebude problém s rozšířenými neoficiálními testy.
# Metoda isFree má v komentáři uvedeno: "Vrátí False jestli je na pozici x,y chodba..." to mi přijde divné a předpokládám,
# že je chyba v komentáři, neboť logicky isFree znamená, že je políčko volné a můžeme na něj jít, tedy pokud je tam chodba vrací True.
# Opět tedy doufám, že nebude problém u rozsáhlejších testů

import numpy
from maze.exceptions import MazeError
from maze.maze_solver import AStarAlg

class MazeGame(object):

    def __init__(self, data, start, end):
        """Inicializuje bludiste
        data je 2D matice , 
        start je pozice zacatku, napr [1,1]
        stop je pozice konce cile. napr. [10,10].

        Pokud start nebo stop je mimo bludiste, vyvola vyjimku
        """
        assert data.dtype == bool
        self._data = data

        width = data.shape[1]
        height = data.shape[0]
        if start[0] < 0 or start[0] > height or start[1] < 0 or start[1] > width:
            raise MazeError("Start is out of maze")
        if end[0] < 0 or end[0] > height or end[1] < 0 or end[1] > width:
            raise MazeError("End is out of maze")

        self._start = start
        self._end = end

    def getSize(self):
        "Vrati velikost bludiste"
        height, width = self._data.shape
        return (width, height)

    def getStart(self):
        return self._start

    def getEnd(self):
        return self._end

    def isFree(self, x, y):
        "Vrátí False jestli na pozici x,y chodba. Jinak vrací True"
        if x < 0 or y < 0 or x > self._data.shape[0] or y > self._data.shape[1]:
            return False
        return self._data[x][y]

    def getSolution(self):
        "Vrati nejake nejkratsi reseni bludiste nebo vyvola vyjimku"
        alg = AStarAlg(self)
        alg.compute()
        path = alg.get_path()
        if path == []:
            raise MazeError("There is no solution")
        return MazePath(path)

    @staticmethod 
    def fromString(data):
        """
        Postavi bludiste z retezce. 
        Prazdne radky se ignoruji, 
        X nebo # je zed,  B je zacatek a E je konec.
        """
        start = (-1,-1)
        end = (-1,-1)
        row = 0
        column = 0
        maze = []
        mazeLine = []
        isLineEmpty = True

        listOfLines = str(data).splitlines();

        for line in listOfLines:
            for char in line:
                if char == 'B':
                    if start != (-1, -1):
                        raise MazeError("There is more than one start")
                    start = (row, column)
                    mazeLine.append(True)
                    isLineEmpty = False
                elif char == 'E':
                    if end != (-1, -1):
                        raise MazeError("There is more than one end")
                    end = (row, column)
                    mazeLine.append(True)
                    isLineEmpty = False
                elif (char == 'X') or (char == '#'):
                    mazeLine.append(False)
                    isLineEmpty = False
                elif char == " ":
                    mazeLine.append(True)
                    isLineEmpty = False
                column += 1

            if not isLineEmpty:
                maze.append(mazeLine)
                row += 1

            isLineEmpty = True
            mazeLine = []
            column = 0

        if start == (-1,-1):
            raise MazeError("There is no start")
        if end == (-1,-1):
            raise MazeError("There is no end")
        finalMaze = numpy.array(maze)
        return MazeGame(finalMaze, start, end)


class MazePath(object):
    "Objekt obsahujici cestu v bludisti"

    def __init__(self, steps):
        "Inicializuje objekt MazePath"
        self._step = 0
        self._steps = steps

    def length(self):
        "Vraci delku cesty v bludisti"
        return len(self._steps)

    def __iter__(self):
        "Iterator vracejici jednotlive body cesty"
        for step in self._steps:
            yield step