package com.example.crittertap.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.wear.compose.foundation.lazy.ScalingLazyColumn
import androidx.wear.compose.foundation.lazy.items
import androidx.wear.compose.foundation.lazy.rememberScalingLazyListState
import androidx.wear.compose.material3.Button
import androidx.wear.compose.material3.ButtonDefaults
import androidx.wear.compose.material3.MaterialTheme
import androidx.wear.compose.material3.Text
import androidx.wear.tooling.preview.devices.WearDevices
import com.example.crittertap.data.CritterCatalog
import com.example.crittertap.data.Language
import com.example.crittertap.data.UiStrings
import com.example.crittertap.data.UiText
import com.example.crittertap.settings.SettingsRepository
import com.example.crittertap.settings.ShufflingMode
import com.example.crittertap.ui.theme.CritterColors
import com.example.crittertap.ui.theme.CritterTapTheme
import kotlin.math.roundToInt

/**
 * Screen for managing application settings like volume and language.
 *
 * Swipe right to go back to the menu.
 */
@Composable
fun SettingsScreen(
    strings: UiStrings,
    language: Language,
    volume: Float,
    catalogSize: Int,
    shufflingMode: ShufflingMode,
    speakLabelOnly: Boolean,
    onLanguage: (Language) -> Unit,
    onVolume: (Float) -> Unit,
    onCatalogSize: (Int) -> Unit,
    onShufflingMode: (ShufflingMode) -> Unit,
    onSpeakLabelOnly: (Boolean) -> Unit,
    modifier: Modifier = Modifier,
    missingVoiceFor: Language? = null,
) {
    val listState = rememberScalingLazyListState()
    ScalingLazyColumn(
        state = listState,
        modifier = modifier
            .fillMaxSize()
            .background(Color.Black),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        item {
            Text(
                text = strings.settings,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.primary,
            )
        }

        item { SectionLabel(strings.volume) }
        item {
            VolumeRow(
                volume = volume,
                mutedLabel = strings.muted,
                onVolume = onVolume,
            )
        }

        item { SectionLabel(strings.catalogSize) }
        item {
            CatalogSizeRow(
                size = catalogSize,
                onSize = onCatalogSize,
            )
        }

        item { SectionLabel(strings.order) }
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Box(modifier = Modifier.weight(1f)) {
                    ChoiceButton(
                        label = strings.random,
                        selected = shufflingMode == ShufflingMode.Random,
                        onClick = { onShufflingMode(ShufflingMode.Random) }
                    )
                }
                Box(modifier = Modifier.weight(1f)) {
                    ChoiceButton(
                        label = strings.sequential,
                        selected = shufflingMode == ShufflingMode.Sequential,
                        onClick = { onShufflingMode(ShufflingMode.Sequential) }
                    )
                }
            }
        }

        item { SectionLabel(strings.voiceDetail) }
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Box(modifier = Modifier.weight(1f)) {
                    ChoiceButton(
                        label = strings.labelOnly,
                        selected = speakLabelOnly,
                        onClick = { onSpeakLabelOnly(true) }
                    )
                }
                Box(modifier = Modifier.weight(1f)) {
                    ChoiceButton(
                        label = strings.fullDescription,
                        selected = !speakLabelOnly,
                        onClick = { onSpeakLabelOnly(false) }
                    )
                }
            }
        }

        item { SectionLabel(strings.language) }
        items(Language.entries) { option ->
            ChoiceButton(
                label = option.label,
                selected = option == language,
                onClick = { onLanguage(option) },
            )
        }

        if (missingVoiceFor != null) {
            item {
                Text(
                    text = strings.voiceMissing,
                    style = MaterialTheme.typography.labelSmall,
                    color = CritterColors.Warning,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 4.dp),
                )
            }
        }
    }
}

@Composable
private fun SectionLabel(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelMedium,
        color = CritterColors.SectionLabel,
        modifier = Modifier.padding(top = 6.dp),
    )
}

@Composable
private fun CatalogSizeRow(size: Int, onSize: (Int) -> Unit) {
    val step = 10
    val max = CritterCatalog.all.size
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(6.dp, Alignment.CenterHorizontally),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        StepButton("–", enabled = size > SettingsRepository.MIN_CATALOG_SIZE) { 
            onSize(size - step) 
        }
        Text(
            text = "$size",
            style = MaterialTheme.typography.bodyMedium,
            color = Color.White,
            textAlign = TextAlign.Center,
            modifier = Modifier.width(74.dp),
        )
        StepButton("+", enabled = size < max) { 
            onSize(size + step) 
        }
    }
}

/** Minus / value / plus, which beats a slider on a screen this small. */
@Composable
private fun VolumeRow(volume: Float, mutedLabel: String, onVolume: (Float) -> Unit) {
    val step = SettingsRepository.VOLUME_STEP
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(6.dp, Alignment.CenterHorizontally),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        StepButton("–", enabled = volume > 0f) { onVolume(volume - step) }
        Text(
            text = if (volume <= 0f) mutedLabel else "${(volume * 100).roundToInt()}%",
            style = MaterialTheme.typography.bodyMedium,
            color = if (volume <= 0f) CritterColors.Muted else Color.White,
            textAlign = TextAlign.Center,
            modifier = Modifier.width(74.dp),
        )
        StepButton("+", enabled = volume < 1f) { onVolume(volume + step) }
    }
}

@Composable
private fun StepButton(symbol: String, enabled: Boolean, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        enabled = enabled,
        modifier = Modifier.size(44.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = CritterColors.Container,
            contentColor = Color.White,
        ),
    ) {
        Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
            Text(symbol, style = MaterialTheme.typography.titleMedium)
        }
    }
}

@Composable
private fun ChoiceButton(label: String, selected: Boolean, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        colors = ButtonDefaults.buttonColors(
            containerColor = if (selected) CritterColors.SelectedContainer else CritterColors.Container,
            contentColor = if (selected) Color.White else CritterColors.UnselectedContent,
        ),
    ) {
        Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
            Text(
                text = if (selected) "• $label" else label,
                textAlign = TextAlign.Center,
            )
        }
    }
}

@Preview(device = WearDevices.LARGE_ROUND, showSystemUi = true)
@Composable
private fun SettingsScreenPreview() {
    CritterTapTheme {
        SettingsScreen(
            strings = UiText.of(Language.ENGLISH),
            language = Language.ENGLISH,
            volume = 0.7f,
            catalogSize = 30,
            shufflingMode = ShufflingMode.Random,
            speakLabelOnly = false,
            onLanguage = {},
            onVolume = {},
            onCatalogSize = {},
            onShufflingMode = {},
            onSpeakLabelOnly = {},
        )
    }
}
