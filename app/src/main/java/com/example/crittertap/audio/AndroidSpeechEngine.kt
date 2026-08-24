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
import java.util.Locale

/** [SpeechEngine] backed by the watch's own text-to-speech engine. */
class AndroidSpeechEngine(context: Context) : SpeechEngine {

    private val appContext = context.applicationContext
    private var tts: TextToSpeech? = null
    private var doneListener: ((String) -> Unit)? = null

    private val speechAttributes = AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
        .build()

    override fun start(onReady: (Boolean) -> Unit) {
        tts = TextToSpeech(appContext) { status ->
            val ready = status == TextToSpeech.SUCCESS
            if (ready) {
                configure()
            } else {
                Log.w(TAG, "Text-to-speech unavailable (status=$status); staying silent.")
            }
            onReady(ready)
        }
    }

    override fun speak(text: String, volume: Float, utteranceId: String, flush: Boolean) {
        val params = Bundle().apply {
            putFloat(TextToSpeech.Engine.KEY_PARAM_VOLUME, volume)
        }
        val mode = if (flush) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
        tts?.speak(text, mode, params, utteranceId)
    }

    override fun silence(millis: Long, utteranceId: String) {
        tts?.playSilentUtterance(millis, TextToSpeech.QUEUE_ADD, utteranceId)
    }

    override fun setLanguage(locale: Locale): Boolean {
        val result = tts?.setLanguage(locale) ?: return false
        val missing = result == TextToSpeech.LANG_MISSING_DATA ||
            result == TextToSpeech.LANG_NOT_SUPPORTED
        if (missing) {
            Log.w(TAG, "No voice data for $locale; falling back to the default voice.")
            tts?.setLanguage(Locale.getDefault())
        }
        return !missing
    }

    override fun onUtteranceDone(listener: (String) -> Unit) {
        doneListener = listener
    }

    override fun stop() {
        tts?.stop()
    }

    override fun shutdown() {
        tts?.setOnUtteranceProgressListener(null)
        tts?.stop()
        tts?.shutdown()
        tts = null
        doneListener = null
    }

    private fun configure() {
        tts?.apply {
            setAudioAttributes(speechAttributes)
            // A slightly slower, higher voice reads better for short animal noises.
            setSpeechRate(0.95f)
            setPitch(1.15f)
            setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(utteranceId: String?) = Unit

                override fun onDone(utteranceId: String?) {
                    utteranceId?.let { id -> doneListener?.invoke(id) }
                }

                @Deprecated("Required by the base class", ReplaceWith(""))
                override fun onError(utteranceId: String?) = Unit
            })
        }
    }

    private companion object {
        const val TAG = "AndroidSpeechEngine"
    }
}

/** [SoundPlayer] backed by MediaPlayer, kept on the main thread. */
class AndroidSoundPlayer(context: Context) : SoundPlayer {

    private val appContext = context.applicationContext
    private val main = Handler(Looper.getMainLooper())
    private var player: MediaPlayer? = null
    private var volume = 1f

    override fun play(resId: Int, volume: Float) {
        this.volume = volume
        main.post {
            stop()
            player = MediaPlayer.create(appContext, resId)?.apply {
                setVolume(volume, volume)
                setOnCompletionListener { stop() }
                start()
            }
        }
    }

    override fun setVolume(volume: Float) {
        this.volume = volume
        player?.setVolume(volume, volume)
    }

    override fun stop() {
        player?.run {
            if (isPlaying) stop()
            release()
        }
        player = null
    }
}
