package com.example.crittertap.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** Mirrors [CritterTextTest] for the feelings catalog. */
class FeelingTextTest {

    private val ids = FeelingCatalog.all.map { it.id }

    @Test
    fun `every language covers every feeling`() {
        Language.entries.forEach { language ->
            assertEquals(
                "missing ${language.tag} wording",
                emptyList<String>(),
                FeelingTexts.missingIn(language, ids),
            )
        }
    }

    @Test
    fun `no wording is left blank`() {
        Language.entries.forEach { language ->
            ids.forEach { id ->
                val text = FeelingTexts.of(id, language)
                assertTrue("$id/$language label", text.label.isNotBlank())
                assertTrue("$id/$language description", text.description.isNotBlank())
            }
        }
    }

    @Test
    fun `feelings carry no noise, since they make no sound of their own`() {
        Language.entries.forEach { language ->
            ids.forEach { id ->
                val text = FeelingTexts.of(id, language)
                assertEquals(null, text.noise)
            }
        }
    }

    @Test
    fun `spanish is actually translated, not a copy of english`() {
        val identical = ids.filter { id ->
            FeelingTexts.of(id, Language.SPANISH).description ==
                FeelingTexts.of(id, Language.ENGLISH).description
        }
        assertEquals(emptyList<String>(), identical)
    }

    @Test
    fun `labels are unique within a language`() {
        Language.entries.forEach { language ->
            val labels = ids.map { FeelingTexts.of(it, language).label }
            assertEquals("duplicate labels in ${language.tag}", labels.size, labels.toSet().size)
        }
    }

    @Test
    fun `the description is a full sentence`() {
        Language.entries.forEach { language ->
            ids.forEach { id ->
                val text = FeelingTexts.of(id, language)
                assertTrue(
                    "$id/$language description should be a sentence",
                    text.description.trimEnd().endsWith("."),
                )
            }
        }
    }
}
