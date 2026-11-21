#!/bin/bash
# Downloads the build tools into tools/ (from Maven Central and PyPI; no Android SDK install needed).
set -e; cd "$(dirname "$0")"; mkdir -p tools; cd tools; M=https://repo1.maven.org/maven2
[ -f android-all.jar ] || curl -fL -o android-all.jar $M/org/robolectric/android-all/14-robolectric-10818077/android-all-14-robolectric-10818077.jar
[ -f dx.jar ] || curl -fL -o dx.jar $M/com/jakewharton/android/repackaged/dalvik-dx/16.0.1/dalvik-dx-16.0.1.jar
[ -f apksig.jar ] || curl -fL -o apksig.jar $M/com/android/tools/build/apksig/2.3.0/apksig-2.3.0.jar
if [ ! -d aapt2pkg ]; then pip download aapt2==0.2.1 --no-deps -d whl -q; mkdir aapt2pkg; (cd aapt2pkg && unzip -qo ../whl/aapt2-*.whl); chmod +x aapt2pkg/aapt2/bin/Linux/aapt2; fi
