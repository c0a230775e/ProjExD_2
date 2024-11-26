import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA ={pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたrectが画面内か画面外かを判定
    引数：こうかとんRectか爆弾Rect
    戻り値：真理値タプル（横、縦）/画面内：True, 画面外False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に、半透明の黒い画面上で「Game Over」と表示し、
    泣いているこうかとん画像を張り付ける
    """
    bg_img_n8 = pg.image.load("fig/8.png")  # こうかとん画像ロード
    fonto = pg.font.Font(None, 100)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    game_over = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(game_over, (0, 0, 0), [0, 0, WIDTH, HEIGHT])
    game_over.set_alpha(128)
    screen.blit(game_over, (0, 0))  # 半透明画面描画
    screen.blit(txt, [WIDTH/2-200, HEIGHT/2])  # Game Over描画
    screen.blit(bg_img_n8, [WIDTH/2-270, HEIGHT/2])  # 泣いてるこうかとん描画
    screen.blit(bg_img_n8, [WIDTH/2+200, HEIGHT/2])
    print("kansujikkou")
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾surfaceを要素としたリストと加速度リストを返す
    """
    bb_img, accs = True, True
    accs = [a for a in range(1, 11)]
    bb_imgs =[]  # 拡大爆弾リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, accs


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像surfaceを返す
    """
    c_img = {
        (5,0):
    }



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとん画像
    bb_img = pg.Surface((20, 20))  # 爆弾用空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円描く
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    vx, vy = +5, +5  # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)  # 爆弾移動
        g_rct = bb_img.get_rect()
        bb_rct.width, bb_rct.height= g_rct.width, g_rct.height
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
