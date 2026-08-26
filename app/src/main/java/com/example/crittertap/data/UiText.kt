package com.example.crittertap.data

/**
 * Every piece of on-screen wording, per language.
 *
 * These live in Kotlin rather than `strings.xml` because the language is chosen
 * inside the app rather than by the watch's system locale — the critter names
 * and descriptions have to switch with it, and keeping all of the text in one
 * place means a new language is one object, not a new resource folder plus a
 * parallel catalog.
 */
data class UiStrings(
    val appTitle: String,
    val play: String,
    val settings: String,
    val volume: String,
    val language: String,
    val muted: String,
    val tapHint: String,
    val doubleTapHint: String,
    val noVoice: String,
    val noAudio: String,
    val voiceMissing: String,
)

object UiText {

    private val english = UiStrings(
        appTitle = "Tap a Critter",
        play = "Play",
        settings = "Settings",
        volume = "Volume",
        language = "Language",
        muted = "Muted",
        tapHint = "Tap to hear",
        doubleTapHint = "Double tap for next",
        noVoice = "no voice engine",
        noAudio = "no speaker/headset",
        voiceMissing = "This watch has no English voice installed.",
    )

    private val spanish = UiStrings(
        appTitle = "Toca un Animal",
        play = "Jugar",
        settings = "Ajustes",
        volume = "Volumen",
        language = "Idioma",
        muted = "Silenciado",
        tapHint = "Toca para escuchar",
        doubleTapHint = "Doble toque: siguiente",
        noVoice = "sin motor de voz",
        noAudio = "sin altavoz/auriculares",
        voiceMissing = "Este reloj no tiene voz en español instalada.",
    )

    fun of(language: Language): UiStrings = when (language) {
        Language.ENGLISH -> english
        Language.SPANISH -> spanish
    }
}
