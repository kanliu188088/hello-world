package app.drivingquiz.tw;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import java.util.Locale;

public class MainActivity extends Activity implements TextToSpeech.OnInitListener {
    private WebView web;
    private TextToSpeech tts;
    private volatile boolean ready = false;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        web.addJavascriptInterface(new Bridge(), "AndroidTTS");
        setContentView(web);
        tts = new TextToSpeech(getApplicationContext(), this);
        web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onInit(int status) {
        if (status != TextToSpeech.SUCCESS) return;
        int r = tts.setLanguage(Locale.TAIWAN);
        if (r < 0) r = tts.setLanguage(Locale.CHINESE);
        ready = r >= 0;
        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override public void onStart(String id) {}
            @Override public void onDone(String id) { report(id, true); }
            @Override public void onError(String id) { report(id, false); }
        });
    }

    private void report(final String id, final boolean ok) {
        runOnUiThread(new Runnable() {
            @Override public void run() {
                if (web != null) web.evaluateJavascript("window.__tts&&window.__tts('" + id.replaceAll("[^0-9]", "") + "'," + ok + ")", null);
            }
        });
    }

    private class Bridge {
        @JavascriptInterface
        public void speak(String text, float rate, String id) {
            if (!ready || tts == null) { report(id, false); return; }
            tts.setSpeechRate(rate);
            if (tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, id) != TextToSpeech.SUCCESS) report(id, false);
        }
        @JavascriptInterface
        public void stop() { if (tts != null) tts.stop(); }
        @JavascriptInterface
        public void openSettings() {
            try { startActivity(new Intent("com.android.settings.TTS_SETTINGS").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); }
            catch (Exception e) { try { startActivity(new Intent(android.provider.Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); } catch (Exception e2) {} }
        }
    }

    @Override protected void onPause() { super.onPause(); if (tts != null) tts.stop(); }

    @Override
    protected void onDestroy() {
        if (tts != null) { tts.stop(); tts.shutdown(); tts = null; }
        if (web != null) { web.destroy(); web = null; }
        super.onDestroy();
    }
}
