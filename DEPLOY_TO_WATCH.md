# Deploying to a physical Galaxy Watch without a Wi-Fi network

Galaxy Watches have no USB port, so normal USB debugging is out. **Bluetooth
debugging was removed starting with Wear OS 3** (the version Galaxy Watch4
and later run), so that option won't appear in Developer options no matter
how carefully you look — it's not a hidden menu, it's gone.

The only remaining wireless path is **Wi-Fi debugging with a pairing code**
(the same mechanism modern Android phones use). It genuinely requires *some*
Wi-Fi network, but that network doesn't have to be a real router — a phone's
personal hotspot works fine and is the standard workaround when no other
Wi-Fi is available (Google's own docs recommend this for enterprise networks
with access-point isolation too).

The only way to avoid Wi-Fi entirely is a USB-capable charging cradle/dock
with data support — a special developer accessory, not the standard
wireless charging puck most people have.

## What you need

- ADB version 30.0.0 or higher.
- Any Wi-Fi network reachable by both the watch and your PC — including a
  phone's personal hotspot if no other network is available.

## Steps

### 1. Enable wireless debugging on the watch

1. Enable Developer options if you haven't: Settings → About watch → tap
   "Software version" repeatedly until it unlocks.
2. Settings → **Developer options** → enable **ADB debugging**.
3. Enable **Wireless debugging** → confirm **Allow** / **Always allow on
   this network**.

### 2. Pair your computer with the watch (one-time only)

1. On the watch: Settings → Developer options → Wireless debugging →
   **Pair new device**.
2. Note the three values shown: **Wi-Fi pairing code**, **IP address**, and
   **pairing port**.
3. On your computer:

   ```
   adb pair ip-address:pairing-port
   ```

4. Enter the Wi-Fi pairing code when prompted. Look for
   `Successfully paired to ip-address:pairing-port`.

### 3. Connect to the watch (required each session)

1. On the watch: Settings → Developer options → Wireless debugging — this
   time read the IP address and **connection port** from the main screen
   (not "Pair new device"; the connection port differs from the pairing
   port).
2. On your computer:

   ```
   adb connect ip-address:connection-port
   adb devices
   ```

   The watch should now show up in the device list.

### 4. Deploy the app

Either pick the watch as the run target in Android Studio, or from the
command line:

```
./gradlew.bat installDebug
```

## Troubleshooting

- **Can't connect at all:** confirm the watch and PC are truly on the same
  Wi-Fi network and that peer-to-peer traffic isn't blocked (this is why
  corporate/guest networks often fail — use a phone hotspot instead).
- **Stuck/flaky connection:** `adb kill-server` then `adb start-server`, or
  toggle Wireless debugging off and back on on the watch.
- **Multiple devices connected:** prefix commands with
  `adb -s ip-address:connection-port`.

## Sources

- [Debug a Wear OS app — Android Developers](https://developer.android.com/training/wearables/get-started/debugging)
- [Debug Wear OS over Wi-Fi — Android Developers](https://developer.android.com/training/wearables/get-started/debug-wifi)
