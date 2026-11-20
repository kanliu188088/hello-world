# 汽車筆試題庫練習 (driving test practice)

Study and mock-exam app for the Taiwan car written test question bank (1,090 questions, Chinese, with Vietnamese button labels).

- **Study**: one question at a time; "讀給我聽" reads the question and options aloud in Chinese, then shows and reads the answer.
- **Exam**: random questions, silent, no answers shown; score and wrong-answer review at the end.

## Layout

- `web/` — the page (`driving-quiz.html`) and its data (`questions.json`, `images.json`).
- `android/` — WebView wrapper with a native text-to-speech bridge, and the APK build scripts.
- `extract/` — scripts that produced the data from the question-bank PDF (PDF not included).

## Build the APK

```bash
cd android
./fetch-tools.sh
KEYSTORE_PASS=your-password ./build.sh
```

Output: `android/build/driving-quiz.apk` (Android 7.0+, v2 signature). The signing key `release.p12` is created on first build and is not committed; keep it, because an APK signed with a different key cannot update an installed copy.

## Regenerate the data from the PDF

Needs `pdfplumber` and `Pillow`. Run from `extract/`:

```bash
python3 parse.py question-bank.pdf
python3 build.py question-bank.pdf ../web
```
