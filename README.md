# Tap a Critter — a Lottie toy for Wear OS

A standalone Wear OS app for Samsung Galaxy Watch. It plays a Lottie animation
in the middle of the screen and speaks it aloud: first a sentence describing the
animal, then the noise the animal makes. **Thirty** critters, in **English** or
**Spanish**.

## Screens

| Screen | What it does |
| --- | --- |
| **Menu** | Play, or Settings. Swipe right anywhere to come back here. |
| **Play** | The toy itself. |
| **Settings** | Volume (0–100% in 10% steps) and language. Both persist. |

## Gestures on the play screen

| Gesture | What happens |
| --- | --- |
| **Single tap** | Speaks the description ("A fox. It is clever and very quick.") then the noise ("Yip! Yip!") |
| **Double tap** | Deals the next critter from a shuffled round and introduces it |
| **Rotating bezel / crown** | Steps through the catalog in order |

Every touch also presses the critter in and springs it back, throws a ring of
stars outwards, and buzzes — a single firm click for a tap, a double pulse when
a new critter arrives. Without that, the only feedback is a sound, which a small
child may not connect to their own finger.

A single tap waits out the system double-tap timeout (~300 ms) before it fires;
that is what makes the two gestures distinguishable and is normal for any
double-tap UI. It is also the main reason this is a toy for a child who can
already tap deliberately — reliable double-tapping is usually a 4-to-5-year-old
skill, not a 2-year-old one.

### How the next critter is picked

Not by rolling a die. Uniform random feels wrong in practice — a child meets the
cat three times in a dozen taps and never meets the giraffe. [`CritterShuffler`]
deals from a shuffled deck instead: **a round is every critter exactly once**,
and only when the round runs out is a new one shuffled. The card that opens a
new round is swapped if it would repeat the one that closed the last, so a
double tap never appears to do nothing. Browsing with the bezel marks that
critter as dealt too, so the round stays honest.

[`CritterShuffler`]: app/src/main/java/com/example/crittertap/data/CritterShuffler.kt

## The critters

cat · dog · cow · duck · frog · lion · bee · sheep · owl · pig · horse ·
elephant · monkey · penguin · tiger · bear · rabbit · mouse · fox · wolf ·
rooster · goat · donkey · panda · koala · giraffe · hippo · crocodile · snake ·
parrot

---

## Requirements

* JDK 17+ (built against the Microsoft OpenJDK 21 on this machine)
* Android SDK with **platform 36** installed (`compileSdk = 36`)
* A Galaxy Watch 4 or newer (`minSdk = 30`, Wear OS 3+), or the
  `Wear_OS_Large_Round` emulator

`local.properties` already points at `C:/Users/NOACA3/AppData/Local/Android/Sdk`.

## Build

```bash
./gradlew :app:assembleDebug
```

The debug APK lands in `app/build/outputs/apk/debug/app-debug.apk`. It is ~37 MB
because debug builds skip R8; the minified release APK is **2.3 MB**:

```bash
./gradlew :app:assembleRelease
```

Release is unsigned — add a `signingConfigs` block with your own keystore before
distributing it.

```bash
./gradlew :app:testDebugUnitTest
```

The gesture tests need a running watch emulator or a connected watch:

```bash
./gradlew :app:connectedDebugAndroidTest
```

## Run on the emulator

```bash
"$ANDROID_HOME/emulator/emulator" -avd Wear_OS_Large_Round
```

```bash
./gradlew :app:installDebug
```

Note: the Wear OS emulator image has **no text-to-speech engine installed**, so
the app runs silently there and shows a small `no voice engine` note at the top
of the play screen. That note does not appear on a real Galaxy Watch, which
ships with Samsung/Google TTS.

## Install on the Galaxy Watch

1. On the watch: **Settings → About watch → Software → Build number**, tap it 7
   times to unlock developer options.
2. **Settings → Developer options → ADB debugging → on**, then
   **Wireless debugging → on**.
3. Wear OS 4/5 (Galaxy Watch 5 and newer) uses pairing codes — tap
   **Pair new device** on the watch and run:

   ```bash
   adb pair <watch-ip>:<pairing-port>
   ```

   Wear OS 3 (Galaxy Watch 4) skips this step.
4. Connect and install:

   ```bash
   adb connect <watch-ip>:<debug-port>
   ```

   ```bash
   adb -s <watch-ip>:<debug-port> install -r app/build/outputs/apk/debug/app-debug.apk
   ```

IP and ports are shown on the watch's Wireless debugging screen. Keep the watch
on its charger and on the same Wi-Fi as the PC.

---

## Adding a critter

1. Drop `<id>.json` into `app/src/main/assets/animations/` (or add
   `tools/critters/<id>.py` defining a function of the same name, and
   regenerate — see *Where the animations come from*).
2. Add one line to `CritterCatalog` with the id and an accent colour:

   ```kotlin
   // app/src/main/java/com/example/crittertap/data/CritterCatalog.kt
   critter("otter", 0xFF8A6446),
   ```

3. Add the wording to **both** language maps in `CritterTexts`:

   ```kotlin
   "otter" to CritterText("Otter", "An otter. It floats on its back.", "Chirp! Chirp!"),
   ```

`CritterTextTest` fails if any language is missing an entry, if a Spanish
description is a copy of the English one, or if two critters share a label — so
a half-finished addition will not slip through.

## Adding a language

1. Add a case to `Language` with its BCP-47 tag.
2. Add a `UiStrings` block to `UiText` — the ten on-screen phrases.
3. Add a map to `CritterTexts` — all thirty critters.

The wording lives in Kotlin rather than `strings.xml` on purpose: the language
is chosen **inside the app**, not by the watch's system locale, and the critter
names have to switch with it. One object per language keeps the UI text and the
catalog text together, and the tests can then check them for gaps.

Whether the watch actually *speaks* a new language depends on its TTS engine
having that voice. If it does not, the settings screen says so instead of
silently reading Spanish with an English voice.

## Where the animations come from

They are **generated**, not downloaded, so there are no third-party licence
strings attached to them:

```bash
python tools/gen_critters.py
```

```
tools/lottie_kit.py       Bodymovin JSON primitives — ellipses, rects, bezier
                          paths, fills, strokes, animated transforms
tools/lottie_bounds.py    measures the built geometry so each critter can be
                          scaled and centred to a common size
tools/critter_parts.py    shared features — the idle bob, blinking eyes,
                          wiggling ears, slit pupils, teeth, tufts
tools/critters/<name>.py  one file per animal, named after it: gorilla.py
                          defines gorilla(). Adding a file is all it takes
                          to add an animal — nothing registers it anywhere
tools/gen_critters.py     the runner
tools/live_preview.py     the edit loop: rebuilds the animal you are editing
                          and pushes it to the browser as you save it
```

While working on an animal, run the live preview instead of regenerating by
hand:

```bash
python tools/live_preview.py          # opens on the animal you edited last
```

It watches `tools/critters/*.py`, rebuilds in ~30 ms on save, switches the page
to whichever animal you are editing, and shows the traceback in the page
instead of dying if the file does not compile.

Each animation is 300×300, 30 fps, 3 s, one shape layer, no image assets, no
expressions, no fonts — the subset that renders fastest on a watch. All thirty
together come to about 500 kB.

`critter()` measures the finished geometry with `tools/lottie_bounds.py` and
applies one corrective scale-and-offset, so every critter ends up exactly 272
units across its longer axis and centred on the canvas. Without it, hand-placed
features drift outside the canvas and get clipped — the rabbit's ears used to
overflow the top by 70 units — and an elephant would arrive on screen nearly
twice the size of a parrot.

To preview them in a browser while iterating:

```bash
python -m http.server 8099
```

then open `http://127.0.0.1:8099/tools/preview/index.html`.

**Using files from lottiefiles.com instead** works the same way: download the
`.json`, drop it in `assets/animations/`, add the catalog line. Prefer
shape-only animations — image assets, masks and mattes are heavier on a watch —
and check each file's licence before shipping it.

## Sound

`CritterVoice` speaks in two parts: the description, a 280 ms silence, then the
noise. Nothing is bundled, so the words always match the catalog and the chosen
language.

It talks to a `SpeechEngine` interface rather than to `TextToSpeech` directly.
That split exists because **the Wear emulator ships no text-to-speech engine at
all**, so the order of the two parts, the volume, the language switch and the
recording hand-off cannot be confirmed by listening — `CritterVoiceTest` drives
a fake engine and asserts them instead.

To use real recordings instead, put them in `app/src/main/res/raw/` and point
the catalog entry at one:

```kotlin
Critter(id = "cat", …, soundRes = R.raw.cat)
```

The description is still spoken first; the recording starts when it finishes,
in place of the spoken noise. Volume from the settings screen applies to both.

## Layout

```
app/src/main/
  assets/animations/*.json           the thirty Lottie files
  java/com/example/crittertap/
    MainActivity.kt                  keeps the screen awake, sets the content
    ui/CritterApp.kt                 the three destinations and swipe-back
    ui/MenuScreen.kt                 play / settings
    ui/PlayScreen.kt                 tap, double tap, rotary, and the animation
    ui/SettingsScreen.kt             volume and language
    ui/theme/Theme.kt                black-background Wear Material 3 theme
    data/Critter.kt                  id, asset, accent colour, optional recording
    data/CritterCatalog.kt           the list of thirty
    data/CritterShuffler.kt          the shuffled deck that deals them
    data/CritterText.kt              label / description / noise, per language
    data/Language.kt                 English, Spanish
    data/UiText.kt                   on-screen wording, per language
    settings/SettingsRepository.kt   volume + language, in shared preferences
    audio/CritterVoice.kt            what to say and in what order (no android.*)
    audio/SpeechEngine.kt            the engine + player interfaces it talks to
    audio/AndroidSpeechEngine.kt     TextToSpeech and MediaPlayer behind them
    ui/CritterHaptics.kt             the two buzzes
    ui/SparkleBurst.kt               the stars thrown on each touch
app/src/test/…                       catalog, translations, speech sequencing
app/src/androidTest/…                what the two gestures mean
```
