package com.example.crittertap.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavController
import androidx.wear.compose.navigation.SwipeDismissableNavHost
import androidx.wear.compose.navigation.composable
import androidx.wear.compose.navigation.rememberSwipeDismissableNavController
import com.example.crittertap.audio.CritterVoice
import com.example.crittertap.data.UiText
import com.example.crittertap.settings.SettingsRepository

object Routes {
    const val MENU = "menu"
    const val PLAY = "play"
    const val SETTINGS = "settings"
}

/**
 * Owns the voice and the settings for as long as the app is on screen, and
 * wires the three destinations together. Swiping right goes back, which is the
 * standard Wear OS gesture.
 *
 * Each destination reads `settings` and `voice` itself rather than being handed
 * values from out here: the navigation graph is built once, so anything read in
 * this scope and captured by a destination lambda would be frozen at whatever
 * it was on the first composition, and changing the language would leave the
 * screens in the old one.
 */
@Composable
fun CritterApp() {
    val context = LocalContext.current
    val settings = remember { SettingsRepository(context) }
    val voice = remember { CritterVoice(context) }
    val navController = rememberSwipeDismissableNavController()

    DisposableEffect(voice) {
        onDispose { voice.shutdown() }
    }
    LaunchedEffect(settings.language) { voice.setLanguage(settings.language) }
    LaunchedEffect(settings.volume) { voice.setVolume(settings.volume) }

    // Nothing should keep talking once the play screen is left.
    DisposableEffect(navController, voice) {
        val listener = NavController.OnDestinationChangedListener { _, destination, _ ->
            if (destination.route != Routes.PLAY) voice.stop()
        }
        navController.addOnDestinationChangedListener(listener)
        onDispose { navController.removeOnDestinationChangedListener(listener) }
    }

    SwipeDismissableNavHost(
        navController = navController,
        startDestination = Routes.MENU,
    ) {
        composable(Routes.MENU) {
            MenuScreen(
                strings = UiText.of(settings.language),
                onPlay = { navController.navigate(Routes.PLAY) },
                onSettings = { navController.navigate(Routes.SETTINGS) },
            )
        }
        composable(Routes.PLAY) {
            PlayScreen(
                language = settings.language,
                strings = UiText.of(settings.language),
                voiceStatus = voice.status,
                onCritterShown = voice::say,
            )
        }
        composable(Routes.SETTINGS) {
            SettingsScreen(
                strings = UiText.of(settings.language),
                language = settings.language,
                volume = settings.volume,
                missingVoiceFor = voice.missingVoiceFor,
                onLanguage = settings::updateLanguage,
                onVolume = settings::updateVolume,
            )
        }
    }
}
