import pygame, sys

BG       = (0,0,0)
ACCENT   = (220,220,220)
EMPTY_C  = (25, 25, 50)
WALL_C   = (20, 20, 20)
START_C  = (0, 200, 80)
END_C    = (220, 60, 60)
PATH_C   = (240, 200, 0)
DP_FILL  = (20, 50, 80)
DP_TXT   = (100, 200, 255)
ZERO_C   = (50, 20, 20)
TEXT_COL = (230,230,230)
BTN_BASE = (20,20,20)
BTN_HOVER= (45,45,45)
BACK_COL = (220,220,220)
WHITE    = (255,255,255)

ROWS=8; COLS=12; CELL=54; GX=20; GY=110


# ── DP logic ──
def count_paths(grid):
    """
    Returns dp table. dp[r][c] = number of unique paths from (0,0) to (r,c).
    Only right and down moves allowed; walls block paths.
    """
    R=len(grid); C=len(grid[0])
    dp=[[0]*C for _ in range(R)]
    if grid[0][0]==0: dp[0][0]=1
    for c in range(1,C):
        if grid[0][c]==0: dp[0][c]=dp[0][c-1]
    for r in range(1,R):
        if grid[r][0]==0: dp[r][0]=dp[r-1][0]
    for r in range(1,R):
        for c in range(1,C):
            if grid[r][c]==0: dp[r][c]=dp[r-1][c]+dp[r][c-1]
    return dp


def reconstruct_path(dp,grid):
    """Walk backwards from bottom-right to top-left to find one valid path."""
    R=len(dp); C=len(dp[0])
    r,c=R-1,C-1; path=[]
    if dp[r][c]==0: return []
    while r>0 or c>0:
        path.append((r,c))
        if   r==0: c-=1
        elif c==0: r-=1
        elif dp[r-1][c]>=dp[r][c-1]: r-=1
        else: c-=1
    path.append((0,0)); path.reverse(); return path


def draw_btn(sur,fnt,txt,rect,acc):
    bg=BTN_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BTN_BASE
    pygame.draw.rect(sur,bg, rect,border_radius=6)
    pygame.draw.rect(sur,acc,rect,2,border_radius=6)
    l=fnt.render(txt,True,acc)
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
    fdp   =pygame.font.SysFont("consolas",12,bold=True)

    grid=[[0]*COLS for _ in range(ROWS)]
    dp=None; path=[]; acells=[]; ai=0; phase="idle"; atimer=0
    START=(0,0); END=(ROWS-1,COLS-1)

    rb =pygame.Rect(20,62,90, 28)
    clb=pygame.Rect(118,62,75,28)
    back=pygame.Rect(W//2-80,H-46,160,32)

    def reset():
        nonlocal dp,path,acells,ai,phase
        dp=None; path=[]; acells=[]; ai=0; phase="idle"

    running=True
    while running:
        now=pygame.time.get_ticks(); screen.fill(BG)
        t=ftitle.render("DP Grid  –  Count Unique Paths",True,ACCENT)
        screen.blit(t,(W//2-t.get_width()//2,16))
        screen.blit(fsm.render("Left-click=toggle wall   Right-click=erase   Start: top-left   End: bottom-right",True,TEXT_COL),(20,46))

        draw_btn(screen,fsm,"▶ Run",rb, ACCENT)
        draw_btn(screen,fsm,"Clear",clb,(140,140,140))

        if phase=="done" and dp is not None:
            total=dp[ROWS-1][COLS-1]
            col=PATH_C if total>0 else END_C
            screen.blit(fsm.render(f"Total unique paths: {total}" if total>0 else "No path exists!",True,col),(220,66))

        pset=set(path)
        revealed=set()
        if dp is not None:
            for idx in range(ai):
                revealed.add(acells[idx])

        for r in range(ROWS):
            for c in range(COLS):
                x=GX+c*CELL; y=GY+r*CELL; rc=(r,c)
                if   rc==START:     bg_c=START_C
                elif rc==END:       bg_c=END_C
                elif grid[r][c]==1: bg_c=WALL_C
                elif rc in pset and phase=="done": bg_c=PATH_C
                elif rc in revealed: bg_c=DP_FILL if(dp and dp[r][c]>0)else ZERO_C
                else: bg_c=EMPTY_C
                pygame.draw.rect(screen,bg_c,pygame.Rect(x+1,y+1,CELL-2,CELL-2))
                if dp is not None and rc in revealed and grid[r][c]==0:
                    v=dp[r][c]; vl=fdp.render(str(v),True,WHITE if rc in pset else DP_TXT)
                    screen.blit(vl,(x+(CELL-vl.get_width())//2,y+(CELL-vl.get_height())//2))

        for r in range(ROWS+1):
            pygame.draw.line(screen,(55,55,55),(GX,GY+r*CELL),(GX+COLS*CELL,GY+r*CELL))
        for c in range(COLS+1):
            pygame.draw.line(screen,(55,55,55),(GX+c*CELL,GY),(GX+c*CELL,GY+ROWS*CELL))

        sy2=GY+ROWS*CELL+5
        LEG=[("Start",START_C),("End",END_C),("Wall",WALL_C),("Path",PATH_C),("DP value",DP_FILL)]
        lx2=W-400
        for i,(lb,col) in enumerate(LEG):
            pygame.draw.rect(screen,col,pygame.Rect(lx2+i*78,sy2,13,13))
            screen.blit(fsm.render(lb,True,TEXT_COL),(lx2+i*78+16,sy2))

        draw_btn(screen,fsm,"◀  Back to Menu",back,BACK_COL)
        pygame.display.flip()

        if phase=="filling":
            if now-atimer>=28:
                atimer=now
                if ai<len(acells): ai+=1
                else: phase="done"; path=reconstruct_path(dp,grid)

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                cell=cell_at(*ev.pos)
                if cell and cell!=START and cell!=END:
                    r2,c2=cell; grid[r2][c2]=1-grid[r2][c2]; reset()
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==3:
                cell=cell_at(*ev.pos)
                if cell and cell!=START and cell!=END:
                    r2,c2=cell; grid[r2][c2]=0; reset()
            if clicked(rb,ev):
                reset(); dp=count_paths(grid)
                acells=[(r,c) for r in range(ROWS) for c in range(COLS)]
                ai=0; phase="filling"; atimer=pygame.time.get_ticks()
            if clicked(clb,ev):
                grid=[[0]*COLS for _ in range(ROWS)]; reset()
            if clicked(back,ev): running=False

        if pygame.mouse.get_pressed()[2]:
            cell=cell_at(*pygame.mouse.get_pos())
            if cell and cell!=START and cell!=END:
                r2,c2=cell
                if grid[r2][c2]==1: grid[r2][c2]=0; reset()
        clock.tick(60)
