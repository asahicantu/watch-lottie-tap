package com.example.crittertap.data

import androidx.compose.ui.graphics.Color
import kotlin.random.Random

/**
 * The array of critters the play screen picks from.
 *
 * To add one: drop `<id>.json` into `app/src/main/assets/animations/`, add a
 * line here, and add the wording to [CritterTexts] for every language.
 */
object CritterCatalog {

    val all: List<Critter> = listOf(
        critter("cat", 0xFFF0A04B),
        critter("dog", 0xFFC98A4B),
        critter("cow", 0xFFF2AAB4),
        critter("duck", 0xFFFFD93B),
        critter("frog", 0xFF6CC24A),
        critter("lion", 0xFFF4C07A),
        critter("bee", 0xFFFFD21F),
        critter("sheep", 0xFFF2EEE6),
        critter("owl", 0xFFC9A273),
        critter("pig", 0xFFF6A5B8),
        critter("horse", 0xFFC17A3F),
        critter("elephant", 0xFF98A2AD),
        critter("monkey", 0xFFDBA97C),
        critter("penguin", 0xFFF0912A),
        critter("tiger", 0xFFF0913C),
        critter("bear", 0xFFB98C63),
        critter("rabbit", 0xFFECE7DF),
        critter("mouse", 0xFFA9A29B),
        critter("fox", 0xFFE8792B),
        critter("wolf", 0xFF9BA5AE),
        critter("rooster", 0xFFD94F3D),
        critter("goat", 0xFFF2ECE1),
        critter("donkey", 0xFF9B9086),
        critter("panda", 0xFFF7F4EE),
        critter("koala", 0xFF9AA0A6),
        critter("giraffe", 0xFFF0C169),
        critter("hippo", 0xFFA98BB5),
        critter("crocodile", 0xFF5F9E56),
        critter("snake", 0xFF6FBF4A),
        critter("parrot", 0xFF3FB56A),
    )

    private val byId = all.associateBy { it.id }

    operator fun get(id: String): Critter = byId.getValue(id)

    /** A deck that deals every critter once per round. See [CritterShuffler]. */
    fun shuffler(random: Random = Random.Default) = CritterShuffler(all.size, random)

    private fun critter(id: String, accent: Long) =
        Critter(id = id, assetPath = "animations/$id.json", accent = Color(accent))
}
