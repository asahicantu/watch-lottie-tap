package com.example.crittertap.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.wear.compose.material3.ColorScheme
import androidx.wear.compose.material3.MaterialTheme

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
        ),
        content = content,
    )
}
