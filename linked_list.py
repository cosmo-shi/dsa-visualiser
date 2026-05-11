import pygame
import sys

BG        = (0, 0, 0)
ACCENT    = (200,200,200)
NODE_BG   = (30, 30, 70)
HIGH_BG   = (240, 200, 0)
HIGH_BOR  = (255, 180, 0)
ARR_COL   = (220,220,220)
TEXT_COL  = (230,230,230)
BTN_BASE  = (20,20,20)
BTN_HOVER = (45,45,45)
OK_COL    = (60, 200, 100)
ERR_COL   = (160,160,160)
REV_COL   = (180, 80, 255)
BACK_COL  = (220,220,220)
WHITE     = (255, 255, 255)

NODE_W      = 80
NODE_H      = 44
HGAP        = 28
RGAP        = 80
MAX_ROW     = 9
SX          = 40
SY          = 260


class Node:
    def __init__(self, data):
        self.data = data; self.next = None


class LinkedList:
    def __init__(self): self.head = None

    def insert_at_index(self, data, index):
        n = Node(data)
        if index == 0:
            n.next = self.head; self.head = n; return True
        cur = self.head; prev = None; cnt = 0
        while cur and cnt < index:
            prev = cur; cur = cur.next; cnt += 1
        if cnt == index:
            prev.next = n; n.next = cur; return True
        return False

    def delete_value(self, val):
        cur = self.head; prev = None
        while cur:
            if str(cur.data) == str(val):
                if prev: prev.next = cur.next
                else:    self.head = cur.next
                return True
            prev = cur; cur = cur.next
        return False

    def search(self, val):
        cur = self.head; i = 0
        while cur:
            if str(cur.data) == str(val): return i
            cur = cur.next; i += 1
        return -1

    def reverse(self):
        prev = None; cur = self.head
        while cur:
            nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
        self.head = prev

    def to_list(self):
        r=[]; cur=self.head
        while cur: r.append(cur.data); cur=cur.next
        return r

    def size(self): return len(self.to_list())


# Helpers 
def draw_btn(sur, fnt, txt, rect, acc):
    bg = BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE
    pygame.draw.rect(sur, bg,  rect, border_radius=6)
    pygame.draw.rect(sur, acc, rect, 2, border_radius=6)
    l = fnt.render(txt, True, acc)
    sur.blit(l,(rect.x+(rect.w-l.get_width())//2, rect.y+(rect.h-l.get_height())//2))


def draw_inp(sur, fnt, rect, txt, active, acc):
    pygame.draw.rect(sur,(8,8,8),rect,border_radius=6)
    pygame.draw.rect(sur,acc if active else (70,70,70),rect,2,border_radius=6)
    l=fnt.render(txt,True,WHITE)
    sur.blit(l,(rect.x+8,rect.y+(rect.h-l.get_height())//2))


def clicked(rect, ev):
    return ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and rect.collidepoint(ev.pos)


def arrow_right(sur, x1, y, x2, col):
    pygame.draw.line(sur, col,(x1,y),(x2,y),2)
    pygame.draw.polygon(sur,col,[(x2,y),(x2-8,y-4),(x2-8,y+4)])


def get_xy(idx):
    r=idx//MAX_ROW; c=idx%MAX_ROW
    return SX+c*(NODE_W+HGAP), SY+r*(NODE_H+RGAP)


def run(screen, clock):
    W,H=screen.get_size()
    ftitle=pygame.font.SysFont("consolas",26,bold=True)
    fsm   =pygame.font.SysFont("consolas",13)

    ll=LinkedList()
    for v in [10,20,30,40,50]: ll.insert_at_index(v,ll.size())

    vi=""; xi=""; di=""; si=""
    va=False; xa=False; da=False; sa=False
    hi=-1; msg=""; mc=OK_COL
    
    row1=46;  row2=96;  row3=146
    iy1=row1+16; iy2=row2+16; iy3=row3+16

    vr=pygame.Rect(20,  iy1, 95,30); xr=pygame.Rect(122,iy1, 60,30)
    ib=pygame.Rect(188, iy1, 80,30)
    dr=pygame.Rect(20,  iy2, 95,30); db=pygame.Rect(122,iy2, 80,30)
    sr=pygame.Rect(20,  iy3, 95,30); sb=pygame.Rect(122,iy3, 80,30)
    rb=pygame.Rect(210, iy3, 85,30)
    back=pygame.Rect(W//2-80,H-48,160,34)

    LBLS=[(20,row1,"Value:"),(122,row1,"Idx:"),(20,row2,"Delete:"),(20,row3,"Search:")]

    running=True
    while running:
        screen.fill(BG)
        t=ftitle.render("Linked List Visualiser",True,ACCENT)
        screen.blit(t,(W//2-t.get_width()//2,14))
        for lx,ly,lt in LBLS:
            screen.blit(fsm.render(lt,True,TEXT_COL),(lx,ly))

        draw_inp(screen,fsm,vr,vi,va,ACCENT); draw_inp(screen,fsm,xr,xi,xa,ACCENT)
        draw_btn(screen,fsm,"Insert", ib,ACCENT)
        draw_inp(screen,fsm,dr,di,da,ERR_COL)
        draw_btn(screen,fsm,"Delete", db,ERR_COL)
        draw_inp(screen,fsm,sr,si,sa,HIGH_BOR)
        draw_btn(screen,fsm,"Search", sb,HIGH_BOR)
        draw_btn(screen,fsm,"Reverse",rb,REV_COL)
        if msg:
            ml=fsm.render(msg,True,mc)
            screen.blit(ml,(ib.x+ib.w+10, iy1+(ib.h-ml.get_height())//2))
        screen.blit(fsm.render(f"Size: {ll.size()}",True,TEXT_COL),(W-110,row1))

        items=ll.to_list()
        for i,val in enumerate(items):
            x,y=get_xy(i)
            fill  =HIGH_BG  if i==hi else NODE_BG
            border=HIGH_BOR if i==hi else ACCENT
            pygame.draw.rect(screen,fill,  pygame.Rect(x,y,NODE_W,NODE_H),border_radius=6)
            pygame.draw.rect(screen,border,pygame.Rect(x,y,NODE_W,NODE_H),2,border_radius=6)
            l=fsm.render(str(val),True,WHITE)
            screen.blit(l,(x+(NODE_W-l.get_width())//2, y+(NODE_H-l.get_height())//2))
            if i==0:
                hl=fsm.render("HEAD",True,ACCENT); screen.blit(hl,(x,y-16))
            if i<len(items)-1:
                nx,ny=get_xy(i+1)
                if i//MAX_ROW==(i+1)//MAX_ROW:
                    arrow_right(screen,x+NODE_W,y+NODE_H//2,nx,ARR_COL)
                else:
                    my2=y+NODE_H+RGAP//2
                    pygame.draw.line(screen,ARR_COL,(x+NODE_W//2,y+NODE_H),(x+NODE_W//2,my2),2)
                    pygame.draw.line(screen,ARR_COL,(x+NODE_W//2,my2),(SX-10,my2),2)
                    pygame.draw.line(screen,ARR_COL,(SX-10,my2),(SX-10,ny+NODE_H//2),2)
                    arrow_right(screen,SX-10,ny+NODE_H//2,nx,ARR_COL)
        if items:
            lx2,ly2=get_xy(len(items)-1)
            if (len(items)-1)%MAX_ROW < MAX_ROW-1:
                arrow_right(screen,lx2+NODE_W,ly2+NODE_H//2,lx2+NODE_W+HGAP+4,ARR_COL)
                nl=fsm.render("NULL",True,(120,120,120))
                screen.blit(nl,(lx2+NODE_W+HGAP+6,ly2+(NODE_H-nl.get_height())//2))

        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN:
                va=vr.collidepoint(ev.pos); xa=xr.collidepoint(ev.pos)
                da=dr.collidepoint(ev.pos); sa=sr.collidepoint(ev.pos)
            if ev.type==pygame.KEYDOWN:
                if va:
                    if ev.key==pygame.K_BACKSPACE: vi=vi[:-1]
                    elif len(vi)<8: vi+=ev.unicode
                elif xa:
                    if ev.key==pygame.K_BACKSPACE: xi=xi[:-1]
                    elif ev.unicode.isdigit() and len(xi)<3: xi+=ev.unicode
                elif da:
                    if ev.key==pygame.K_BACKSPACE: di=di[:-1]
                    elif len(di)<8: di+=ev.unicode
                elif sa:
                    if ev.key==pygame.K_BACKSPACE: si=si[:-1]
                    elif len(si)<8: si+=ev.unicode

            if clicked(ib,ev):
                hi=-1
                if vi.strip() and xi.strip():
                    ok=ll.insert_at_index(vi.strip(),int(xi.strip()))
                    if ok: msg=f"Inserted '{vi.strip()}' at {xi.strip()}"; mc=OK_COL; vi=""; xi=""
                    else:  msg="Index out of range"; mc=ERR_COL
                else: msg="Enter value and index"; mc=ERR_COL
            if clicked(db,ev):
                hi=-1
                if di.strip():
                    ok=ll.delete_value(di.strip())
                    msg=(f"Deleted '{di.strip()}'" if ok else f"'{di.strip()}' not found")
                    mc=OK_COL if ok else ERR_COL; di=""
                else: msg="Enter a value to delete"; mc=ERR_COL
            if clicked(sb,ev):
                if si.strip():
                    idx=ll.search(si.strip())
                    if idx>=0: hi=idx; msg=f"Found '{si.strip()}' at index {idx}"; mc=HIGH_BOR
                    else:      hi=-1;  msg=f"'{si.strip()}' not found"; mc=ERR_COL
                    si=""
                else: msg="Enter a value to search"; mc=ERR_COL
            if clicked(rb,ev):
                ll.reverse(); hi=-1; msg="List reversed!"; mc=REV_COL
            if clicked(back,ev): running=False
        clock.tick(60)
