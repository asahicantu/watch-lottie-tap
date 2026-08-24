package com.example.crittertap.ui

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

private const val SPARKLE_COUNT = 8
private const val BURST_MILLIS = 640

/**
 * A ring of little stars that flies outwards once each time [trigger] changes.
 *
 * The point is to make the touch visibly cause something. The critter's own
 * animation loops the same whether or not it has been tapped, so without this
 * the only feedback is a sound the child may not connect to their finger.
 */
@Composable
fun SparkleBurst(
    trigger: Int,
    color: Color,
    modifier: Modifier = Modifier,
) {
    val progress = remember { Animatable(1f) }

    LaunchedEffect(trigger) {
        if (trigger <= 0) return@LaunchedEffect
        progress.snapTo(0f)
        progress.animateTo(1f, tween(BURST_MILLIS, easing = FastOutSlowInEasing))
    }

    val phase = progress.value
    if (phase >= 1f) return

    Canvas(modifier = modifier) {
        val radius = size.minDimension / 2f
        val distance = radius * (0.50f + 0.56f * phase)
        val alpha = (1f - phase * phase).coerceIn(0f, 1f)
        val outer = radius * 0.115f * (1f - 0.35f * phase)

        repeat(SPARKLE_COUNT) { index ->
            val turn = index.toFloat() / SPARKLE_COUNT + phase * 0.05f
            val angle = turn * 2.0 * PI
            val cx = center.x + (cos(angle) * distance).toFloat()
            val cy = center.y + (sin(angle) * distance).toFloat()
            drawPath(
                path = starPath(cx, cy, outer, outer * 0.44f, turn),
                color = if (index % 2 == 0) color else Color.White,
                alpha = alpha,
            )
        }
    }
}

/** A five-pointed star centred on ([cx], [cy]). */
private fun starPath(cx: Float, cy: Float, outer: Float, inner: Float, turn: Float): Path {
    val path = Path()
    val points = 5
    repeat(points * 2) { step ->
        val radius = if (step % 2 == 0) outer else inner
        val angle = (step.toFloat() / (points * 2) + turn) * 2.0 * PI - PI / 2
        val x = cx + (cos(angle) * radius).toFloat()
        val y = cy + (sin(angle) * radius).toFloat()
        if (step == 0) path.moveTo(x, y) else path.lineTo(x, y)
    }
    path.close()
    return path
}
