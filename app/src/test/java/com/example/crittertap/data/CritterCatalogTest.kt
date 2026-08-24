package com.example.crittertap.data

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
    fun `ids are unique`() {
        val ids = CritterCatalog.all.map { it.id }
        assertEquals(ids.size, ids.toSet().size)
    }

    @Test
    fun `nextIndex never returns the critter already on screen`() {
        val random = Random(20260824)
        CritterCatalog.all.indices.forEach { current ->
            repeat(100) {
                val next = CritterCatalog.nextIndex(current, random)
                assertNotEquals(current, next)
                assertTrue(next in CritterCatalog.all.indices)
            }
        }
    }

    @Test
    fun `nextIndex can reach every other critter`() {
        val random = Random(7)
        val seen = (0 until 6000)
            .map { CritterCatalog.nextIndex(0, random) }
            .toSet()
        assertEquals(CritterCatalog.all.indices.drop(1).toSet(), seen)
    }
}
