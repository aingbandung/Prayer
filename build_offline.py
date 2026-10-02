#!/usr/bin/env python3
"""Downloads the MediaPipe pieces ONCE and builds:
  dist/prayer-counter-offline.html  -> single self-contained file (~21 MB)
  www/                              -> index.html + vendor/ folder used by the APK
Needs only Python 3 and an internet connection for the first run."""
import base64, json, os, shutil, urllib.request

VER = "0.10.14"
CDN = f"https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@{VER}"
FILES = {  # local name -> url (the bundle is saved as .js so Android serves it with a JS mime type)
    "vision_bundle.js": f"{CDN}/vision_bundle.mjs",
    "vision_wasm_internal.js": f"{CDN}/wasm/vision_wasm_internal.js",
    "vision_wasm_internal.wasm": f"{CDN}/wasm/vision_wasm_internal.wasm",
    "pose_landmarker_lite.task": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
}
here = os.path.dirname(os.path.abspath(__file__))
cache = os.path.join(here, "vendor_cache")
os.makedirs(cache, exist_ok=True)

def get(name, url):
    path = os.path.join(cache, name)
    if not os.path.exists(path):
        print("downloading", name)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=180) as r, open(path, "wb") as f:
            shutil.copyfileobj(r, f)
    return path

paths = {n: get(n, u) for n, u in FILES.items()}
src = open(os.path.join(here, "prayer-counter.html"), encoding="utf-8").read()
MARK = '<script type="module">'
assert MARK in src, "prayer-counter.html not found / changed"
b64 = lambda n: base64.b64encode(open(paths[n], "rb").read()).decode()

# 1) single-file offline html
v = {"inline": True, "js": b64("vision_bundle.js"), "loader": b64("vision_wasm_internal.js"),
     "wasm": b64("vision_wasm_internal.wasm"), "model": b64("pose_landmarker_lite.task")}
os.makedirs(os.path.join(here, "dist"), exist_ok=True)
out = src.replace(MARK, "<script>window.PC_VENDOR=" + json.dumps(v) + ";</script>\n" + MARK, 1)
open(os.path.join(here, "dist", "prayer-counter-offline.html"), "w", encoding="utf-8").write(out)

# 2) www/ folder for the APK
www = os.path.join(here, "www"); vend = os.path.join(www, "vendor")
shutil.rmtree(www, ignore_errors=True); os.makedirs(vend)
for n in paths: shutil.copy(paths[n], os.path.join(vend, n))
out = src.replace(MARK, '<script>window.PC_VENDOR={"dir":"./vendor"};</script>\n' + MARK, 1)
open(os.path.join(www, "index.html"), "w", encoding="utf-8").write(out)
print("Done -> dist/prayer-counter-offline.html and www/")
