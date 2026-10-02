# Prayer Counter – offline file + Android APK

## A. One offline HTML file (no Netlify, no CDN)
    python build_offline.py
Creates `dist/prayer-counter-offline.html` (~21 MB, everything embedded). Needs internet only for this first build.
- **PC:** double-click the file (Chrome/Edge).
- **Android:** the camera needs a secure origin, so a file opened from Downloads will NOT get camera access. Either use the APK (B), or run it from Termux:
  `pkg install python` → put the file in a folder → `python -m http.server 8080` → open `http://localhost:8080/prayer-counter-offline.html` in Chrome.

## B. Android APK (no Android Studio needed) – GitHub Actions
1. Create a new GitHub repo and upload ALL files of this folder (keep the `.github` folder).
2. Open the repo → **Actions** → **Build APK** → **Run workflow**.
3. When it finishes (~5–8 min) download the artifact **prayer-counter-apk** (zip containing `app-debug.apk`). The offline HTML is also attached.
4. Send the APK on WhatsApp. Users install it after allowing "install unknown apps".

## B2. Build the APK on your own PC instead
Needs Node 20, JDK 17, Android SDK.
    python build_offline.py
    npm install
    npx cap add android
    python patch_manifest.py
    npx cap sync android
    cd android && ./gradlew assembleDebug      (Windows: gradlew.bat assembleDebug)
APK: `android/app/build/outputs/apk/debug/app-debug.apk`

Notes: the APK is debug-signed (fine for sharing, not for Google Play). Speech needs a TTS engine with Arabic/Indonesian voices installed on the phone.
