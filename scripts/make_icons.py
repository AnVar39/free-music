"""Рисует иконки приложения. `python3 scripts/make_icons.py web` — иконки сайта,
`python3 scripts/make_icons.py android` — значки запуска для Android-проекта."""
import os, sys
from PIL import Image, ImageDraw

def draw(size, pad):
    im = Image.new('RGB', (size, size), '#2447f5'); d = ImageDraw.Draw(im)
    u = (size - 2 * pad) / 100
    P = lambda x, y: (pad + x * u, pad + y * u)
    d.line([P(62, 22), P(62, 66)], fill='white', width=int(7 * u))
    d.line([P(62, 22), P(80, 30)], fill='white', width=int(7 * u))
    d.ellipse([*P(40, 58), *P(64, 76)], fill='white')
    d.polygon([P(26, 40), P(46, 40), P(36, 54)], fill='white')
    d.rectangle([*P(33, 22), *P(39, 42)], fill='white')
    return im

mode = sys.argv[1] if len(sys.argv) > 1 else 'web'
if mode == 'web':
    os.makedirs('icons', exist_ok=True)
    draw(192, 16).save('icons/icon-192.png')
    draw(512, 40).save('icons/icon-512.png')
    draw(512, 90).save('icons/icon-maskable-512.png')
else:
    res = 'android/app/src/main/res'
    fg = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}
    leg = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
    base = draw(1024, 180)
    for dens in fg:
        folder = f'{res}/mipmap-{dens}'
        os.makedirs(folder, exist_ok=True)
        base.resize((fg[dens], fg[dens]), Image.LANCZOS).save(f'{folder}/ic_launcher_foreground.png')
        for name in ('ic_launcher.png', 'ic_launcher_round.png'):
            base.resize((leg[dens], leg[dens]), Image.LANCZOS).save(f'{folder}/{name}')
    print('android icons written')
