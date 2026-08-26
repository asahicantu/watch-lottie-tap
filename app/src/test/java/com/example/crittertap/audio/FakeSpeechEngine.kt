package com.example.crittertap.audio

import java.util.Locale

/** Records what was asked of it, and lets a test drive engine start-up by hand. */
class FakeSpeechEngine(
    /** Locales this pretend watch has voice data for; null means all of them. */
    private val supported: Set<String>? = null,
) : SpeechEngine {

    sealed interface Call {
        data class Speak(
            val text: String,
            val volume: Float,
            val utteranceId: String,
            val flush: Boolean,
        ) : Call

        data class Silence(val millis: Long, val utteranceId: String) : Call
        data object Stop : Call
        data object Shutdown : Call
    }

    val calls = mutableListOf<Call>()
    val languages = mutableListOf<Locale>()
    var started = false
        private set

    private var onReady: ((SpeechEngine.Readiness) -> Unit)? = null
    private var doneListener: ((String) -> Unit)? = null

    /** The spoken text in order, ignoring gaps and stops. */
    val spoken: List<String>
        get() = calls.filterIsInstance<Call.Speak>().map { it.text }

    override fun start(onReady: (SpeechEngine.Readiness) -> Unit) {
        started = true
        this.onReady = onReady
    }

    /** Completes start-up. Nothing is spoken until this is called. */
    fun becomeReady(ready: Boolean = true) {
        onReady?.invoke(if (ready) SpeechEngine.Readiness.Ready else SpeechEngine.Readiness.NoEngine)
    }

    override fun speak(text: String, volume: Float, utteranceId: String, flush: Boolean) {
        calls += Call.Speak(text, volume, utteranceId, flush)
    }

    override fun silence(millis: Long, utteranceId: String) {
        calls += Call.Silence(millis, utteranceId)
    }

    override fun setLanguage(locale: Locale): Boolean {
        languages += locale
        return supported == null || locale.toLanguageTag() in supported
    }

    override fun onUtteranceDone(listener: (String) -> Unit) {
        doneListener = listener
    }

    /** Pretends the given utterance finished playing. */
    fun finish(utteranceId: String) {
        doneListener?.invoke(utteranceId)
    }

    override fun stop() {
        calls += Call.Stop
    }

    override fun shutdown() {
        calls += Call.Shutdown
    }
}

/** Records playback requests for bundled recordings. */
class FakeSoundPlayer : SoundPlayer {
    val played = mutableListOf<Pair<Int, Float>>()
    var stops = 0
        private set
    var volume = 1f
        private set

    override fun play(resId: Int, volume: Float) {
        played += resId to volume
    }

    override fun setVolume(volume: Float) {
        this.volume = volume
    }

    override fun stop() {
        stops++
    }
}
