#!/usr/bin/env bash
# Готовит Android-проект: веб-файлы -> www, создаёт android/, добавляет нативный код и иконки.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf www && mkdir www
cp index.html manifest.webmanifest sw.js www/
cp -r icons www/icons

[ -d android ] || npx cap add android

PKG=android/app/src/main/java/com/freemusic/app
mkdir -p "$PKG"
cp android-overrides/*.java "$PKG/"

# Загрузки через DownloadManager не требуют разрешений на Android 10+
sed -i 's/minSdkVersion = [0-9]*/minSdkVersion = 29/' android/variables.gradle

python3 scripts/make_icons.py android
npx cap sync android
echo "Android-проект готов"
