package com.example.crittertap.data

import androidx.annotation.RawRes
import androidx.compose.ui.graphics.Color

/**
 * One tappable critter. The wording lives in [CritterTexts] because it changes
 * with the chosen language; everything here is language-independent.
 *
 * @param id         stable key, also the asset file name and the text lookup key
 * @param assetPath  path inside `src/main/assets`
 * @param accent     colour used for the name on screen
 * @param soundRes   optional recording in `res/raw`; when set it is played in
 *                   place of speaking the noise
 */
data class Critter(
    val id: String,
    val assetPath: String,
    val accent: Color,
    @param:RawRes val soundRes: Int? = null,
)
