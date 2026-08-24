package com.example.crittertap.settings

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.example.crittertap.data.Language

/**
 * The two things the user can configure, kept in shared preferences so they
 * survive the watch killing the app.
 *
 * Backed by Compose state, so a screen reading [language] or [volume]
 * recomposes as soon as the settings screen changes it.
 */
class SettingsRepository(context: Context) {

    private val prefs = context.applicationContext
        .getSharedPreferences(FILE, Context.MODE_PRIVATE)

    var language by mutableStateOf(Language.fromTag(prefs.getString(KEY_LANGUAGE, null)))
        private set

    /** 0f is muted, 1f is the engine's own full volume. */
    var volume by mutableFloatStateOf(prefs.getFloat(KEY_VOLUME, DEFAULT_VOLUME))
        private set

    fun updateLanguage(value: Language) {
        language = value
        prefs.edit().putString(KEY_LANGUAGE, value.tag).apply()
    }

    fun updateVolume(value: Float) {
        val clamped = value.coerceIn(0f, 1f)
        volume = clamped
        prefs.edit().putFloat(KEY_VOLUME, clamped).apply()
    }

    fun nudgeVolume(delta: Float) = updateVolume(volume + delta)

    companion object {
        const val VOLUME_STEP = 0.1f
        private const val FILE = "critter_settings"
        private const val KEY_LANGUAGE = "language"
        private const val KEY_VOLUME = "volume"
        private const val DEFAULT_VOLUME = 0.9f
    }
}
