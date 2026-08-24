package com.example.crittertap.data

import androidx.compose.runtime.saveable.Saver
import androidx.compose.runtime.saveable.listSaver
import kotlin.random.Random

/**
 * Deals critters like a shuffled deck rather than rolling a die.
 *
 * Picking uniformly at random feels wrong in practice: a child sees the cat
 * three times in a dozen taps and never meets the giraffe. Instead a round is
 * a shuffle of every critter, dealt one at a time, and only once the round is
 * exhausted is a new one shuffled. So across any [size] draws every critter
 * appears exactly once.
 *
 * The one seam is the boundary between rounds — the last card of one round and
 * the first of the next could be the same critter, which would look like a
 * double tap that did nothing. [refill] swaps that card away.
 */
class CritterShuffler(
    private val size: Int,
    private val random: Random = Random.Default,
) {

    private val remaining = ArrayDeque<Int>()

    /** The critter on screen; -1 until the first [next]. */
    var current: Int = -1
        private set

    /** The state of the deck, for saving and restoring. */
    val state: List<Int> get() = listOf(current) + remaining

    init {
        require(size > 0) { "a catalog needs at least one critter" }
    }

    /** Deals the next critter, reshuffling when the round runs out. */
    fun next(): Int {
        if (remaining.isEmpty()) refill()
        current = remaining.removeFirst()
        return current
    }

    /**
     * Jumps straight to [index] — the rotating bezel browsing in order. It
     * counts as dealt, so the round stays honest and a following double tap
     * will not repeat it.
     */
    fun jumpTo(index: Int) {
        require(index in 0 until size) { "index $index outside 0..${size - 1}" }
        remaining.remove(index)
        current = index
    }

    /** How many critters are left before the deck is reshuffled. */
    val remainingInRound: Int get() = remaining.size

    /** Replaces the deck's state with [value]. */
    fun restore(value: List<Int>) {
        current = value.first()
        remaining.clear()
        remaining.addAll(value.drop(1))
    }

    private fun refill() {
        val round = (0 until size).shuffled(random).toMutableList()
        // Never open a new round with the critter that closed the last one.
        if (size > 1 && round.first() == current) {
            val swap = 1 + random.nextInt(size - 1)
            round[0] = round[swap].also { round[swap] = round[0] }
        }
        remaining.addAll(round)
    }

    companion object {
        /** Survives the watch killing and restoring the play screen. */
        fun saver(size: Int, random: Random = Random.Default): Saver<CritterShuffler, Any> =
            listSaver(
                save = { it.state },
                restore = { state -> CritterShuffler(size, random).apply { restore(state) } },
            )
    }
}
