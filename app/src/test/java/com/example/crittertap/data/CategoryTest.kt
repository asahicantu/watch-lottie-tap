package com.example.crittertap.data

import org.junit.Assert.assertEquals
import org.junit.Test

class CategoryTest {

    @Test
    fun `fromTag round-trips every category's own tag`() {
        Category.entries.forEach { category ->
            assertEquals(category, Category.fromTag(category.tag))
        }
    }

    @Test
    fun `an unknown or missing tag falls back to animals`() {
        assertEquals(Category.ANIMALS, Category.fromTag(null))
        assertEquals(Category.ANIMALS, Category.fromTag("not-a-real-category"))
    }
}
