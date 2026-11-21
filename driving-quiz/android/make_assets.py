"""Builds assets/ for the APK from ../web (page + question data inlined as a script, since WebView cannot fetch file:// URLs)."""
import os
here = os.path.dirname(os.path.abspath(__file__)); web = os.path.join(here, '..', 'web')
rd = lambda n: open(os.path.join(web, n), encoding='utf-8').read()
os.makedirs(os.path.join(here, 'assets'), exist_ok=True)
with open(os.path.join(here, 'assets', 'data.js'), 'w', encoding='utf-8') as f:
    f.write('window.QDATA=' + rd('questions.json') + ';\nwindow.QIMG=' + rd('images.json') + ';\nwindow.QVI=' + rd('vi.json') + ';\nwindow.QDESC=' + rd('desc.json') + ';\n')
with open(os.path.join(here, 'assets', 'index.html'), 'w', encoding='utf-8') as f:
    f.write('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
            '<script src="data.js"></script></head><body>\n' + rd('driving-quiz.html') + '\n</body></html>')
