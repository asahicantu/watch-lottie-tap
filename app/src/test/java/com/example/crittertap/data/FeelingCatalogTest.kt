package com.example.crittertap.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.random.Random

class FeelingCatalogTest {

    @Test
    fun `every feeling points at a distinct animation asset`() {
        val assets = FeelingCatalog.all.map { it.assetPath }
        assertEquals(assets.size, assets.toSet().size)
        assertTrue(assets.all { it.startsWith("animations/") && it.endsWith(".json") })
    }

    @Test
    fun `ids are unique`() {
        val ids = FeelingCatalog.all.map { it.id }
        assertEquals(ids.size, ids.toSet().size)
    }

    @Test
    fun `the catalog hands out a working deck`() {
        val deck = FeelingCatalog.shuffler(Random(4))
        val round = FeelingCatalog.all.indices.map { deck.next() }
        assertEquals(FeelingCatalog.all.indices.toSet(), round.toSet())
    }

    @Test
    fun `there are at least twenty feelings to choose from`() {
        assertTrue(FeelingCatalog.all.size >= 20)
    }
}
