package com.example.crittertap.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.wear.compose.material3.ColorScheme
import androidx.wear.compose.material3.MaterialTheme

/**
 * Standard colors for the CritterTap UI.
 */
object CritterColors {
    /** Color for gesture hints and secondary labels. */
    val Hint = Color(0xFF7C838C)
    
    /** Color for system status messages (e.g. "no voice engine"). */
    val Status = Color(0xFF6E7480)

    /** Color for warning messages (e.g. "missing voice data"). */
    val Warning = Color(0xFFD8974A)

    /** Color for section labels in settings. */
    val SectionLabel = Color(0xFF9BA1A9)

    /** Color for muted text. */
    val Muted = Color(0xFF8A8F96)

    /** Standard container color for buttons and items. */
    val Container = Color(0xFF23262B)

    /** Container color for selected items (greenish). */
    val SelectedContainer = Color(0xFF2E6B3E)

    /** Content color for unselected items. */
    val UnselectedContent = Color(0xFFC9CED4)
}

/** Black-background theme; on the watch OLED that means the critter floats in the dark. */
@Composable
fun CritterTapTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = ColorScheme(
            background = Color.Black,
            onBackground = Color.White,
            surfaceContainer = Color(0xFF17191C),
            primary = Color(0xFFFFD21F),
            onPrimary = Color.Black,
            onSurfaceVariant = CritterColors.Status,
            outline = CritterColors.Hint
        ),
        content = content,
    )
}
