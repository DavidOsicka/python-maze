import heapq

class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.distance = 0
        self.estimation = 0


class AStarAlg(object):

    def __init__(self, maze):
        self._opened = []
        self._closed = set()
        self._cells = []
        self._maze = maze
        heapq.heapify(self._opened)

    def init_cells(self):
        line = []
        cols, rows = self._maze.getSize()
        for x in range(rows):
            for y in range(cols):
                line.append(Cell(x, y))
            self._cells.append(line)
            line = []
        self._start = self._cells [self._maze.getStart()[0]] [self._maze.getStart()[1]]
        self._end = self._cells [self._maze.getEnd()[0]] [self._maze.getEnd()[1]]

    def compute_estimated_distance(self, cell):
        return (abs(cell.x - self._end.x) + abs(cell.y - self._end.x))

    def get_adjacent_cells(self, cell):
        adj_cells = []
        cols, rows = self._maze.getSize()
        if cell.x < rows-1:
            adj_cells.append(self._cells[cell.x+1][cell.y])
        if cell.x > 0:
            adj_cells.append(self._cells[cell.x-1][cell.y])
        if cell.y < cols-1:
            adj_cells.append(self._cells[cell.x][cell.y+1])
        if cell.y > 0:
            adj_cells.append(self._cells[cell.x][cell.y-1])
        return adj_cells

    def get_path(self):
        if self._end.parent == None:
            return []
        path = []
        cell = self._end
        while cell is not self._start:
            path = [(cell.x, cell.y)] + path
            cell = cell.parent
        path = [(self._start.x, self._start.y)] + path
        return path

    def update_cell(self, adj, cell):
        adj.distance = cell.distance + 1
        adj.estimation = self.compute_estimated_distance(adj)
        adj.parent = cell

    def compute(self):
        self.init_cells()
        self.compute_estimated_distance(self._start)
        cellIndexToHeap = 0

        heapq.heappush(self._opened, (self._start.distance + self._start.estimation, cellIndexToHeap, self._start))
        cellIndexToHeap += 1

        while len(self._opened):
            n, i, cell = heapq.heappop(self._opened)
            self._closed.add(cell)
            if cell is self._end:
                return
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if self._maze.isFree(adj_cell.x, adj_cell.y) and adj_cell not in self._closed:
                    if (adj_cell.distance + adj_cell.estimation, adj_cell) in self._opened:
                        if adj_cell.distance > cell.distance + 1:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self._opened, (adj_cell.distance + adj_cell.estimation, cellIndexToHeap, adj_cell))
                        cellIndexToHeap += 1