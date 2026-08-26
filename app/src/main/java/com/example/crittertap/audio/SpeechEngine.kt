package com.example.crittertap.audio

import java.util.Locale

/**
 * The slice of a text-to-speech engine that [CritterVoice] needs.
 *
 * Pulling this out of [CritterVoice] is what makes the speaking *sequence*
 * testable without a device: the Wear emulator ships no TTS engine at all, so
 * the order of "description, pause, noise" could otherwise only be checked by
 * listening to a real watch.
 */
interface SpeechEngine {

    /** Readiness state of the engine. */
    enum class Readiness { Ready, NoEngine, NoAudioOutput }

    /** Starts the engine. [onReady] provides the readiness state. */
    fun start(onReady: (readiness: Readiness) -> Unit)

    /** @param flush true replaces anything already queued, false appends to it. */
    fun speak(text: String, volume: Float, utteranceId: String, flush: Boolean)

    /** Queues a gap so the description and the noise do not run together. */
    fun silence(millis: Long, utteranceId: String)

    /** Returns false when the engine has no voice data for [locale]. */
    fun setLanguage(locale: Locale): Boolean

    /** Registers the callback fired with each utterance id as it finishes. */
    fun onUtteranceDone(listener: (utteranceId: String) -> Unit)

    fun stop()

    fun shutdown()
}

/** Plays a bundled recording in place of the spoken noise. */
interface SoundPlayer {
    fun play(resId: Int, volume: Float)
    fun setVolume(volume: Float)
    fun stop()
}
