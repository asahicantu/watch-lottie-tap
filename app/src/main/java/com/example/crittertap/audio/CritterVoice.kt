package com.example.crittertap.audio

import android.content.Context
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.example.crittertap.data.Critter
import com.example.crittertap.data.CritterText
import com.example.crittertap.data.Language

/**
 * Says a critter out loud, in two parts: first the sentence describing it, then
 * the noise the animal makes. A short silence separates them so they do not run
 * together.
 *
 * Text-to-speech carries both parts by default, because it needs nothing
 * bundled and always matches the catalog in the chosen language. A critter with
 * a [Critter.soundRes] recording plays that instead of speaking the noise —
 * the description is still spoken first, and the recording starts when it ends.
 *
 * TTS initialises asynchronously, so a request made before the engine is ready
 * is held in [pending]. Watches with no TTS engine end up in
 * [Status.Unavailable]; the screen shows that rather than just going quiet.
 */
class CritterVoice(context: Context) {

    enum class Status { Starting, Ready, Unavailable }

    private val appContext = context.applicationContext
    private val main = Handler(Looper.getMainLooper())
    private var pending: Utterance? = null
    private var player: MediaPlayer? = null
    private var queuedRecording: Int? = null

    /** Observable so the UI can explain itself when the watch has no voice. */
    var status by mutableStateOf(Status.Starting)
        private set

    /** Set when the engine has no voice data for the language that was asked for. */
    var missingVoiceFor by mutableStateOf<Language?>(null)
        private set

    private var language = Language.ENGLISH
    private var volume = 1f

    private val speechAttributes = AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
        .build()

    private val tts = TextToSpeech(appContext) { initStatus ->
        if (initStatus == TextToSpeech.SUCCESS) {
            configureEngine()
            status = Status.Ready
            pending?.let { pending = null; say(it.critter, it.text) }
        } else {
            status = Status.Unavailable
            pending = null
            Log.w(TAG, "Text-to-speech unavailable (status=$initStatus); staying silent.")
        }
    }

    private data class Utterance(val critter: Critter, val text: CritterText)

    /**
     * Speaks [text] for [critter]: the description, a beat, then the noise.
     * Cuts off whatever was playing before.
     */
    fun say(critter: Critter, text: CritterText) {
        stop()
        if (volume <= 0f) return
        when (status) {
            Status.Starting -> pending = Utterance(critter, text)
            Status.Unavailable -> Unit
            Status.Ready -> {
                val params = Bundle().apply {
                    putFloat(TextToSpeech.Engine.KEY_PARAM_VOLUME, volume)
                }
                queuedRecording = critter.soundRes
                tts.speak(text.description, TextToSpeech.QUEUE_FLUSH, params, describeId(critter))
                if (critter.soundRes == null) {
                    tts.playSilentUtterance(GAP_MILLIS, TextToSpeech.QUEUE_ADD, gapId(critter))
                    tts.speak(text.noise, TextToSpeech.QUEUE_ADD, params, noiseId(critter))
                }
                // With a recording, onDone(describeId) starts the player instead.
            }
        }
    }

    /** Applies to both the spoken parts and any bundled recording. */
    fun setVolume(value: Float) {
        volume = value.coerceIn(0f, 1f)
        player?.setVolume(volume, volume)
    }

    fun setLanguage(value: Language) {
        language = value
        if (status == Status.Ready) applyLanguage()
    }

    fun stop() {
        queuedRecording = null
        if (status == Status.Ready) tts.stop()
        releasePlayer()
    }

    fun shutdown() {
        pending = null
        stop()
        tts.setOnUtteranceProgressListener(null)
        tts.shutdown()
        status = Status.Unavailable
    }

    private fun configureEngine() {
        tts.setAudioAttributes(speechAttributes)
        // A slightly slower, higher voice reads better for short animal noises.
        tts.setSpeechRate(0.95f)
        tts.setPitch(1.15f)
        applyLanguage()
        tts.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) = Unit

            override fun onDone(utteranceId: String?) {
                val sound = queuedRecording ?: return
                if (utteranceId?.endsWith(DESCRIBE_SUFFIX) != true) return
                queuedRecording = null
                main.post { playRecording(sound) }
            }

            @Deprecated("Required by the base class", ReplaceWith(""))
            override fun onError(utteranceId: String?) = Unit
        })
    }

    private fun applyLanguage() {
        val result = tts.setLanguage(language.locale)
        val missing = result == TextToSpeech.LANG_MISSING_DATA ||
            result == TextToSpeech.LANG_NOT_SUPPORTED
        missingVoiceFor = if (missing) language else null
        if (missing) {
            Log.w(TAG, "No voice data for ${language.tag}; the watch will read it with " +
                "whatever voice it has.")
        }
    }

    private fun playRecording(resId: Int) {
        releasePlayer()
        player = MediaPlayer.create(appContext, resId)?.apply {
            setVolume(volume, volume)
            setOnCompletionListener { releasePlayer() }
            start()
        }
    }

    private fun releasePlayer() {
        player?.run {
            if (isPlaying) stop()
            release()
        }
        player = null
    }

    private fun describeId(critter: Critter) = "${critter.id}$DESCRIBE_SUFFIX"
    private fun gapId(critter: Critter) = "${critter.id}-gap"
    private fun noiseId(critter: Critter) = "${critter.id}-noise"

    private companion object {
        const val TAG = "CritterVoice"
        const val GAP_MILLIS = 280L
        const val DESCRIBE_SUFFIX = "-describe"
    }
}
