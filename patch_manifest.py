# adds camera permission (+ text-to-speech visibility) to the generated Android project
p = "android/app/src/main/AndroidManifest.xml"
s = open(p, encoding="utf-8").read()
if "android.permission.CAMERA" not in s:
    s = s.replace("<application", """<uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <queries><intent><action android:name="android.intent.action.TTS_SERVICE" /></intent></queries>
    <application""", 1)
    open(p, "w", encoding="utf-8").write(s)
print("manifest patched")
