# Implementation Plan - Enhancing Human Readability and Editability

This plan outlines improvements to the **CritterTap** Wear OS application to make it more human-readable, editable, and easy to onboard. The focus is on architectural cleanup, standardizing theming, and improving accessibility.

## User Review Required

> [!IMPORTANT]
> This plan introduces **ViewModels** to manage UI state. This is a standard Android practice that separates business logic from UI components, making the code easier to test and maintain.

> [!NOTE]
> I will keep the current Kotlin-based localization system (`CritterTexts`) as it allows for in-app language switching without complex context wrapping, but I will clean up its structure and move hardcoded colors into the theme.

## Proposed Changes

### Architecture & State Management

#### [NEW] [PlayViewModel.kt](file:///C:/Users/NOACA3/src/misc/watch-lottie-tap/app/src/main/java/com/example/crittertap/ui/PlayViewModel.kt)
- Move `CritterShuffler` management and current index logic here.
- Expose state via `StateFlow` for better testability and lifecycle management.

#### [MODIFY] [PlayScreen.kt](file:///C:/Users/NOACA3/src/misc/watch-lottie-tap/app/src/main/java/com/example/crittertap/ui/PlayScreen.kt)
- Connect to `PlayViewModel`.
- Move gesture-triggered logic (speak, show next) to the ViewModel.
- Remove `rememberSaveable` for `deck` and `index` from the Composable.

#### [MODIFY] [CritterApp.kt](file:///C:/Users/NOACA3/src/misc/watch-lottie-tap/app/src/main/java/com/example/crittertap/ui/CritterApp.kt)
- Clean up the instantiation of `SettingsRepository` and `CritterVoice`.
- Provide the ViewModel to `PlayScreen`.

### Theming & Styling

#### [MODIFY] [Theme.kt](file:///C:/Users/NOACA3/src/misc/watch-lottie-tap/app/src/main/java/com/example/crittertap/ui/theme/Theme.kt)
- Define critter-related colors and standard text colors here.
- Replace hardcoded hex values in `PlayScreen.kt` with theme references.

#### [MODIFY] [CritterCatalog.kt](file:///C:/Users/NOACA3/src/misc/watch-lottie-tap/app/src/main/java/com/example/crittertap/data/CritterCatalog.kt)
- Review the `accent` color management to ensure it integrates well with the theme.

### Accessibility & Documentation

#### [MODIFY] [PlayScreen.kt](file:///C:/Users/NOACA3/src/misc/watch-lottie-tap/app/src/main/java/com/example/crittertap/ui/PlayScreen.kt)
- Add `contentDescription` to the `LottieAnimation` to support TalkBack.
- Use the animal's name and description as the accessibility text.

#### [MODIFY] All key files
- Add missing KDoc for classes and public methods to improve onboarding for new developers.

## Verification Plan

### Automated Tests
- Run `PlayScreenTest.kt` to ensure gestures and navigation still work correctly.
- Add unit tests for the new `PlayViewModel`.

### Manual Verification
- Deploy to a Wear OS emulator/device.
- Verify that tapping and double-tapping behave as expected.
- Verify that rotary input still works.
- Check accessibility by enabling TalkBack and ensuring critters are described correctly.
