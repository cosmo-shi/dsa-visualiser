import pygame
import sys
import unittest
import io

# ── Colours ──
BG         = (0, 0, 0)
TITLE_COL  = (220,220,220)
TEXT_COL   = (230,230,230)
SUB_COL    = (90,90,90)
BTN_BASE   = (20,20,20)
BTN_HOVER  = (45,45,45)
BTN_BORDER = (220,220,220)
P1_COL     = (200,200,200)
P2_COL     = (180,180,180)
P3_COL     = (210,210,210)
TEST_COL   = (200,200,200)
PASS_COL   = (200,200,200)
FAIL_COL   = (160,160,160)

WIDTH, HEIGHT = 900, 700


# Shared helpers
def draw_button(surface, font, text, rect, accent):
    mouse = pygame.mouse.get_pos()
    bg    = BTN_HOVER if rect.collidepoint(mouse) else BTN_BASE
    pygame.draw.rect(surface, bg,     rect, border_radius=8)
    pygame.draw.rect(surface, accent, rect, 2, border_radius=8)
    lbl = font.render(text, True, accent)
    surface.blit(lbl, (
        rect.x + (rect.w - lbl.get_width())  // 2,
        rect.y + (rect.h - lbl.get_height()) // 2
    ))


def is_clicked(rect, event):
    return (
        event.type == pygame.MOUSEBUTTONDOWN
        and event.button == 1
        and rect.collidepoint(event.pos)
    )


# In-app test runner
def run_tests_screen(screen, clock):
    from test_phase1 import TestPhase1
    from test_phase2 import TestPhase2
    from test_phase3 import TestPhase3

    font_title = pygame.font.SysFont("consolas", 26, bold=True)
    font_med   = pygame.font.SysFont("consolas", 17, bold=True)
    font_sm    = pygame.font.SysFont("consolas", 14)

    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestPhase1))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase2))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase3))

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    lines = []
    for line in stream.getvalue().splitlines():
        if " ... ok" in line:
            lines.append((line.replace(" ... ok", ""), "PASS"))
        elif " ... FAIL" in line:
            lines.append((line.replace(" ... FAIL", ""), "FAIL"))
        elif " ... ERROR" in line:
            lines.append((line.replace(" ... ERROR", ""), "ERROR"))
        elif line.strip():
            lines.append((line, "INFO"))

    for test, tb in result.failures + result.errors:
        lines.append(("  " + str(test), "FAIL"))
        for dl in tb.splitlines()[-2:]:
            lines.append(("    " + dl, "INFO"))

    total  = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    failed = len(result.failures) + len(result.errors)

    back_btn = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 52, 160, 36)
    scroll_y = 0
    line_h   = 22
    clip_top = 108
    clip_h   = HEIGHT - clip_top - 64

    running = True
    while running:
        screen.fill(BG)
        title = font_title.render("Test Results", True, TITLE_COL)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 18))

        summary_col = PASS_COL if failed == 0 else FAIL_COL
        summary = font_med.render(
            f"Total: {total}   Passed: {passed}   Failed: {failed}",
            True, summary_col
        )
        screen.blit(summary, (WIDTH // 2 - summary.get_width() // 2, 58))

        screen.set_clip(pygame.Rect(30, clip_top, WIDTH - 60, clip_h))
        for i, (text, status) in enumerate(lines):
            y = clip_top + i * line_h - scroll_y
            if y < clip_top - line_h or y > clip_top + clip_h:
                continue
            if status == "PASS":
                col = PASS_COL; prefix = "✔  "
            elif status in ("FAIL", "ERROR"):
                col = FAIL_COL; prefix = "✘  "
            else:
                col = TEXT_COL; prefix = "   "
            lbl = font_sm.render(prefix + text, True, col)
            screen.blit(lbl, (40, y))
        screen.set_clip(None)

        draw_button(screen, font_sm, "◀  Back to Menu", back_btn, BTN_BORDER)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                max_s    = max(0, len(lines) * line_h - clip_h)
                scroll_y = max(0, min(scroll_y - event.y * line_h, max_s))
            if is_clicked(back_btn, event):
                running = False

        clock.tick(60)


# Module launcher
def launch(key, screen, clock):
    if key == "stack_queue":
        from stack_queue     import run
    elif key == "linked_list":
        from linked_list     import run
    elif key == "bst":
        from bst             import run
    elif key == "sorting":
        from sorting         import run
    elif key == "graph":
        from graph_traversal import run
    elif key == "heap":
        from heap            import run
    elif key == "pathfinding":
        from pathfinding     import run
    elif key == "event_queue":
        from event_queue     import run
    elif key == "dp_grid":
        from dp_grid         import run
    else:
        return
    run(screen, clock)


# Main Menu
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DSA Explorer & Visualiser")
    clock  = pygame.time.Clock()

    font_title   = pygame.font.SysFont("consolas", 38, bold=True)
    font_sub     = pygame.font.SysFont("consolas", 14)
    font_section = pygame.font.SysFont("consolas", 14, bold=True)
    font_btn     = pygame.font.SysFont("consolas", 16, bold=True)

    # ── Layout constants ──
    BTN_W   = 340
    BTN_H   = 44
    COL_GAP = 30
    ROW_GAP = 12
    SEC_GAP = 28 

    total_w = BTN_W * 2 + COL_GAP
    LEFT_X  = (WIDTH - total_w) // 2
    RIGHT_X = LEFT_X + BTN_W + COL_GAP


    PHASES = [
        ("Data Structures", P1_COL, [
            ("Stack & Queue",  "stack_queue"),
            ("Linked List",    "linked_list"),
            ("BST Visualiser", "bst"),
        ]),
        ("Algorithm Visualiser", P2_COL, [
            ("Sorting",         "sorting"),
            ("Graph Traversal", "graph"),
            ("Heap",            "heap"),
        ]),
        ("Puzzle Challenges", P3_COL, [
            ("Pathfinding",  "pathfinding"),
            ("Event Queue",  "event_queue"),
            ("DP Grid",      "dp_grid"),
        ]),
    ]

    def build_layout(start_y):
        items = []   # (rect, key, colour)
        y = start_y
        for (sec_title, col, btns) in PHASES:
            sec_y = y
            y += 26   
            row_items = []
            for i, (label, key) in enumerate(btns):
                col_idx = i % 2
                row_idx = i // 2
                x   = LEFT_X  if col_idx == 0 else RIGHT_X
                ry  = y + row_idx * (BTN_H + ROW_GAP)
                rect = pygame.Rect(x, ry, BTN_W, BTN_H)
                items.append((rect, label, key, col))
            rows = (len(btns) + 1) // 2
            y += rows * (BTN_H + ROW_GAP) - ROW_GAP + SEC_GAP

        tests_rect = pygame.Rect(LEFT_X + BTN_W // 2 - BTN_W // 2,
                                  y + 10, BTN_W, BTN_H)
        tests_rect = pygame.Rect(WIDTH // 2 - BTN_W // 2, y + 10, BTN_W, BTN_H)
        items.append((tests_rect, "Run Tests", "tests", TEST_COL))
        return items

    START_Y = 150
    all_items = build_layout(START_Y)

    def build_section_headers(start_y):
        headers = []
        y = start_y
        for (sec_title, col, btns) in PHASES:
            headers.append((sec_title, col, y))
            y += 26
            rows = (len(btns) + 1) // 2
            y += rows * (BTN_H + ROW_GAP) - ROW_GAP + SEC_GAP
        return headers

    headers = build_section_headers(START_Y)

    while True:
        screen.fill(BG)

        title = font_title.render("DSA Explorer & Visualiser", True, TITLE_COL)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 28))

        sub = font_sub.render("Select a module to begin", True, SUB_COL)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 82))

        for sec_title, col, hy in headers:
            h = font_section.render(sec_title, True, col)
            screen.blit(h, (WIDTH // 2 - h.get_width() // 2, hy + 4))

        for rect, label, key, col in all_items:
            draw_button(screen, font_btn, label, rect, col)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            for rect, label, key, col in all_items:
                if is_clicked(rect, event):
                    if key == "tests":
                        run_tests_screen(screen, clock)
                    else:
                        launch(key, screen, clock)

        clock.tick(60)


if __name__ == "__main__":
    main_menu()
