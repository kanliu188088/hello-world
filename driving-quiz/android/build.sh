#!/bin/bash
# Builds build/driving-quiz.apk. Needs JDK 17+, python3, zip. Run ./fetch-tools.sh once first.
# Signing: uses release.p12 (not in git). Set KEYSTORE_PASS; a new key is generated if release.p12 is missing.
# Keep release.p12 safe: an APK signed with a different key cannot update an installed copy.
set -e; cd "$(dirname "$0")"; T=$PWD/tools; A=$T/aapt2pkg/aapt2/bin/Linux/aapt2
: "${KEYSTORE_PASS:?Set KEYSTORE_PASS to the keystore password}"
[ -f release.p12 ] || keytool -genkeypair -keystore release.p12 -storetype PKCS12 -storepass "$KEYSTORE_PASS" -alias key -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Driving Quiz"
rm -rf build; mkdir -p build/classes build/dex
python3 make_assets.py
$A compile --dir res -o build/res.zip
$A link -o build/base.apk -I $T/android-all.jar --manifest AndroidManifest.xml -A assets build/res.zip --min-sdk-version 24 --target-sdk-version 34
javac --release 8 -Xlint:-options -cp $T/android-all.jar -d build/classes src/app/drivingquiz/tw/MainActivity.java
java -cp $T/dx.jar com.android.dx.command.Main --dex --min-sdk-version=24 --output=build/dex/classes.dex build/classes
(cd build/dex && zip -q ../base.apk classes.dex)
python3 align.py build/base.apk build/aligned.apk
javac -cp $T/apksig.jar -d build src/Sign.java
java --add-exports java.base/sun.security.x509=ALL-UNNAMED --add-exports java.base/sun.security.pkcs=ALL-UNNAMED \
  -cp $T/apksig.jar:build Sign release.p12 "$KEYSTORE_PASS" build/aligned.apk build/driving-quiz.apk
