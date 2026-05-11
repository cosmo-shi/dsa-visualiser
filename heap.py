import pygame, sys, heapq

BG        = (0,0,0)
ACCENT    = (180,180,180)
NODE_BG   = (30, 30, 70)
HIGH_COL  = (240, 200, 0)
EDGE_COL  = (60,60,60)
TEXT_COL  = (230,230,230)
BTN_BASE  = (20,20,20)
BTN_HOVER = (45,45,45)
OK_COL    = (60, 200, 100)
ERR_COL   = (220, 60, 60)
BACK_COL  = (220,220,220)
WHITE     = (255,255,255)

NODE_R  = 24
LGAP    = 78


def node_positions(n,cx,ty):
    pos={}; lv=0; i=0
    while i<n:
        cnt=2**lv; y=ty+lv*LGAP; sp=max(38,680//(cnt+1))
        for j in range(cnt):
            if i>=n: break
            pos[i]=(cx-(cnt-1)*sp//2+j*sp, y); i+=1
        lv+=1
    return pos


def draw_heap(sur,fsm,heap,pos,hi):
    ftiny=pygame.font.SysFont("consolas",11)
    for i in range(len(heap)):
        for ch in (2*i+1,2*i+2):
            if ch<len(heap) and i in pos and ch in pos:
                pygame.draw.line(sur,EDGE_COL,pos[i],pos[ch],2)
    for i,v in enumerate(heap):
        if i not in pos: continue
        x,y=pos[i]
        fill  =HIGH_COL if i==hi else NODE_BG
        border=HIGH_COL if i==hi else ACCENT
        pygame.draw.circle(sur,fill,  (x,y),NODE_R)
        pygame.draw.circle(sur,border,(x,y),NODE_R,2)
        l=fsm.render(str(v),True,WHITE)
        sur.blit(l,(x-l.get_width()//2,y-l.get_height()//2))
        idx=ftiny.render(f"[{i}]",True,(150,150,150))
        sur.blit(idx,(x-idx.get_width()//2,y+NODE_R+2))


def draw_btn(sur,fnt,txt,rect,acc):
    bg=BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE
    pygame.draw.rect(sur,bg, rect,border_radius=6)
    pygame.draw.rect(sur,acc,rect,2,border_radius=6)
    l=fnt.render(txt,True,acc)
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

    heap=[]
    for v in [15,40,25,60,10,35]: heapq.heappush(heap,v)

    inp=""; ia=False; msg=""; mc=OK_COL; hi=None
    ir =pygame.Rect(20,50,120,32); ib=pygame.Rect(148,50,110,32)
    eb =pygame.Rect(266,50,140,32); back=pygame.Rect(W//2-80,H-48,160,34)

    running=True
    while running:
        screen.fill(BG)
        t=ftitle.render("Min-Heap Visualiser",True,ACCENT)
        screen.blit(t,(W//2-t.get_width()//2,14))
        screen.blit(fsm.render("Value:",True,(230,230,230)),(20,34))

        draw_inp(screen,fsm,ir,inp,ia,ACCENT)
        draw_btn(screen,fsm,"Insert",     ib,OK_COL)
        draw_btn(screen,fsm,"Extract Min",eb,(210,210,210))

        if msg: screen.blit(fsm.render(msg,True,mc),(20,90))
        arr_s="Array: ["+ ", ".join(str(v) for v in heap)+"]"
        screen.blit(fsm.render(arr_s,True,(150,150,150)),(20,108))
        screen.blit(fsm.render(f"Size: {len(heap)}",True,TEXT_COL),(W-110,50))

        if heap:
            pos=node_positions(len(heap),W//2,180)
            draw_heap(screen,fsm,heap,pos,hi)
            ml=fsm.render(f"Min (root) = {heap[0]}",True,HIGH_COL)
            screen.blit(ml,(W//2-ml.get_width()//2, 128))

        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN: ia=ir.collidepoint(ev.pos)
            if ev.type==pygame.KEYDOWN and ia:
                if ev.key==pygame.K_BACKSPACE: inp=inp[:-1]
                elif ev.key==pygame.K_RETURN:
                    try: v=int(inp.strip()); heapq.heappush(heap,v); hi=heap.index(v); msg=f"Inserted {v}"; mc=OK_COL; inp=""
                    except ValueError: msg="Enter a valid integer"; mc=ERR_COL
                elif (ev.unicode.lstrip("-").isdigit() or ev.unicode=="-") and len(inp)<6: inp+=ev.unicode
            if clicked(ib,ev):
                try: v=int(inp.strip()); heapq.heappush(heap,v); hi=heap.index(v); msg=f"Inserted {v}"; mc=OK_COL; inp=""
                except ValueError: msg="Enter a valid integer"; mc=ERR_COL
            if clicked(eb,ev):
                if heap: v=heapq.heappop(heap); hi=0 if heap else None; msg=f"Extracted min: {v}"; mc=(210,210,210)
                else: msg="Heap is empty!"; mc=ERR_COL
            if clicked(back,ev): running=False
        clock.tick(60)
