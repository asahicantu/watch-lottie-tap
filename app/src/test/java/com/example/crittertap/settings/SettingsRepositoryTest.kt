package com.example.crittertap.settings

import com.example.crittertap.data.Category
import com.example.crittertap.data.CritterCatalog
import com.example.crittertap.data.FeelingCatalog
import org.junit.Assert.assertEquals
import org.junit.Test

class SettingsRepositoryTest {

    @Test
    fun `the catalog size cap matches the selected category`() {
        assertEquals(CritterCatalog.all.size, SettingsRepository.maxCatalogSizeFor(Category.ANIMALS))
        assertEquals(FeelingCatalog.all.size, SettingsRepository.maxCatalogSizeFor(Category.FEELINGS))
    }
}
