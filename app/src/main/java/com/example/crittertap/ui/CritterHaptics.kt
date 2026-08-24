package com.example.crittertap.ui

import android.content.Context
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager

/**
 * Two distinct buzzes, so a tap and a new critter do not feel the same.
 *
 * Compose's `LocalHapticFeedback` only offers a light tick, which is easy to
 * miss on a wrist — and for a small child the buzz is a large part of the
 * cause-and-effect the toy is teaching.
 */
class CritterHaptics(context: Context) {

    private val vibrator: Vibrator? = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        context.getSystemService(VibratorManager::class.java)?.defaultVibrator
    } else {
        @Suppress("DEPRECATION")
        context.getSystemService(Vibrator::class.java)
    }

    private val available = vibrator?.hasVibrator() == true

    /** A single firm click: the critter has been poked and is about to speak. */
    fun poke() {
        if (!available) return
        vibrator?.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK))
    }

    /** A double pulse: a different critter has arrived. */
    fun arrive() {
        if (!available) return
        vibrator?.vibrate(VibrationEffect.createWaveform(ARRIVAL_PATTERN, -1))
    }

    private companion object {
        /** wait, buzz, wait, buzz — in milliseconds */
        val ARRIVAL_PATTERN = longArrayOf(0, 28, 70, 46)
    }
}
