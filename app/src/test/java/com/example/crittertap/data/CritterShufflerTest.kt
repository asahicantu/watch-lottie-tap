package com.example.crittertap.data

import androidx.compose.runtime.saveable.SaverScope
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.random.Random

class CritterShufflerTest {

    private val size = CritterCatalog.all.size

    @Test
    fun `one round shows every critter exactly once`() {
        val shuffler = CritterShuffler(size, Random(1))
        val round = (0 until size).map { shuffler.next() }
        assertEquals(
            "a round should be a permutation of the whole catalog",
            (0 until size).toSet(),
            round.toSet(),
        )
        assertEquals("no critter twice in a round", size, round.toSet().size)
    }

    @Test
    fun `every round is complete, round after round`() {
        val shuffler = CritterShuffler(size, Random(99))
        repeat(20) { roundNumber ->
            val round = (0 until size).map { shuffler.next() }
            assertEquals(
                "round $roundNumber was not a full sweep",
                (0 until size).toSet(),
                round.toSet(),
            )
        }
    }

    @Test
    fun `never deals the same critter twice running, including across rounds`() {
        // Many seeds, because the round boundary is the only place it could
        // happen and it needs the shuffle to land badly to show up at all.
        (0 until 200).forEach { seed ->
            val shuffler = CritterShuffler(size, Random(seed))
            val dealt = (0 until size * 4).map { shuffler.next() }
            val repeats = dealt.zipWithNext().withIndex().filter { it.value.first == it.value.second }
            assertEquals(
                "seed $seed repeated at ${repeats.map { it.index }}",
                emptyList<IndexedValue<Pair<Int, Int>>>(),
                repeats,
            )
        }
    }

    @Test
    fun `rounds are actually shuffled, not the same order every time`() {
        val shuffler = CritterShuffler(size, Random(7))
        val first = (0 until size).map { shuffler.next() }
        val second = (0 until size).map { shuffler.next() }
        assertNotEquals("two identical rounds means it is not shuffling", first, second)
    }

    @Test
    fun `different seeds give different orders`() {
        val a = CritterShuffler(size, Random(1)).let { s -> (0 until size).map { s.next() } }
        val b = CritterShuffler(size, Random(2)).let { s -> (0 until size).map { s.next() } }
        assertNotEquals(a, b)
    }

    @Test
    fun `jumping with the bezel counts as dealt, so the round stays honest`() {
        val shuffler = CritterShuffler(size, Random(3))
        shuffler.next()
        shuffler.jumpTo(11)
        assertEquals(11, shuffler.current)

        // Deal out the rest of the round; 11 must not come round again.
        val rest = (0 until shuffler.remainingInRound).map { shuffler.next() }
        assertTrue("11 was already shown this round", 11 !in rest)
    }

    @Test
    fun `jumping to the critter already on screen does not lose it from the round`() {
        val shuffler = CritterShuffler(size, Random(5))
        val shown = shuffler.next()
        shuffler.jumpTo(shown)
        assertEquals(shown, shuffler.current)
        val rest = (0 until shuffler.remainingInRound).map { shuffler.next() }
        assertEquals("the rest of the round should still be complete",
            (0 until size).toSet() - shown, rest.toSet())
    }

    @Test
    fun `a restored shuffler carries on where it left off`() {
        val original = CritterShuffler(size, Random(42))
        repeat(7) { original.next() }

        val saver = CritterShuffler.saver(size, Random(42))
        val scope = SaverScope { true }
        val state = with(saver) { scope.save(original) }
        val restored = saver.restore(state!!)!!

        assertEquals(original.current, restored.current)
        assertEquals(original.remainingInRound, restored.remainingInRound)

        // and finishing the round still yields the untouched critters
        val fromOriginal = (0 until original.remainingInRound).map { original.next() }
        val fromRestored = (0 until restored.remainingInRound).map { restored.next() }
        assertEquals(fromOriginal, fromRestored)
    }

    @Test
    fun `a one-critter catalog does not spin`() {
        val shuffler = CritterShuffler(1, Random(0))
        repeat(5) { assertEquals(0, shuffler.next()) }
    }
}
