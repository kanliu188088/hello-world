"""Writes one self-contained HTML file (page + questions + pictures + translations) that opens in Safari or any browser.
Usage: python3 make_single.py [output.html]"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read().replace('</', '<\\/')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'driving-quiz-offline.html')
page = open(os.path.join(here, 'driving-quiz.html'), encoding='utf-8').read()
with open(out, 'w', encoding='utf-8') as f:
    f.write('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-title" content="汽車筆試練習">'
            '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
            '<script>window.QDATA=' + rd('questions.json') + ';\nwindow.QIMG=' + rd('images.json') +
            ';\nwindow.QVI=' + rd('vi.json') + ';\nwindow.QDESC=' + rd('desc.json') + ';</script></head><body>\n' + page + '\n</body></html>')
print(out, os.path.getsize(out))
