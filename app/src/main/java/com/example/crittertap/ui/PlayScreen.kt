package com.example.crittertap.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.ui.draw.scale
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
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.rotary.onRotaryScrollEvent
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.wear.compose.material3.MaterialTheme
import androidx.wear.compose.material3.Text
import androidx.wear.tooling.preview.devices.WearDevices
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.airbnb.lottie.compose.LottieAnimation
import com.airbnb.lottie.compose.LottieCompositionSpec
import com.airbnb.lottie.compose.LottieConstants
import com.airbnb.lottie.compose.animateLottieCompositionAsState
import com.airbnb.lottie.compose.rememberLottieComposition
import com.example.crittertap.audio.CritterVoice
import com.example.crittertap.data.Critter
import com.example.crittertap.data.CritterText
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
 * The main play screen of the toy.
 *
 * Interactions:
 * * **Tap** — says the critter's description, then the noise it makes.
 * * **Double tap** — brings on the next critter (and introduces it).
 * * **Rotating bezel / crown** — steps through the catalog in order.
 *
 * @param language The current [Language] selected in settings.
 * @param strings The localized UI strings.
 * @param onCritterShown Callback when a critter is presented to the user (usually for voice).
 * @param modifier Modifier for the root container.
 * @param voiceStatus The availability status of the text-to-speech engine.
 * @param viewModel The ViewModel managing play state.
 */
@OptIn(ExperimentalComposeUiApi::class)
@Composable
fun PlayScreen(
    language: Language,
    strings: UiStrings,
    onCritterShown: (Critter, CritterText) -> Unit,
    modifier: Modifier = Modifier,
    voiceStatus: CritterVoice.Status = CritterVoice.Status.Ready,
    viewModel: PlayViewModel = viewModel(factory = PlayViewModel.Factory)
) {
    val context = LocalContext.current
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    val haptics = remember(context) { CritterHaptics(context) }
    val focusRequester = remember { FocusRequester() }
    var rotaryAccumulator by remember { mutableFloatStateOf(0f) }

    fun speak() {
        haptics.poke()
        viewModel.onSpeakTriggered(onCritterShown)
    }

    fun next() {
        haptics.arrive()
        viewModel.onNextCritterTriggered(onCritterShown)
    }

    // Introduce whatever is on screen when the player arrives, and again if the
    // language changes underneath them.
    LaunchedEffect(language) {
        viewModel.onLanguageChanged(language)
        val currentState = viewModel.uiState.value
        onCritterShown(currentState.critter, currentState.text)
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
                    haptics.arrive()
                    viewModel.onRotaryScroll(steps, onCritterShown)
                }
                true
            }
            .focusRequester(focusRequester)
            .focusable()
            .pointerInput(Unit) {
                detectTapGestures(
                    onTap = { speak() },
                    onDoubleTap = { next() },
                )
            },
        contentAlignment = Alignment.Center,
    ) {
        CritterStage(
            critter = uiState.critter,
            text = uiState.text,
            reaction = uiState.interactions,
            hint = when (uiState.interactions) {
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
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
            )
        }

    }
}

/**
 * The stage where the critter animation and its label are displayed.
 *
 * The animation sits dead centre of the watch face; the name and the gesture
 * hint hang off the bottom.
 */
@Composable
private fun CritterStage(
    critter: Critter,
    text: CritterText,
    hint: String?,
    reaction: Int,
) {
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

    // Presses in, then springs back past its resting size: the critter reacts
    // to being poked rather than looping on regardless.
    val squash = remember { Animatable(1f) }
    LaunchedEffect(reaction) {
        if (reaction <= 0) return@LaunchedEffect
        squash.snapTo(0.86f)
        squash.animateTo(
            targetValue = 1f,
            animationSpec = spring(
                dampingRatio = Spring.DampingRatioMediumBouncy,
                stiffness = Spring.StiffnessLow,
            ),
        )
    }

    val contentDescription = "${text.label}: ${text.description}"

    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        LottieAnimation(
            composition = composition,
            progress = { progress },
            modifier = Modifier
                .fillMaxWidth(ANIMATION_FRACTION)
                .aspectRatio(1f)
                .scale(squash.value)
                .semantics { this.contentDescription = contentDescription },
        )
        SparkleBurst(
            trigger = reaction,
            color = critter.accent,
            modifier = Modifier
                .fillMaxWidth(ANIMATION_FRACTION * 1.5f)
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
            color = MaterialTheme.colorScheme.outline.copy(alpha = alpha),
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
