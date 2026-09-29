package com.example.crittertap.data

import java.io.File
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.random.Random

class CritterCatalogTest {

    @Test
    fun `every critter points at a distinct animation asset`() {
        val assets = CritterCatalog.all.map { it.assetPath }
        assertEquals(assets.size, assets.toSet().size)
        assertTrue(assets.all { it.startsWith("animations/") && it.endsWith(".json") })
    }

    @Test
    fun `every critter's animation file actually exists`() {
        CritterCatalog.all.forEach { critter ->
            val file = File("src/main/assets/${critter.assetPath}")
            assertTrue("missing asset for ${critter.id}: ${file.path}", file.exists())
        }
    }

    @Test
    fun `ids are unique`() {
        val ids = CritterCatalog.all.map { it.id }
        assertEquals(ids.size, ids.toSet().size)
    }

    @Test
    fun `the catalog hands out a working deck`() {
        val deck = CritterCatalog.shuffler(Random(4))
        val round = CritterCatalog.all.indices.map { deck.next() }
        assertEquals(CritterCatalog.all.indices.toSet(), round.toSet())
    }
}
