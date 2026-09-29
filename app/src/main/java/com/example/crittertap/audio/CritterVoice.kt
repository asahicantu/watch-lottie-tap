package com.example.crittertap.audio

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.example.crittertap.data.Critter
import com.example.crittertap.data.CritterText
import com.example.crittertap.data.Language

/**
 * Decides *what* to say and in what order; [SpeechEngine] decides how.
 *
 * A critter's first appearance calls for [say]: the sentence describing it,
 * then the noise it makes, with a short silence between them so they do not
 * run together. A critter carrying a [Critter.soundRes] recording gets the
 * recording in place of the spoken noise, started when the description ends.
 *
 * Once it is already on screen, a further tap calls for [replay] instead —
 * the critter's name, then its noise, without repeating the description.
 *
 * Engines initialise asynchronously, so a request made before one is ready is
 * held in [pending]. Watches with no engine at all end up in
 * [Status.NoEngine] and the screen says so; a [Critter.soundRes] recording
 * needs no engine, though, so it still plays even then.
 *
 * Deliberately free of `android.*` imports: the sequencing is the part worth
 * testing, and the emulator cannot speak.
 */
class CritterVoice(
    private val engine: SpeechEngine,
    private val player: SoundPlayer,
) {

    enum class Status { Starting, Ready, NoEngine, NoAudioOutput }

    /** Observable so the UI can explain itself when the watch has no voice. */
    var status by mutableStateOf(Status.Starting)
        private set

    /** Set when the engine has no voice data for the language that was asked for. */
    var missingVoiceFor by mutableStateOf<Language?>(null)
        private set

    private var pending: Utterance? = null
    private var queuedRecording: Int? = null
    private var language = Language.ENGLISH
    private var volume = 1f
    private var speakLabelOnly = false

    private data class Utterance(val critter: Critter, val text: CritterText, val nameOnly: Boolean)

    init {
        engine.onUtteranceDone(::onUtteranceDone)
        engine.start { readiness ->
            status = when (readiness) {
                SpeechEngine.Readiness.Ready -> Status.Ready
                SpeechEngine.Readiness.NoEngine -> Status.NoEngine
                SpeechEngine.Readiness.NoAudioOutput -> Status.NoAudioOutput
            }
            if (status == Status.Ready) applyLanguage()
            pending?.let {
                pending = null
                if (it.nameOnly) replay(it.critter, it.text) else say(it.critter, it.text)
            }
        }
    }

    /**
     * Says [text] for [critter]: the description, a beat, then the noise.
     * Cuts off whatever was playing before.
     */
    fun say(critter: Critter, text: CritterText) {
        stop()
        if (volume <= 0f) return
        when (status) {
            Status.Starting -> pending = Utterance(critter, text, nameOnly = false)
            // No text-to-speech engine (the emulator, some watches) means the
            // description can't be spoken, but a bundled recording needs no
            // engine at all and can still play.
            Status.NoEngine, Status.NoAudioOutput -> critter.soundRes?.let { player.play(it, volume) }
            Status.Ready -> {
                queuedRecording = critter.soundRes
                val introText = if (speakLabelOnly) text.label else text.description
                engine.speak(introText, volume, describeId(critter), flush = true)
                if (critter.soundRes == null) {
                    engine.silence(GAP_MILLIS, gapId(critter))
                    engine.speak(text.noise, volume, noiseId(critter), flush = false)
                }
                // With a recording, the description finishing starts the player.
            }
        }
    }

    /**
     * Says [critter]'s name, then its noise — no description. For a critter
     * already on screen, a tap should name it again without repeating the
     * whole introduction.
     *
     * The name needs an engine; a bundled recording does not, so with no
     * engine the recording still plays on its own, and a spoken-noise critter
     * stays quiet.
     */
    fun replay(critter: Critter, text: CritterText) {
        stop()
        if (volume <= 0f) return
        when (status) {
            Status.Starting -> pending = Utterance(critter, text, nameOnly = true)
            Status.NoEngine, Status.NoAudioOutput -> critter.soundRes?.let { player.play(it, volume) }
            Status.Ready -> {
                queuedRecording = critter.soundRes
                engine.speak(text.label, volume, nameId(critter), flush = true)
                if (critter.soundRes == null) {
                    engine.silence(GAP_MILLIS, gapId(critter))
                    engine.speak(text.noise, volume, noiseId(critter), flush = false)
                }
                // With a recording, the name finishing starts the player.
            }
        }
    }

    /** Applies to both the spoken parts and any bundled recording. */
    fun setVolume(value: Float) {
        volume = value.coerceIn(0f, 1f)
        player.setVolume(volume)
    }

    fun setLanguage(value: Language) {
        language = value
        if (status == Status.Ready) applyLanguage()
    }

    fun setSpeakLabelOnly(value: Boolean) {
        speakLabelOnly = value
    }

    fun stop() {
        queuedRecording = null
        if (status == Status.Ready) engine.stop()
        player.stop()
    }

    fun shutdown() {
        pending = null
        stop()
        engine.shutdown()
        status = Status.NoEngine
    }

    private fun onUtteranceDone(utteranceId: String) {
        val sound = queuedRecording ?: return
        if (!utteranceId.endsWith(DESCRIBE_SUFFIX) && !utteranceId.endsWith(NAME_SUFFIX)) return
        queuedRecording = null
        player.play(sound, volume)
    }

    private fun applyLanguage() {
        missingVoiceFor = if (engine.setLanguage(language.locale)) null else language
    }

    private fun describeId(critter: Critter) = "${critter.id}$DESCRIBE_SUFFIX"
    private fun nameId(critter: Critter) = "${critter.id}$NAME_SUFFIX"
    private fun gapId(critter: Critter) = "${critter.id}-gap"
    private fun noiseId(critter: Critter) = "${critter.id}-noise"

    companion object {
        const val GAP_MILLIS = 280L
        const val DESCRIBE_SUFFIX = "-describe"
        const val NAME_SUFFIX = "-name"
    }
}
