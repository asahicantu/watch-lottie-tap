package com.example.crittertap.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * The translations are the easiest thing to get quietly out of step with the
 * catalog, so they are checked rather than trusted.
 */
class CritterTextTest {

    private val ids = CritterCatalog.all.map { it.id }

    @Test
    fun `every language covers every critter`() {
        Language.entries.forEach { language ->
            assertEquals(
                "missing ${language.tag} wording",
                emptyList<String>(),
                CritterTexts.missingIn(language, ids),
            )
        }
    }

    @Test
    fun `no wording is left blank`() {
        Language.entries.forEach { language ->
            ids.forEach { id ->
                val text = CritterTexts.of(id, language)
                assertTrue("$id/$language label", text.label.isNotBlank())
                assertTrue("$id/$language description", text.description.isNotBlank())
                assertTrue("$id/$language noise", text.noise.isNotBlank())
            }
        }
    }

    @Test
    fun `spanish is actually translated, not a copy of english`() {
        val identical = ids.filter { id ->
            CritterTexts.of(id, Language.SPANISH).description ==
                CritterTexts.of(id, Language.ENGLISH).description
        }
        assertEquals(emptyList<String>(), identical)
    }

    @Test
    fun `labels are unique within a language`() {
        Language.entries.forEach { language ->
            val labels = ids.map { CritterTexts.of(it, language).label }
            assertEquals("duplicate labels in ${language.tag}", labels.size, labels.toSet().size)
        }
    }

    @Test
    fun `the description leads with the animal and the noise is separate`() {
        Language.entries.forEach { language ->
            ids.forEach { id ->
                val text = CritterTexts.of(id, language)
                assertNotEquals("$id/$language", text.description, text.noise)
                assertTrue(
                    "$id/$language description should be a sentence",
                    text.description.trimEnd().endsWith("."),
                )
            }
        }
    }

    @Test
    fun `ui strings exist for every language`() {
        Language.entries.forEach { language ->
            val strings = UiText.of(language)
            listOf(
                strings.appTitle, strings.play, strings.settings, strings.volume,
                strings.language, strings.muted, strings.tapHint,
                strings.doubleTapHint, strings.noVoice, strings.voiceMissing,
            ).forEach { assertTrue("blank string for ${language.tag}", it.isNotBlank()) }
        }
    }
}
