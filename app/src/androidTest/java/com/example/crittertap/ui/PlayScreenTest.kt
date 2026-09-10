package com.example.crittertap.ui

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onRoot
import androidx.compose.ui.test.performTouchInput
import androidx.compose.ui.test.doubleClick
import androidx.compose.ui.test.click
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.example.crittertap.data.Critter
import com.example.crittertap.data.CritterCatalog
import com.example.crittertap.data.CritterText
import com.example.crittertap.data.CritterTexts
import com.example.crittertap.data.Language
import com.example.crittertap.data.UiText
import com.example.crittertap.settings.ShufflingMode
import com.example.crittertap.ui.theme.CritterTapTheme
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Locks in what the two gestures mean. Screenshots proved this once by hand;
 * these keep it true.
 */
@RunWith(AndroidJUnit4::class)
class PlayScreenTest {

    @get:Rule
    val rule = createComposeRule()

    private val shown = mutableListOf<Pair<String, CritterText>>()
    private val poked = mutableListOf<Pair<String, CritterText>>()

    private fun start(language: Language = Language.ENGLISH) {
        shown.clear()
        poked.clear()
        rule.setContent {
            val playViewModel: PlayViewModel = viewModel(
                factory = PlayViewModel.factory(CritterCatalog.all.size, ShufflingMode.Random)
            )
            CritterTapTheme {
                PlayScreen(
                    language = language,
                    strings = UiText.of(language),
                    onCritterShown = { critter: Critter, text: CritterText ->
                        shown += critter.id to text
                    },
                    onCritterPoked = { critter: Critter, text: CritterText ->
                        poked += critter.id to text
                    },
                    viewModel = playViewModel
                )
            }
        }
        rule.waitForIdle()
    }

    /** Taps, then lets the double-tap timeout expire so the single tap fires. */
    private fun tapOnce() {
        rule.onRoot().performTouchInput { click() }
        rule.mainClock.advanceTimeBy(500)
        rule.waitForIdle()
    }

    private fun tapTwice() {
        rule.onRoot().performTouchInput { doubleClick() }
        rule.mainClock.advanceTimeBy(500)
        rule.waitForIdle()
    }

    @Test
    fun introducesACritterOnArrival() {
        start()
        assertEquals(1, shown.size)
    }

    @Test
    fun singleTapReplaysTheSameCritterWithoutReintroducing() {
        start()
        val first = shown.single().first

        tapOnce()

        assertEquals("a single tap should not repeat the introduction", 1, shown.size)
        assertEquals("a single tap should replay the same critter", 1, poked.size)
        assertEquals(first, poked.single().first)
    }

    @Test
    fun doubleTapMovesToADifferentCritter() {
        start()
        val first = shown.single().first

        tapTwice()

        assertTrue(shown.size >= 2)
        assertNotEquals("a double tap should bring on a new critter", first, shown.last().first)
    }

    @Test
    fun repeatedDoubleTapsNeverShowTheSameCritterTwiceRunning() {
        start()
        repeat(12) { tapTwice() }

        val ids = shown.map { it.first }
        val repeats = ids.zipWithNext().filter { (a, b) -> a == b }
        assertEquals("consecutive repeats: $ids", emptyList<Pair<String, String>>(), repeats)
    }

    @Test
    fun oneRoundOfDoubleTapsShowsEveryCritterExactlyOnce() {
        start()
        val catalog = CritterCatalog.all.map { it.id }
        // the screen arrives showing one already, so a round is size - 1 more
        repeat(catalog.size - 1) { tapTwice() }

        val ids = shown.map { it.first }
        assertEquals("a round should cover the catalog", catalog.toSet(), ids.toSet())
        assertEquals("and show nothing twice", catalog.size, ids.size)
    }

    @Test
    fun everyCritterIsAnnouncedWithItsOwnWords() {
        start()
        tapTwice()
        tapTwice()
        shown.forEach { (id, text) ->
            assertEquals(CritterTexts.of(id, Language.ENGLISH), text)
        }
    }

    @Test
    fun spanishIsUsedWhenSpanishIsChosen() {
        start(Language.SPANISH)
        val (id, text) = shown.single()
        assertEquals(CritterTexts.of(id, Language.SPANISH), text)
        assertNotEquals(CritterTexts.of(id, Language.ENGLISH).label, text.label)
    }
}
