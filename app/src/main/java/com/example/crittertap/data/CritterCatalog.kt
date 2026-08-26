package com.example.crittertap.data

import androidx.annotation.RawRes
import androidx.compose.ui.graphics.Color
import com.example.crittertap.R
import kotlin.random.Random

/**
 * The array of critters the play screen picks from.
 *
 * To add one: drop `<id>.json` into `app/src/main/assets/animations/`, add a
 * line here, and add the wording to [CritterTexts] for every language.
 */
object CritterCatalog {

    val all: List<Critter> = listOf(
        critter("cat", 0xFFF0A04B, soundRes = R.raw.cat),
        critter("dog", 0xFFC98A4B, soundRes = R.raw.dog),
        critter("cow", 0xFFF2AAB4, soundRes = R.raw.cow),
        critter("duck", 0xFFFFD93B, soundRes = R.raw.duck),
        critter("frog", 0xFF6CC24A, soundRes = R.raw.frog),
        critter("lion", 0xFFF4C07A, soundRes = R.raw.lion),
        critter("bee", 0xFFFFD21F),
        critter("sheep", 0xFFF2EEE6, soundRes = R.raw.sheep),
        critter("owl", 0xFFC9A273, soundRes = R.raw.owl),
        critter("pig", 0xFFF6A5B8, soundRes = R.raw.pig),
        critter("horse", 0xFFC17A3F, soundRes = R.raw.horse),
        critter("elephant", 0xFF98A2AD, soundRes = R.raw.elephant),
        critter("monkey", 0xFFDBA97C, soundRes = R.raw.monkey),
        critter("penguin", 0xFFF0912A),
        critter("tiger", 0xFFF0913C, soundRes = R.raw.tiger),
        critter("bear", 0xFFB98C63, soundRes = R.raw.bear),
        critter("rabbit", 0xFFECE7DF),
        critter("mouse", 0xFFA9A29B, soundRes = R.raw.mouse),
        critter("fox", 0xFFE8792B, soundRes = R.raw.fox),
        critter("wolf", 0xFF9BA5AE),
        critter("rooster", 0xFFD94F3D, soundRes = R.raw.rooster),
        critter("goat", 0xFFF2ECE1),
        critter("donkey", 0xFF9B9086, soundRes = R.raw.donkey),
        critter("panda", 0xFFF7F4EE, soundRes = R.raw.panda),
        critter("koala", 0xFF9AA0A6),
        critter("giraffe", 0xFFF0C169, soundRes = R.raw.giraffe),
        critter("hippo", 0xFFA98BB5),
        critter("crocodile", 0xFF5F9E56, soundRes = R.raw.crocodile),
        critter("snake", 0xFF6FBF4A),
        critter("parrot", 0xFF3FB56A, soundRes = R.raw.parrot),
    )

    private val byId = all.associateBy { it.id }

    operator fun get(id: String): Critter = byId.getValue(id)

    /** A deck that deals every critter once per round. See [CritterShuffler]. */
    fun shuffler(random: Random = Random.Default) = CritterShuffler(all.size, random)

    private fun critter(id: String, accent: Long, @RawRes soundRes: Int? = null) =
        Critter(id = id, assetPath = "animations/$id.json", accent = Color(accent),
                soundRes = soundRes)
}
