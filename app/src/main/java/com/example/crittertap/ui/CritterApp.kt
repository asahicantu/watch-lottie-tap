package com.example.crittertap.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import androidx.wear.compose.navigation.SwipeDismissableNavHost
import androidx.wear.compose.navigation.composable
import androidx.wear.compose.navigation.rememberSwipeDismissableNavController
import com.example.crittertap.audio.AndroidSoundPlayer
import com.example.crittertap.audio.AndroidSpeechEngine
import com.example.crittertap.audio.CritterVoice
import com.example.crittertap.data.UiText
import com.example.crittertap.settings.SettingsRepository

object Routes {
    const val MENU = "menu"
    const val PLAY = "play"
    const val SETTINGS = "settings"
}

/**
 * The root Composable for the CritterTap application.
 *
 * It manages the app's navigation, central settings, and voice engine lifecycle.
 */
@Composable
fun CritterApp() {
    val context = LocalContext.current
    val settings = remember { SettingsRepository(context) }
    val voice = remember {
        CritterVoice(AndroidSpeechEngine(context), AndroidSoundPlayer(context))
    }
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
            val playViewModel: PlayViewModel = viewModel(factory = PlayViewModel.Factory)
            PlayScreen(
                language = settings.language,
                strings = UiText.of(settings.language),
                voiceStatus = voice.status,
                onCritterShown = voice::say,
                onCritterPoked = voice::replay,
                viewModel = playViewModel
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
