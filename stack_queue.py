import pygame
import sys

BG        = (0, 0, 0)
PANEL     = (15,15,15)
S_COL     = (200,200,200)
Q_COL     = (210,210,210)
NODE_BG   = (20,20,20)
TEXT_COL  = (230,230,230)
BTN_BASE  = (20,20,20)
BTN_HOVER = (45,45,45)
OK_COL    = (60, 200, 100)
ERR_COL   = (220, 60, 60)
BACK_COL  = (220,220,220)
WHITE     = (255, 255, 255)

NODE_W  = 130
NODE_H  = 42
GAP     = 8
MAX_VIS = 9


class Stack:
    def __init__(self):      self._data = []
    def push(self, item):    self._data.append(item)
    def pop(self):           return self._data.pop() if self._data else None
    def peek(self):          return self._data[-1]   if self._data else None
    def isEmpty(self):       return len(self._data) == 0
    def size(self):          return len(self._data)
    def to_list(self):       return list(self._data)


class Queue:
    def __init__(self):      self._data = []
    def enqueue(self, v):    self._data.append(v)
    def dequeue(self):       return self._data.pop(0) if self._data else None
    def peek(self):          return self._data[0]     if self._data else None
    def isEmpty(self):       return len(self._data) == 0
    def size(self):          return len(self._data)
    def to_list(self):       return list(self._data)


def draw_btn(sur, fnt, txt, rect, acc):
    bg = BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE
    pygame.draw.rect(sur, bg,  rect, border_radius=6)
    pygame.draw.rect(sur, acc, rect, 2, border_radius=6)
    l = fnt.render(txt, True, acc)
    sur.blit(l, (rect.x+(rect.w-l.get_width())//2, rect.y+(rect.h-l.get_height())//2))


def draw_inp(sur, fnt, rect, txt, active, acc):
    pygame.draw.rect(sur, (8,8,8), rect, border_radius=6)
    pygame.draw.rect(sur, acc if active else (70,70,70), rect, 2, border_radius=6)
    l = fnt.render(txt, True, WHITE)
    sur.blit(l, (rect.x+8, rect.y+(rect.h-l.get_height())//2))


def draw_node(sur, fnt, x, y, val, acc, tag=""):
    r = pygame.Rect(x, y, NODE_W, NODE_H)
    pygame.draw.rect(sur, NODE_BG, r, border_radius=6)
    pygame.draw.rect(sur, acc,     r, 2, border_radius=6)
    l = fnt.render(str(val), True, WHITE)
    sur.blit(l, (x+(NODE_W-l.get_width())//2, y+(NODE_H-l.get_height())//2))
    if tag:
        t = pygame.font.SysFont("consolas",12).render(tag, True, acc)
        sur.blit(t, (x+NODE_W+5, y+(NODE_H-t.get_height())//2))


def clicked(rect, ev):
    return ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and rect.collidepoint(ev.pos)


def run(screen, clock):
    W, H   = screen.get_size()
    ftitle = pygame.font.SysFont("consolas", 26, bold=True)
    fmed   = pygame.font.SysFont("consolas", 15, bold=True)
    fsm    = pygame.font.SysFont("consolas", 13)

    stack = Stack(); queue = Queue()
    for v in ["10","20","30"]:
        stack.push(v); queue.enqueue(v)

    si=""; sa=False; sm=""; sc=OK_COL
    qi=""; qa=False; qm=""; qc=OK_COL

    mid   = W//2
    py    = 95; ph = H-py-58
    sp    = pygame.Rect(14,  py, mid-20, ph)
    qp    = pygame.Rect(mid+8, py, mid-22, ph)

    sx=sp.x+14; sy=py+34
    sir = pygame.Rect(sx, sy, 130, 32)
    spb = pygame.Rect(sx+138, sy, 80, 32)
    sob = pygame.Rect(sx, sy+42, 80, 32)
    skb = pygame.Rect(sx+88, sy+42, 80, 32)

    qx=qp.x+14; qy=py+34
    qir = pygame.Rect(qx, qy, 130, 32)
    qeb = pygame.Rect(qx+138, qy, 90, 32)
    qdb = pygame.Rect(qx, qy+42, 90, 32)
    qkb = pygame.Rect(qx+98, qy+42, 80, 32)

    back = pygame.Rect(W//2-80, H-48, 160, 34)
 
    node_start_y = py + 120   
    node_x_s     = sp.x + 16  
    node_x_q     = qp.x + 16  

    running=True
    while running:
        screen.fill(BG)
        t=ftitle.render("Stack  &  Queue  Visualiser", True, S_COL)
        screen.blit(t,(W//2-t.get_width()//2, 16))

        pygame.draw.rect(screen,PANEL,sp,border_radius=10)
        pygame.draw.rect(screen,S_COL,sp,2,border_radius=10)
        pygame.draw.rect(screen,PANEL,qp,border_radius=10)
        pygame.draw.rect(screen,Q_COL,qp,2,border_radius=10)

        sh=fmed.render("STACK (LIFO)",True,S_COL)
        screen.blit(sh,(sp.x+(sp.w-sh.get_width())//2, py+8))
        qh=fmed.render("QUEUE (FIFO)",True,Q_COL)
        screen.blit(qh,(qp.x+(qp.w-qh.get_width())//2, py+8))

        draw_inp(screen,fsm,sir,si,sa,S_COL)
        draw_btn(screen,fsm,"Push",    spb,S_COL)
        draw_btn(screen,fsm,"Pop",     sob,S_COL)
        draw_btn(screen,fsm,"Peek",    skb,S_COL)
        if sm:
            ml=fsm.render(sm,True,sc)
            screen.blit(ml,(spb.x+spb.w+10, sy+(spb.h-ml.get_height())//2))

        draw_inp(screen,fsm,qir,qi,qa,Q_COL)
        draw_btn(screen,fsm,"Enqueue", qeb,Q_COL)
        draw_btn(screen,fsm,"Dequeue", qdb,Q_COL)
        draw_btn(screen,fsm,"Peek",    qkb,Q_COL)
        if qm:
            ml=fsm.render(qm,True,qc)
            screen.blit(ml,(qeb.x+qeb.w+10, qy+(qeb.h-ml.get_height())//2))

        sl=stack.to_list()
        visible=sl[-MAX_VIS:]  
        visible_rev=list(reversed(visible))  
        for i,v in enumerate(visible_rev):
            ny=node_start_y+i*(NODE_H+GAP)
            if ny+NODE_H > sp.y+sp.h-30: break 
            tag="TOP" if i==0 else ""
            draw_node(screen,fsm,node_x_s,ny,v,S_COL,tag)
            if i>0:
                ax=node_x_s+NODE_W//2
                pygame.draw.line(screen,S_COL,(ax,ny-GAP),(ax,ny),2)
        sz_y=min(node_start_y+len(visible_rev)*(NODE_H+GAP)+4, sp.y+sp.h-20)
        screen.blit(fsm.render(f"Size: {stack.size()}",True,TEXT_COL),(node_x_s,sz_y))

        ql=queue.to_list()
        visible_q=ql[-MAX_VIS:]  
        visible_q_rev=list(reversed(visible_q)) 
        for i,v in enumerate(visible_q_rev):
            ny=node_start_y+i*(NODE_H+GAP)
            if ny+NODE_H > qp.y+qp.h-30: break
            last_idx=len(visible_q_rev)-1
            tag="REAR" if i==0 else ("FRONT" if i==last_idx else "")
            draw_node(screen,fsm,node_x_q,ny,v,Q_COL,tag)
            if i>0:
                ax=node_x_q+NODE_W//2
                pygame.draw.line(screen,Q_COL,(ax,ny-GAP),(ax,ny),2)
        sz_y=min(node_start_y+len(visible_q_rev)*(NODE_H+GAP)+4, qp.y+qp.h-20)
        screen.blit(fsm.render(f"Size: {queue.size()}",True,TEXT_COL),(node_x_q,sz_y))

        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN:
                sa=sir.collidepoint(ev.pos); qa=qir.collidepoint(ev.pos)
            if ev.type==pygame.KEYDOWN:
                if sa:
                    if ev.key==pygame.K_BACKSPACE: si=si[:-1]
                    elif len(si)<8: si+=ev.unicode
                elif qa:
                    if ev.key==pygame.K_BACKSPACE: qi=qi[:-1]
                    elif len(qi)<8: qi+=ev.unicode

            if clicked(spb,ev):
                if si.strip(): stack.push(si.strip()); sm=f"Pushed: {si.strip()}"; sc=OK_COL; si=""
                else: sm="Enter a value"; sc=ERR_COL
            if clicked(sob,ev):
                v=stack.pop()
                if v: sm=f"Popped: {v}"; sc=OK_COL
                else: sm="Stack is empty!"; sc=ERR_COL
            if clicked(skb,ev):
                v=stack.peek()
                sm=(f"Top: {v}" if v else "Stack is empty!")
                sc=(S_COL if v else ERR_COL)
            if clicked(qeb,ev):
                if qi.strip(): queue.enqueue(qi.strip()); qm=f"Enqueued: {qi.strip()}"; qc=OK_COL; qi=""
                else: qm="Enter a value"; qc=ERR_COL
            if clicked(qdb,ev):
                v=queue.dequeue()
                if v: qm=f"Dequeued: {v}"; qc=OK_COL
                else: qm="Queue is empty!"; qc=ERR_COL
            if clicked(qkb,ev):
                v=queue.peek()
                qm=(f"Front: {v}" if v else "Queue is empty!")
                qc=(Q_COL if v else ERR_COL)
            if clicked(back,ev): running=False
        clock.tick(60)
