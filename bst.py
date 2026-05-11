import pygame
import sys

BG        = (0, 0, 0)
ACCENT    = (200,200,200)
NODE_BG   = (30, 30, 70)
HIGH_BG   = (240, 200, 0)
EDGE_COL  = (160,160,160)
TEXT_COL  = (230,230,230)
BTN_BASE  = (20,20,20)
BTN_HOVER = (45,45,45)
OK_COL    = (60, 200, 100)
ERR_COL   = (220, 60, 60)
TRAV_COL  = (180,180,180)
BACK_COL  = (220,220,220)
WHITE     = (255, 255, 255)

NODE_R    = 22
LGAP      = 70

class BSTNode:
    def __init__(self, v): self.value=v; self.left=None; self.right=None


class BST:
    def __init__(self): self.root=None

    def insert(self, v):   self.root=self._ins(self.root,v)
    def _ins(self,n,v):
        if n is None: return BSTNode(v)
        if v<n.value: n.left =self._ins(n.left, v)
        elif v>n.value: n.right=self._ins(n.right,v)
        return n

    def search(self,v):    return self._srch(self.root,v)
    def _srch(self,n,v):
        if n is None or n.value==v: return n
        return self._srch(n.left,v) if v<n.value else self._srch(n.right,v)

    def delete(self,v):    self.root=self._del(self.root,v)
    def _del(self,n,v):
        if n is None: return n
        if   v<n.value: n.left =self._del(n.left, v)
        elif v>n.value: n.right=self._del(n.right,v)
        else:
            if n.left  is None: return n.right
            if n.right is None: return n.left
            m=n.right
            while m.left: m=m.left
            n.value=m.value; n.right=self._del(n.right,m.value)
        return n

    def inorder(self):
        r=[]; self._in(self.root,r); return r
    def _in(self,n,r):
        if n: self._in(n.left,r); r.append(n.value); self._in(n.right,r)

    def preorder(self):
        r=[]; self._pre(self.root,r); return r
    def _pre(self,n,r):
        if n: r.append(n.value); self._pre(n.left,r); self._pre(n.right,r)

    def postorder(self):
        r=[]; self._post(self.root,r); return r
    def _post(self,n,r):
        if n: self._post(n.left,r); self._post(n.right,r); r.append(n.value)


def compute_pos(n,x,y,xoff,pos):
    if n is None: return
    pos[n]=(x,y)
    compute_pos(n.left, x-xoff,y+LGAP,max(xoff//2,26),pos)
    compute_pos(n.right,x+xoff,y+LGAP,max(xoff//2,26),pos)


def draw_tree(sur,fnt,n,pos,hv):
    if n is None: return
    x,y=pos[n]
    for ch in (n.left,n.right):
        if ch and ch in pos:
            cx,cy=pos[ch]; pygame.draw.line(sur,EDGE_COL,(x,y),(cx,cy),2)
    draw_tree(sur,fnt,n.left, pos,hv)
    draw_tree(sur,fnt,n.right,pos,hv)
    fill  =HIGH_BG if n.value==hv else NODE_BG
    border=HIGH_BG if n.value==hv else ACCENT
    pygame.draw.circle(sur,fill,  (x,y),NODE_R)
    pygame.draw.circle(sur,border,(x,y),NODE_R,2)
    l=fnt.render(str(n.value),True,WHITE)
    sur.blit(l,(x-l.get_width()//2,y-l.get_height()//2))


def draw_btn(sur,fnt,txt,rect,acc,active=False):
    bg=(50,0,80) if active else (BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE)
    pygame.draw.rect(sur,bg,  rect,border_radius=6)
    pygame.draw.rect(sur,acc, rect,2,border_radius=6)
    l=fnt.render(txt,True,WHITE if active else acc)
    sur.blit(l,(rect.x+(rect.w-l.get_width())//2,rect.y+(rect.h-l.get_height())//2))


def draw_inp(sur,fnt,rect,txt,active,acc):
    pygame.draw.rect(sur,(8,8,8),rect,border_radius=6)
    pygame.draw.rect(sur,acc if active else (70,70,70),rect,2,border_radius=6)
    l=fnt.render(txt,True,WHITE)
    sur.blit(l,(rect.x+8,rect.y+(rect.h-l.get_height())//2))


def clicked(rect,ev):
    return ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and rect.collidepoint(ev.pos)


def run(screen, clock):
    W,H=screen.get_size()
    ftitle=pygame.font.SysFont("consolas",26,bold=True)
    fsm   =pygame.font.SysFont("consolas",13)

    bst=BST()
    for v in [50,30,70,20,40,60,80]: bst.insert(v)

    ii=""; di=""; si=""
    ia=False; da=False; sa=False
    msg=""; mc=OK_COL; hv=None; tm=None; ts=""

    # Each row: label at row_y, then input+button 16px below
    row1=52;  row2=106; row3=160
    cy1=row1+16; cy2=row2+16; cy3=row3+16

    ir =pygame.Rect(20, cy1, 85,30); ib=pygame.Rect(112,cy1, 75,30)
    dr =pygame.Rect(20, cy2, 85,30); db=pygame.Rect(112,cy2, 75,30)
    sr =pygame.Rect(20, cy3, 85,30); sb=pygame.Rect(112,cy3, 75,30)
    inb=pygame.Rect(210,cy1, 105,30)
    prb=pygame.Rect(210,cy2, 105,30)
    pob=pygame.Rect(210,cy3, 105,30)
    back=pygame.Rect(W//2-80,H-48,160,34)

    LBLS=[(20,row1,"Insert:"),(20,row2,"Delete:"),(20,row3,"Search:"),(210,row1,"Traversals:")]
    tcx=W//2; ty0=285

    running=True
    while running:
        screen.fill(BG)
        t=ftitle.render("Binary Search Tree Visualiser",True,ACCENT)
        screen.blit(t,(W//2-t.get_width()//2,14))
        for lx,ly,lt in LBLS:
            screen.blit(fsm.render(lt,True,TEXT_COL),(lx,ly))

        draw_inp(screen,fsm,ir,ii,ia,ACCENT)
        draw_btn(screen,fsm,"Insert",ib,ACCENT)
        draw_inp(screen,fsm,dr,di,da,ERR_COL)
        draw_btn(screen,fsm,"Delete",db,ERR_COL)
        draw_inp(screen,fsm,sr,si,sa,HIGH_BG)
        draw_btn(screen,fsm,"Search",sb,HIGH_BG)
        draw_btn(screen,fsm,"In-order",  inb,TRAV_COL,tm=="in")
        draw_btn(screen,fsm,"Pre-order", prb,TRAV_COL,tm=="pre")
        draw_btn(screen,fsm,"Post-order",pob,TRAV_COL,tm=="post")

        if msg: screen.blit(fsm.render(msg,True,mc),(20,cy3+40))
        if ts:
            # Wrap traversal string if too wide
            full = f"{tm}-order: {ts}"
            max_w = W - 40
            if fsm.size(full)[0] <= max_w:
                screen.blit(fsm.render(full, True, TRAV_COL), (20, cy3+58))
            else:
                # Split at midpoint word boundary
                words = full.split(" → ")
                line1 = ""; line2 = ""
                for w in words:
                    test = line1 + (" → " if line1 else "") + w
                    if fsm.size(test)[0] <= max_w:
                        line1 = test
                    else:
                        line2 += (" → " if line2 else "") + w
                screen.blit(fsm.render(line1, True, TRAV_COL), (20, cy3+58))
                screen.blit(fsm.render(line2, True, TRAV_COL), (20, cy3+76))

        if bst.root:
            pos={}; compute_pos(bst.root,tcx,ty0,185,pos)
            draw_tree(screen,fsm,bst.root,pos,hv)

        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN:
                ia=ir.collidepoint(ev.pos); da=dr.collidepoint(ev.pos); sa=sr.collidepoint(ev.pos)
            if ev.type==pygame.KEYDOWN:
                if ia:
                    if ev.key==pygame.K_BACKSPACE: ii=ii[:-1]
                    elif (ev.unicode.lstrip("-").isdigit() or ev.unicode=="-") and len(ii)<6: ii+=ev.unicode
                elif da:
                    if ev.key==pygame.K_BACKSPACE: di=di[:-1]
                    elif (ev.unicode.lstrip("-").isdigit() or ev.unicode=="-") and len(di)<6: di+=ev.unicode
                elif sa:
                    if ev.key==pygame.K_BACKSPACE: si=si[:-1]
                    elif (ev.unicode.lstrip("-").isdigit() or ev.unicode=="-") and len(si)<6: si+=ev.unicode

            if clicked(ib,ev):
                hv=None; ts=""
                try:
                    v=int(ii.strip()); bst.insert(v); msg=f"Inserted {v}"; mc=OK_COL; ii=""
                except ValueError: msg="Enter a valid integer"; mc=ERR_COL
            if clicked(db,ev):
                hv=None; ts=""
                try:
                    v=int(di.strip())
                    if bst.search(v): bst.delete(v); msg=f"Deleted {v}"; mc=OK_COL
                    else: msg=f"{v} not found"; mc=ERR_COL
                    di=""
                except ValueError: msg="Enter a valid integer"; mc=ERR_COL
            if clicked(sb,ev):
                ts=""
                try:
                    v=int(si.strip()); f=bst.search(v)
                    if f: hv=v; msg=f"Found {v}"; mc=OK_COL
                    else: hv=None; msg=f"{v} not found"; mc=ERR_COL
                    si=""
                except ValueError: msg="Enter a valid integer"; mc=ERR_COL
            if clicked(inb,ev):  hv=None; tm="in";   ts=" → ".join(str(v) for v in bst.inorder())
            if clicked(prb,ev):  hv=None; tm="pre";  ts=" → ".join(str(v) for v in bst.preorder())
            if clicked(pob,ev):  hv=None; tm="post"; ts=" → ".join(str(v) for v in bst.postorder())
            if clicked(back,ev): running=False
        clock.tick(60)
