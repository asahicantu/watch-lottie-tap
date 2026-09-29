package com.example.crittertap.data

import androidx.compose.ui.graphics.Color
import kotlin.random.Random

/**
 * The array of feelings the play screen picks from, when [Category.FEELINGS]
 * is selected in settings.
 *
 * Reuses [Critter] as the generic "tappable thing with an animation" model —
 * a feeling has no animal sound of its own, so [Critter.soundRes] stays null
 * and [CritterText.noise] stays null too; [CritterVoice] speaks only the
 * description for these.
 *
 * To add one: drop `<id>.json` into `app/src/main/assets/animations/feelings/`,
 * add a line here, and add the wording to [FeelingTexts] for every language.
 */
object FeelingCatalog {

    val all: List<Critter> = listOf(
        feeling("happy", 0xFFFFC93C),
        feeling("sad", 0xFF6FA8DC),
        feeling("angry", 0xFFE15554),
        feeling("scared", 0xFF8E7CC3),
        feeling("surprised", 0xFFF5A623),
        feeling("disgusted", 0xFF8BC34A),
        feeling("calm", 0xFF7FD1B9),
        feeling("excited", 0xFFFF6F61),
        feeling("tired", 0xFFA79E8C),
        feeling("proud", 0xFFD4A017),
        feeling("embarrassed", 0xFFF4989C),
        feeling("confused", 0xFFB39DDB),
        feeling("jealous", 0xFF7CB342),
        feeling("grateful", 0xFFF2C14E),
        feeling("lonely", 0xFF5C7A99),
        feeling("hopeful", 0xFF6FCF97),
        feeling("nervous", 0xFFC9ADA7),
        feeling("bored", 0xFF9DA5B4),
        feeling("curious", 0xFF4FC3F7),
        feeling("loving", 0xFFF06292),
    )

    private val byId = all.associateBy { it.id }

    operator fun get(id: String): Critter = byId.getValue(id)

    /** A deck that deals every feeling once per round. See [CritterShuffler]. */
    fun shuffler(random: Random = Random.Default) = CritterShuffler(all.size, random)

    private fun feeling(id: String, accent: Long) =
        Critter(id = id, assetPath = "animations/feelings/$id.json", accent = Color(accent))
}
