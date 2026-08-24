package com.example.crittertap.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.wear.compose.foundation.lazy.ScalingLazyColumn
import androidx.wear.compose.foundation.lazy.rememberScalingLazyListState
import androidx.wear.compose.material3.Button
import androidx.wear.compose.material3.ButtonDefaults
import androidx.wear.compose.material3.MaterialTheme
import androidx.wear.compose.material3.Text
import androidx.wear.tooling.preview.devices.WearDevices
import com.airbnb.lottie.compose.LottieAnimation
import com.airbnb.lottie.compose.LottieCompositionSpec
import com.airbnb.lottie.compose.LottieConstants
import com.airbnb.lottie.compose.animateLottieCompositionAsState
import com.airbnb.lottie.compose.rememberLottieComposition
import com.example.crittertap.data.Language
import com.example.crittertap.data.UiStrings
import com.example.crittertap.data.UiText
import com.example.crittertap.ui.theme.CritterColors
import com.example.crittertap.ui.theme.CritterTapTheme

/**
 * The landing screen: play, or go and change the settings.
 *
 * A scaling list rather than a plain column, so the round screen keeps the
 * buttons off the curved edges and the whole thing still works if a longer
 * translation pushes it past one screenful.
 */
@Composable
fun MenuScreen(
    strings: UiStrings,
    onPlay: () -> Unit,
    onSettings: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val listState = rememberScalingLazyListState()
    ScalingLazyColumn(
        state = listState,
        modifier = modifier
            .fillMaxSize()
            .background(Color.Black),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        item { MenuMascot() }
        item {
            Text(
                text = strings.appTitle,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.primary,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(bottom = 4.dp),
            )
        }
        item {
            MenuButton(
                label = strings.play,
                container = CritterColors.SelectedContainer,
                content = Color.White,
                onClick = onPlay,
            )
        }
        item {
            MenuButton(
                label = strings.settings,
                container = CritterColors.Container,
                content = CritterColors.UnselectedContent,
                onClick = onSettings,
            )
        }
    }
}

/** Wear's Button lays its slot out start-aligned, so the label gets centred here. */
@Composable
private fun MenuButton(
    label: String,
    container: Color,
    content: Color,
    onClick: () -> Unit,
) {
    Button(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        colors = ButtonDefaults.buttonColors(
            containerColor = container,
            contentColor = content,
        ),
    ) {
        Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
            Text(text = label, textAlign = TextAlign.Center)
        }
    }
}

/** A small looping critter so the menu is not just two grey slabs. */
@Composable
private fun MenuMascot() {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.Asset("animations/cat.json"),
    )
    val progress by animateLottieCompositionAsState(
        composition = composition,
        iterations = LottieConstants.IterateForever,
        ignoreSystemAnimatorScale = true,
    )
    LottieAnimation(
        composition = composition,
        progress = { progress },
        modifier = Modifier.size(52.dp),
    )
}

@Preview(device = WearDevices.LARGE_ROUND, showSystemUi = true)
@Composable
private fun MenuScreenPreview() {
    CritterTapTheme {
        MenuScreen(UiText.of(Language.ENGLISH), onPlay = {}, onSettings = {})
    }
}
