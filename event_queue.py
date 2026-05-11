import pygame, sys, heapq

BG       = (0,0,0)
ACCENT   = (210,210,210)
NODE_BG  = (30, 30, 70)
HIGH_COL = (240, 200, 0)
EDGE_COL = (70,70,70)
LOG_BG   = (8,8,8)
TEXT_COL = (230,230,230)
BTN_BASE = (20,20,20)
BTN_HOVER= (45,45,45)
OK_COL   = (60, 200, 100)
ERR_COL  = (220, 60, 60)
BACK_COL = (220,220,220)
WHITE    = (255,255,255)

NODE_R=22; LGAP=64


def node_pos(n,cx,ty):
    pos={}; lv=0; i=0
    while i<n:
        cnt=2**lv; y=ty+lv*LGAP; sp=max(32,380//(cnt+1))
        for j in range(cnt):
            if i>=n: break
            pos[i]=(cx-(cnt-1)*sp//2+j*sp,y); i+=1
        lv+=1
    return pos


def draw_heap_tree(sur,fsm,heap,pos):
    ftiny=pygame.font.SysFont("consolas",11)
    for i in range(len(heap)):
        for ch in (2*i+1,2*i+2):
            if ch<len(heap) and i in pos and ch in pos:
                pygame.draw.line(sur,EDGE_COL,pos[i],pos[ch],2)
    for i,(prio,name) in enumerate(heap):
        if i not in pos: continue
        x,y=pos[i]
        pygame.draw.circle(sur,NODE_BG,(x,y),NODE_R)
        pygame.draw.circle(sur,ACCENT, (x,y),NODE_R,2)
        pl=fsm.render(str(prio),True,HIGH_COL)
        nl=ftiny.render(name[:7],True,WHITE)
        sur.blit(pl,(x-pl.get_width()//2,y-13))
        sur.blit(nl,(x-nl.get_width()//2,y+4))


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
    ftitle=pygame.font.SysFont("consolas",24,bold=True)
    fmed  =pygame.font.SysFont("consolas",13,bold=True)
    fsm   =pygame.font.SysFont("consolas",13)

    heap=[]
    for p,n in [(3,"Eat"),(1,"Sleep"),(5,"Work"),(2,"Exercise")]:
        heapq.heappush(heap,(p,n))

    log=[]; ni=""; pi=""; na=False; pa=False; msg=""; mc=OK_COL

    log_w=260           # fixed log panel width
    lx=W-log_w-15       # log panel left edge
    ltop=145            # log panel top
    tcx=(lx)//2         # tree centre = middle of left zone
    ty=170              # tree top (below controls+info)

    nr =pygame.Rect(20, 58,130,28); pr=pygame.Rect(158,58,80,28)
    ab =pygame.Rect(246,58,100,28); pb=pygame.Rect(354,58,140,28)
    clb=pygame.Rect(502,58,75, 28); back=pygame.Rect(W//2-80,H-46,160,32)

    running=True
    while running:
        screen.fill(BG)
        t=ftitle.render("Event Queue Simulator",True,ACCENT)
        screen.blit(t,(W//2-t.get_width()//2,16))

        screen.blit(fsm.render("Event name:",True,TEXT_COL),(20,42))
        screen.blit(fsm.render("Priority:",  True,TEXT_COL),(158,42))
        draw_inp(screen,fsm,nr,ni,na,ACCENT); draw_inp(screen,fsm,pr,pi,pa,ACCENT)
        draw_btn(screen,fsm,"Add Event",   ab, ACCENT)
        draw_btn(screen,fsm,"Process Next",pb, OK_COL)
        draw_btn(screen,fsm,"Clear All",   clb,(140,140,140))

        if msg: screen.blit(fsm.render(msg,True,mc),(20,94))
        screen.blit(fsm.render(f"Heap size: {len(heap)}",True,TEXT_COL),(20,112))
        if heap:
            mn=fsm.render(f"Next: [{heap[0][0]}] {heap[0][1]}",True,HIGH_COL)
            screen.blit(mn,(160,112))

        if heap:
            pos=node_pos(len(heap),tcx,ty); draw_heap_tree(screen,fsm,heap,pos)

        lh2=H-ltop-52
        pygame.draw.rect(screen,LOG_BG, pygame.Rect(lx-6,ltop-6,log_w+12,lh2+6),border_radius=8)
        pygame.draw.rect(screen,ACCENT, pygame.Rect(lx-6,ltop-6,log_w+12,lh2+6),1,border_radius=8)
        screen.blit(fmed.render("Processed Events:",True,ACCENT),(lx,ltop-2))
        max_rows=lh2//22-1
        for i,(p2,n2) in enumerate(log[-max_rows:]):
            screen.blit(fsm.render(f"  [{p2}]  {n2}",True,TEXT_COL),(lx,ltop+20+i*22))

        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN:
                na=nr.collidepoint(ev.pos); pa=pr.collidepoint(ev.pos)
            if ev.type==pygame.KEYDOWN:
                if na:
                    if ev.key==pygame.K_BACKSPACE: ni=ni[:-1]
                    elif len(ni)<14: ni+=ev.unicode
                elif pa:
                    if ev.key==pygame.K_BACKSPACE: pi=pi[:-1]
                    elif ev.unicode.isdigit() and len(pi)<3: pi+=ev.unicode
            if clicked(ab,ev):
                if ni.strip() and pi.strip():
                    try:
                        p2=int(pi.strip()); heapq.heappush(heap,(p2,ni.strip()))
                        msg=f"Added '{ni.strip()}' (priority {p2})"; mc=OK_COL; ni=""; pi=""
                    except ValueError: msg="Priority must be a number"; mc=ERR_COL
                else: msg="Enter both name and priority"; mc=ERR_COL
            if clicked(pb,ev):
                if heap:
                    p2,n2=heapq.heappop(heap); log.append((p2,n2))
                    msg=f"Processed: '{n2}'  (priority {p2})"; mc=OK_COL
                else: msg="Queue is empty!"; mc=ERR_COL
            if clicked(clb,ev): heap=[]; log=[]; msg="Cleared"; mc=TEXT_COL
            if clicked(back,ev): running=False
        clock.tick(60)
