import pygame, sys, math, time
from typing import List, Dict, Tuple, Generator

BG        = (0,0,0)
ACCENT    = (180,180,180)
NODE_DEF  = (30, 30, 70)
NODE_VIS  = (220, 140, 0)
NODE_STA  = (0, 180, 80)
NODE_CUR  = (0, 160, 255)
EDGE_DEF  = (70,70,70)
EDGE_VIS  = (220, 140, 0)
TEXT_COL  = (230,230,230)
BTN_BASE  = (20,20,20)
BTN_HOVER = (45,45,45)
BACK_COL  = (220,220,220)
WHITE     = (255,255,255)

NODE_R  = 24
STEP_DL = 0.55

class Stack:
    def __init__(self):      self._data: List[int] = []
    def push(self, item):    self._data.append(item)
    def pop(self):           return self._data.pop()
    def peek(self):          return self._data[-1]
    def isEmpty(self):       return len(self._data) == 0

class Queue:
    def __init__(self):      self._data: List[int] = []
    def insert(self, item):  self._data.append(item)
    def remove(self):        return self._data.pop(0)
    def isEmpty(self):       return len(self._data) == 0

class Graph:
    def __init__(self, directed=False):
        self._vertices: List[str] = []
        self._adjMat: Dict[Tuple[int,int], int] = {}
        self.directed = directed

    def addVertex(self, vertex: str):
        if vertex not in self._vertices:
            self._vertices.append(vertex)

    def nVertices(self) -> int:
        return len(self._vertices)

    def getVertex(self, n: int) -> str:
        return self._vertices[n] if 0 <= n < self.nVertices() else "?"

    def getIndex(self, vertex: str) -> int:
        return self._vertices.index(vertex)

    def addEdge(self, A: str, B: str):
        i, j = self.getIndex(A), self.getIndex(B)
        if i == j: return
        self._adjMat[(i, j)] = 1
        if not self.directed:
            self._adjMat[(j, i)] = 1

    def hasEdge(self, i: int, j: int) -> bool:
        return bool(self._adjMat.get((i, j), False))

    def adjacentVertices(self, n: int) -> Generator[int, None, None]:
        for j in range(self.nVertices()):
            if j != n and self.hasEdge(n, j):
                yield j

    def adjacentUnvisitedVertices(self, n: int, visited: List[bool]) -> Generator[int, None, None]:
        for j in self.adjacentVertices(n):
            if not visited[j]:
                visited[j] = True
                yield j

    def bfs_steps(self, start: str):
        start_idx = self.getIndex(start)
        visited   = [False] * self.nVertices()
        queue     = Queue()
        queue.insert(start_idx)
        visited[start_idx] = True
        order = []

        while not queue.isEmpty():
            v = queue.remove()
            order.append(self.getVertex(v))
            yield self.getVertex(v), None, self._vis_set(visited), list(order)

            for adj in self.adjacentUnvisitedVertices(v, visited):
                queue.insert(adj)
                yield self.getVertex(v), self.getVertex(adj), self._vis_set(visited), list(order)

    def dfs_steps(self, start: str):
        start_idx = self.getIndex(start)
        visited   = [False] * self.nVertices()
        stack     = Stack()
        stack.push(start_idx)
        visited[start_idx] = True
        order = []

        while not stack.isEmpty():
            v = stack.pop()
            order.append(self.getVertex(v))
            yield self.getVertex(v), None, self._vis_set(visited), list(order)

            neighbours = sorted(self.adjacentVertices(v), reverse=True)
            for adj in neighbours:
                if not visited[adj]:
                    stack.push(adj)
                    visited[adj] = True
                    yield self.getVertex(v), self.getVertex(adj), self._vis_set(visited), list(order)

    def _vis_set(self, visited: List[bool]) -> set:
        return {self.getVertex(i) for i, v in enumerate(visited) if v}


# Build default graph
def build_graph(directed):
    g = Graph(directed=directed)
    for v in ["A","B","C","D","E","F","G"]:
        g.addVertex(v)
    for e in [("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G"),("D","E")]:
        g.addEdge(*e)
    return g


# Drawing helpers
def circle_layout(vertices, cx, cy, r):
    pos = {}
    n   = len(vertices)
    for i, v in enumerate(vertices):
        a      = math.radians(360 / n * i - 90)
        pos[v] = (int(cx + r * math.cos(a)), int(cy + r * math.sin(a)))
    return pos


def draw_edge(sur, x1, y1, x2, y2, col, directed):
    pygame.draw.line(sur, col, (x1,y1), (x2,y2), 2)
    if directed:
        a  = math.atan2(y2-y1, x2-x1)
        ux = math.cos(a); uy = math.sin(a)
        ex = int(x2 - ux*NODE_R); ey = int(y2 - uy*NODE_R)
        for da in (0.4, -0.4):
            pygame.draw.line(sur, col, (ex,ey),
                (int(ex - 12*math.cos(a-da)), int(ey - 12*math.sin(a-da))), 2)


def draw_btn(sur, fnt, txt, rect, acc, active=False):
    bg = (20,20,20) if active else (BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE)
    pygame.draw.rect(sur, bg,  rect, border_radius=6)
    pygame.draw.rect(sur, acc, rect, 2, border_radius=6)
    l = fnt.render(txt, True, WHITE if active else acc)
    sur.blit(l, (rect.x+(rect.w-l.get_width())//2, rect.y+(rect.h-l.get_height())//2))


def clicked(rect, ev):
    return ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and rect.collidepoint(ev.pos)


def run(screen, clock):
    W, H   = screen.get_size()
    ftitle = pygame.font.SysFont("consolas", 26, bold=True)
    fmed   = pygame.font.SysFont("consolas", 15, bold=True)
    fsm    = pygame.font.SysFont("consolas", 13)

    g    = build_graph(directed=False)
    npos = circle_layout(g._vertices, W//2, H//2+30, 200)

    sv    = "A"
    vis   = set()
    vedges= []
    cur   = None
    steps = []
    si    = 0
    anim  = False
    last  = 0
    ostr  = ""

    bfsb = pygame.Rect(20, 50,100,30)
    dfsb = pygame.Rect(128,50,100,30)
    rstb = pygame.Rect(236,50,90, 30)
    dirb = pygame.Rect(334,50,160,30)
    back = pygame.Rect(W//2-80, H-48, 160, 34)

    def reset():
        nonlocal vis, vedges, cur, steps, si, anim, ostr
        vis=set(); vedges=[]; cur=None; steps=[]; si=0; anim=False; ostr=""

    def start_trav(method):
        nonlocal steps, si, anim, last
        reset()
        steps = list(g.bfs_steps(sv) if method=="BFS" else g.dfs_steps(sv))
        si=0; anim=True; last=time.time()

    running = True
    while running:
        now = time.time()
        screen.fill(BG)

        t = ftitle.render("Graph Traversal Visualiser", True, ACCENT)
        screen.blit(t, (W//2 - t.get_width()//2, 14))

        draw_btn(screen, fsm, "▶ BFS", bfsb, (200,200,200))
        draw_btn(screen, fsm, "▶ DFS", dfsb, (200,200,200))
        draw_btn(screen, fsm, "Reset", rstb, (160,160,160))
        draw_btn(screen, fsm, "Directed: ON" if g.directed else "Directed: OFF",
                 dirb, ACCENT, g.directed)

        screen.blit(fsm.render(f"Click node to set start.  Start: {sv}", True, TEXT_COL), (20,88))
        if ostr:
            screen.blit(fsm.render("Order: " + ostr, True, (240,240,240)), (20,106))

        # Draw edges
        drawn = set()
        for v in g._vertices:
            vi = g.getIndex(v)
            for j in range(g.nVertices()):
                if not g.hasEdge(vi, j): continue
                key = (vi,j) if g.directed else (min(vi,j), max(vi,j))
                if key in drawn: continue
                drawn.add(key)
                nb    = g.getVertex(j)
                x1,y1 = npos[v]; x2,y2 = npos[nb]
                col   = EDGE_VIS if (v,nb) in vedges or (nb,v) in vedges else EDGE_DEF
                draw_edge(screen, x1,y1, x2,y2, col, g.directed)

        # Draw nodes
        for v in g._vertices:
            x,y  = npos[v]
            fill = NODE_STA if v==sv else (NODE_CUR if v==cur else (NODE_VIS if v in vis else NODE_DEF))
            pygame.draw.circle(screen, fill,   (x,y), NODE_R)
            pygame.draw.circle(screen, ACCENT, (x,y), NODE_R, 2)
            l = fmed.render(v, True, WHITE)
            screen.blit(l, (x-l.get_width()//2, y-l.get_height()//2))

        draw_btn(screen, fsm, "◀  Back to Menu", back, BACK_COL)
        pygame.display.flip()

        # Animation tick
        if anim and si < len(steps):
            if now - last >= STEP_DL:
                last = now
                c, edge, v2, order = steps[si]
                cur  = c
                vis  = v2
                if edge: vedges.append((c, edge))
                ostr = " → ".join(order)
                si  += 1
        elif anim:
            anim = False; cur = None

        # Events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for v in g._vertices:
                    x,y = npos[v]
                    if math.hypot(ev.pos[0]-x, ev.pos[1]-y) <= NODE_R:
                        sv=v; reset(); break
            if clicked(bfsb, ev): start_trav("BFS")
            if clicked(dfsb, ev): start_trav("DFS")
            if clicked(rstb, ev): reset()
            if clicked(dirb, ev):
                reset()
                g    = build_graph(directed=not g.directed)
                npos = circle_layout(g._vertices, W//2, H//2+30, 200)
            if clicked(back, ev): running = False

        clock.tick(60)
