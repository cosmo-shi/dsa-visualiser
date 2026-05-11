import pygame, sys, heapq

BG       = (0,0,0)
ACCENT   = (210,210,210)
EMPTY_C  = (25, 25, 50)
WALL_C   = (80, 80, 80)
START_C  = (0, 200, 80)
END_C    = (220, 60, 60)
VISIT_C  = (80, 40, 160)  
PATH_C   = (240, 200, 0)    
GRID_C   = (55,55,55)
TEXT_COL = (230,230,230)
BTN_BASE = (20,20,20)
BTN_HOVER= (45,45,45)
BACK_COL = (220,220,220)
WHITE    = (255,255,255)

ROWS=14; COLS=24; CELL=26; GX=20; GY=110


def dijkstra_grid(grid,start,end):
    """Returns (visited_order, path). path=[] if no path found."""
    INF=float("inf"); rows=len(grid); cols=len(grid[0])
    dist=[[INF]*cols for _ in range(rows)]
    prev=[[None]*cols for _ in range(rows)]
    dist[start[0]][start[1]]=0
    pq=[(0,start[0],start[1])]; vset=set(); vorder=[]
    dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    while pq:
        cost,r,c=heapq.heappop(pq)
        if (r,c) in vset: continue
        vset.add((r,c)); vorder.append((r,c))
        if (r,c)==end: break
        for dr,dc in dirs:
            nr,nc=r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0:
                nc2=cost+1
                if nc2<dist[nr][nc]:
                    dist[nr][nc]=nc2; prev[nr][nc]=(r,c)
                    heapq.heappush(pq,(nc2,nr,nc))
    path=[]; node=end
    while node: path.append(node); node=prev[node[0]][node[1]]
    path.reverse()
    return vorder,(path if path and path[0]==start else [])


def draw_btn(sur,fnt,txt,rect,acc,active=False):
    bg=(20,20,20) if active else (BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE)
    pygame.draw.rect(sur,bg,  rect,border_radius=6)
    pygame.draw.rect(sur,acc, rect,2,border_radius=6)
    l=fnt.render(txt,True,WHITE if active else acc)
    sur.blit(l,(rect.x+(rect.w-l.get_width())//2,rect.y+(rect.h-l.get_height())//2))


def clicked(rect,ev):
    return ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and rect.collidepoint(ev.pos)


def cell_at(mx,my):
    c=(mx-GX)//CELL; r=(my-GY)//CELL
    return (r,c) if 0<=r<ROWS and 0<=c<COLS else None


def run(screen, clock):
    W,H=screen.get_size()
    ftitle=pygame.font.SysFont("consolas",24,bold=True)
    fsm   =pygame.font.SysFont("consolas",13)

    grid=[[0]*COLS for _ in range(ROWS)]
    start=(1,1); end=(ROWS-2,COLS-2); mode="wall"

    vorder=[]; path=[]; vset=set(); pset=set()
    vi=0; pi=0; phase="idle"; atimer=0

    sb =pygame.Rect(20, 62,100,28); eb=pygame.Rect(128,62,80,28)
    wb =pygame.Rect(216,62,70, 28); rb=pygame.Rect(294,62,90,28)
    clb=pygame.Rect(392,62,75, 28); back=pygame.Rect(W//2-80,H-46,160,32)

    def reset_anim():
        nonlocal vorder,path,vset,pset,vi,pi,phase
        vorder=[]; path=[]; vset=set(); pset=set(); vi=0; pi=0; phase="idle"

    running=True
    while running:
        now=pygame.time.get_ticks(); screen.fill(BG)
        t=ftitle.render("Pathfinding Puzzle  –  Dijkstra",True,ACCENT)
        screen.blit(t,(W//2-t.get_width()//2,16))

        draw_btn(screen,fsm,"Set Start",sb,  START_C,mode=="start")
        draw_btn(screen,fsm,"Set End",  eb,  END_C,  mode=="end")
        draw_btn(screen,fsm,"Wall",     wb,  (150,150,150),mode=="wall")
        draw_btn(screen,fsm,"▶ Run",    rb,  ACCENT)
        draw_btn(screen,fsm,"Clear",    clb, (140,140,140))

        screen.blit(fsm.render("Mode: "+mode.upper()+"   Left-drag=wall   Right-drag=erase",True,TEXT_COL),(20,96))

        for r in range(ROWS):
            for c in range(COLS):
                x=GX+c*CELL; y=GY+r*CELL; rc=(r,c)
                if   rc==start:     col=START_C
                elif rc==end:       col=END_C
                elif grid[r][c]==1: col=WALL_C
                elif rc in pset:    col=PATH_C
                elif rc in vset:    col=VISIT_C
                else:               col=EMPTY_C
                pygame.draw.rect(screen,col,pygame.Rect(x+1,y+1,CELL-2,CELL-2))

        for r in range(ROWS+1):
            pygame.draw.line(screen,GRID_C,(GX,GY+r*CELL),(GX+COLS*CELL,GY+r*CELL))
        for c in range(COLS+1):
            pygame.draw.line(screen,GRID_C,(GX+c*CELL,GY),(GX+c*CELL,GY+ROWS*CELL))

        sy2=GY+ROWS*CELL+5
        if phase=="done":
            msg=(f"Shortest path: {len(path)-1} steps" if path else "No path found!")
            screen.blit(fsm.render(msg,True,PATH_C if path else END_C),(20,sy2))
        elif phase in("visiting","pathing"):
            screen.blit(fsm.render("Searching...",True,VISIT_C),(20,sy2))

        LEG=[("Start",START_C),("End",END_C),("Wall",WALL_C),("Visited",VISIT_C),("Path",PATH_C)]
        lx2=W-360
        for i,(lb,col) in enumerate(LEG):
            r2=pygame.Rect(lx2+i*70,sy2,13,13)
            pygame.draw.rect(screen,col,r2)
            pygame.draw.rect(screen,(180,180,180),r2,1)
            screen.blit(fsm.render(lb,True,TEXT_COL),(lx2+i*70+16,sy2))

        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        if phase=="visiting":
            if now-atimer>=14:
                atimer=now
                if vi<len(vorder): vset.add(vorder[vi]); vi+=1
                else: phase="pathing"; pi=0
        elif phase=="pathing":
            if now-atimer>=35:
                atimer=now
                if pi<len(path): pset.add(path[pi]); pi+=1
                else: phase="done"

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                cell=cell_at(*ev.pos)
                if cell:
                    r2,c2=cell; reset_anim()
                    if   mode=="start": start=(r2,c2); grid[r2][c2]=0
                    elif mode=="end":   end  =(r2,c2); grid[r2][c2]=0
                    elif mode=="wall" and (r2,c2)!=start and (r2,c2)!=end: grid[r2][c2]=1
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==3:
                cell=cell_at(*ev.pos)
                if cell:
                    r2,c2=cell
                    if (r2,c2)!=start and (r2,c2)!=end: grid[r2][c2]=0
            if clicked(sb, ev): mode="start"
            if clicked(eb, ev): mode="end"
            if clicked(wb, ev): mode="wall"
            if clicked(rb, ev):
                reset_anim()
                vorder,path=dijkstra_grid(grid,start,end)
                phase="visiting"; atimer=pygame.time.get_ticks()
            if clicked(clb,ev):
                grid=[[0]*COLS for _ in range(ROWS)]; reset_anim()
            if clicked(back,ev): running=False

        if pygame.mouse.get_pressed()[0] and mode=="wall":
            cell=cell_at(*pygame.mouse.get_pos())
            if cell:
                r2,c2=cell
                if (r2,c2)!=start and (r2,c2)!=end: grid[r2][c2]=1
        if pygame.mouse.get_pressed()[2]:
            cell=cell_at(*pygame.mouse.get_pos())
            if cell:
                r2,c2=cell
                if (r2,c2)!=start and (r2,c2)!=end: grid[r2][c2]=0
        clock.tick(60)
