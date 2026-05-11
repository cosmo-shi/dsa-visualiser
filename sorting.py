import pygame, sys, random, time

BG         = (0,0,0)
ACCENT     = (180,180,180)
BAR_DEF    = (40, 40, 80)
BAR_CMP    = (220, 60, 60)
BAR_SORTED = (60, 200, 100)
BAR_MIN    = (240, 200, 0)
TEXT_COL   = (230,230,230)
BTN_BASE   = (20,20,20)
BTN_HOVER  = (45,45,45)
BACK_COL   = (220,220,220)
WHITE      = (255,255,255)

N          = 40
BGAP       = 2
DELAY      = 0.022


def bubble_steps(arr):
    a=arr[:]; n=len(a)
    for i in range(n):
        sw=False
        for j in range(n-i-1):
            yield a[:],[j,j+1],list(range(n-i,n))
            if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]; sw=True
        if not sw: break
    yield a[:],[],list(range(n))


def selection_steps(arr):
    a=arr[:]; n=len(a)
    for i in range(n):
        mi=i
        for j in range(i+1,n):
            yield a[:],[j,mi],list(range(i))
            if a[j]<a[mi]: mi=j
        a[i],a[mi]=a[mi],a[i]
    yield a[:],[],list(range(n))


def merge_steps(arr):
    a=arr[:]; steps=[]
    def ms(sub,off):
        if len(sub)<=1: return sub
        mid=len(sub)//2
        L=ms(sub[:mid],off); R=ms(sub[mid:],off+mid)
        return mg(L,R,off)
    def mg(L,R,off):
        merged=[]; li=ri=0
        while li<len(L) and ri<len(R):
            steps.append((a[:],[off+li,off+len(L)+ri],[]))
            if L[li]<=R[ri]: merged.append(L[li]); li+=1
            else:             merged.append(R[ri]); ri+=1
        merged+=L[li:]; merged+=R[ri:]
        for k,v in enumerate(merged):
            a[off+k]=v; steps.append((a[:],[off+k],[]))
        return merged
    ms(a,0); steps.append((a[:],[],list(range(len(a))))); return steps


def draw_btn(sur,fnt,txt,rect,acc,active=False):
    bg=(20,20,20) if active else (BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE)
    pygame.draw.rect(sur,bg,  rect,border_radius=6)
    pygame.draw.rect(sur,acc, rect,2,border_radius=6)
    l=fnt.render(txt,True,WHITE if active else acc)
    sur.blit(l,(rect.x+(rect.w-l.get_width())//2,rect.y+(rect.h-l.get_height())//2))


def clicked(rect,ev):
    return ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and rect.collidepoint(ev.pos)


def draw_bars(sur,arr,ci,si,bw,lx,bot,maxv):
    area_h=bot-128
    for i,v in enumerate(arr):
        h=max(2,int(v/maxv*area_h)); x=lx+i*(bw+BGAP); y=bot-h
        col=BAR_SORTED if i in si else (BAR_CMP if(ci and i==ci[0])else(BAR_MIN if(len(ci)>1 and i==ci[1])else BAR_DEF))
        pygame.draw.rect(sur,col,pygame.Rect(x,y,bw,h))


def run(screen, clock):
    W,H=screen.get_size()
    ftitle=pygame.font.SysFont("consolas",26,bold=True)
    fsm   =pygame.font.SysFont("consolas",13)

    arr=[random.randint(5,100) for _ in range(N)]; maxv=100
    lx=20; bot=H-68; avail=W-40; bw=max(3,(avail-BGAP*N)//N)

    algo="Bubble"; steps=[]; si2=0; anim=False; last=0
    ca=arr[:]; ci=[]; srt=[]; elapsed=0.0; st=0.0

    bb=pygame.Rect(20, 50,120,30); slb=pygame.Rect(148,50,130,30)
    mb=pygame.Rect(286,50,120,30); gb=pygame.Rect(424,50,90, 30)
    rb=pygame.Rect(522,50,90, 30); back=pygame.Rect(W//2-80,H-48,160,34)

    def reset():
        nonlocal arr,ca,steps,si2,anim,ci,srt,elapsed
        arr=[random.randint(5,100) for _ in range(N)]
        ca=arr[:]; steps=[]; si2=0; anim=False; ci=[]; srt=[]; elapsed=0.0

    def start():
        nonlocal steps,si2,anim,last,ca,ci,srt,elapsed,st
        ca=arr[:]; ci=[]; srt=[]; elapsed=0.0; st=time.time()
        if   algo=="Bubble":    steps=list(bubble_steps(arr))
        elif algo=="Selection": steps=list(selection_steps(arr))
        else:                   steps=merge_steps(arr)
        si2=0; anim=True; last=time.time()

    running=True
    while running:
        now=time.time(); screen.fill(BG)
        t=ftitle.render("Sorting Algorithm Visualiser",True,ACCENT)
        screen.blit(t,(W//2-t.get_width()//2,14))

        draw_btn(screen,fsm,"Bubble Sort",   bb, ACCENT,algo=="Bubble")
        draw_btn(screen,fsm,"Selection Sort",slb,ACCENT,algo=="Selection")
        draw_btn(screen,fsm,"Merge Sort",    mb, ACCENT,algo=="Merge")
        draw_btn(screen,fsm,"▶ Start",       gb, (200,200,200))
        draw_btn(screen,fsm,"⟳ Reset",       rb, (210,210,210))

        info=f"Algorithm: {algo}   Step: {si2}/{len(steps)}"+(f"   Time: {elapsed:.2f}s" if elapsed>0 else "")
        screen.blit(fsm.render(info,True,TEXT_COL),(20,88))

        LEG=[("Comparing",BAR_CMP),("Pivot/Min",BAR_MIN),("Sorted",BAR_SORTED)]
        lx2=W-185
        for i,(lb,col) in enumerate(LEG):
            pygame.draw.rect(screen,col,pygame.Rect(lx2,50+i*17,13,12))
            screen.blit(fsm.render(lb,True,TEXT_COL),(lx2+16,49+i*17))

        draw_bars(screen,ca,ci,srt,bw,lx,bot,maxv)
        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        if anim and si2<len(steps):
            if now-last>=DELAY:
                last=now; snap,c2,s2=steps[si2]; ca=snap; ci=c2; srt=s2; si2+=1; elapsed=now-st
        elif anim:
            anim=False; ci=[]; srt=list(range(N))

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if clicked(bb, ev): algo="Bubble";    anim=False; ca=arr[:]
            if clicked(slb,ev): algo="Selection"; anim=False; ca=arr[:]
            if clicked(mb, ev): algo="Merge";     anim=False; ca=arr[:]
            if clicked(gb, ev): start()
            if clicked(rb, ev): reset()
            if clicked(back,ev): running=False
        clock.tick(60)
