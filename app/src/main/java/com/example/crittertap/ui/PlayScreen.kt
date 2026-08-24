package com.example.crittertap.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.focusable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.rotary.onRotaryScrollEvent
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.wear.compose.material3.MaterialTheme
import androidx.wear.compose.material3.Text
import androidx.wear.tooling.preview.devices.WearDevices
import com.airbnb.lottie.compose.LottieAnimation
import com.airbnb.lottie.compose.LottieCompositionSpec
import com.airbnb.lottie.compose.LottieConstants
import com.airbnb.lottie.compose.animateLottieCompositionAsState
import com.airbnb.lottie.compose.rememberLottieComposition
import com.example.crittertap.audio.CritterVoice
import com.example.crittertap.data.Critter
import com.example.crittertap.data.CritterCatalog
import com.example.crittertap.data.CritterText
import com.example.crittertap.data.CritterTexts
import com.example.crittertap.data.Language
import com.example.crittertap.data.UiStrings
import com.example.crittertap.data.UiText
import com.example.crittertap.ui.theme.CritterTapTheme
import kotlin.math.roundToInt

private const val ROTARY_STEP_PIXELS = 90f

/**
 * Width of the animation as a fraction of the screen. Sized so that, centred, it
 * still clears the name underneath on the smallest round Wear screen (396 px)
 * as well as the 454 px one.
 */
private const val ANIMATION_FRACTION = 0.52f
private val HINT_LINE_HEIGHT = 22.dp

/**
 * The toy itself.
 *
 * * **Tap** — says the critter's description, then the noise it makes.
 * * **Double tap** — brings on the next critter (and introduces it).
 * * **Rotating bezel / crown** — steps through the catalog in order.
 */
@OptIn(ExperimentalComposeUiApi::class)
@Composable
fun PlayScreen(
    language: Language,
    strings: UiStrings,
    onCritterShown: (Critter, CritterText) -> Unit,
    modifier: Modifier = Modifier,
    voiceStatus: CritterVoice.Status = CritterVoice.Status.Ready,
) {
    val critters = CritterCatalog.all
    var index by rememberSaveable { mutableIntStateOf(CritterCatalog.nextIndex(-1)) }
    var interactions by rememberSaveable { mutableIntStateOf(0) }
    val critter = critters[index]
    val text = CritterTexts.of(critter.id, language)

    val haptics = LocalHapticFeedback.current
    val focusRequester = remember { FocusRequester() }
    var rotaryAccumulator by remember { mutableFloatStateOf(0f) }

    fun speak() {
        interactions++
        haptics.performHapticFeedback(HapticFeedbackType.LongPress)
        onCritterShown(critter, text)
    }

    fun show(next: Int) {
        index = next
        interactions++
        haptics.performHapticFeedback(HapticFeedbackType.LongPress)
        onCritterShown(critters[next], CritterTexts.of(critters[next].id, language))
    }

    // Introduce whatever is on screen when the player arrives, and again if the
    // language changes underneath them.
    LaunchedEffect(language) {
        onCritterShown(critter, CritterTexts.of(critter.id, language))
        runCatching { focusRequester.requestFocus() }
    }

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Color.Black)
            .onRotaryScrollEvent { event ->
                rotaryAccumulator += event.verticalScrollPixels
                val steps = (rotaryAccumulator / ROTARY_STEP_PIXELS).roundToInt()
                if (steps != 0) {
                    rotaryAccumulator -= steps * ROTARY_STEP_PIXELS
                    val size = critters.size
                    show(((index + steps) % size + size) % size)
                }
                true
            }
            .focusRequester(focusRequester)
            .focusable()
            .pointerInput(critters, language) {
                detectTapGestures(
                    onTap = { speak() },
                    onDoubleTap = { show(CritterCatalog.nextIndex(index)) },
                )
            },
        contentAlignment = Alignment.Center,
    ) {
        CritterStage(
            critter = critter,
            text = text,
            hint = when (interactions) {
                0 -> strings.tapHint
                1 -> strings.doubleTapHint
                else -> null
            },
        )

        // A watch with no text-to-speech engine would otherwise just be
        // mysteriously silent, so say so instead.
        AnimatedVisibility(
            visible = voiceStatus == CritterVoice.Status.Unavailable,
            enter = fadeIn(tween(400)),
            exit = fadeOut(tween(200)),
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 8.dp),
        ) {
            Text(
                text = strings.noVoice,
                style = MaterialTheme.typography.labelSmall,
                color = Color(0xFF6E7480),
                textAlign = TextAlign.Center,
            )
        }

    }
}

/**
 * The animation sits dead centre of the watch face; the name and the gesture
 * hint hang off the bottom.
 *
 * The name is anchored to the bottom rather than stacked under the animation in
 * a column, because a column has to centre the *whole* block — animation plus
 * text — which pushes the animation itself well above the middle of the screen.
 * The hint keeps its line whether or not it is showing, so nothing shifts when
 * it goes away.
 */
@Composable
private fun CritterStage(critter: Critter, text: CritterText, hint: String?) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.Asset(critter.assetPath),
    )
    val progress by animateLottieCompositionAsState(
        composition = composition,
        iterations = LottieConstants.IterateForever,
        restartOnPlay = true,
        // Watches often run with system animator scale turned down or off.
        ignoreSystemAnimatorScale = true,
    )
    val labelAlpha by animateFloatAsState(
        targetValue = if (composition == null) 0f else 1f,
        animationSpec = tween(250),
        label = "labelAlpha",
    )

    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        LottieAnimation(
            composition = composition,
            progress = { progress },
            modifier = Modifier
                .fillMaxWidth(ANIMATION_FRACTION)
                .aspectRatio(1f),
        )
        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .padding(start = 26.dp, end = 26.dp, bottom = 12.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(
                text = text.label,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = critter.accent.copy(alpha = labelAlpha),
                textAlign = TextAlign.Center,
                maxLines = 1,
            )
            // Fading the colour rather than the composable keeps the line's
            // height reserved, so the name never jumps when the hint retires.
            HintLine(hint)
        }
    }
}

/** One reserved line that fades its text in and out without changing height. */
@Composable
private fun HintLine(hint: String?) {
    var lastShown by remember { mutableStateOf("") }
    if (hint != null) lastShown = hint
    val alpha by animateFloatAsState(
        targetValue = if (hint != null) 1f else 0f,
        animationSpec = tween(if (hint != null) 500 else 250),
        label = "hintAlpha",
    )
    Box(modifier = Modifier.height(HINT_LINE_HEIGHT), contentAlignment = Alignment.Center) {
        Text(
            text = lastShown,
            style = MaterialTheme.typography.labelSmall,
            color = Color(0xFF7C838C).copy(alpha = alpha),
            textAlign = TextAlign.Center,
            maxLines = 1,
        )
    }
}

@Preview(device = WearDevices.LARGE_ROUND, showSystemUi = true)
@Composable
private fun PlayScreenPreview() {
    CritterTapTheme {
        PlayScreen(
            language = Language.ENGLISH,
            strings = UiText.of(Language.ENGLISH),
            onCritterShown = { _, _ -> },
        )
    }
}
