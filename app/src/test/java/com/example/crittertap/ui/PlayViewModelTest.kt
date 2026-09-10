package com.example.crittertap.ui

import androidx.lifecycle.SavedStateHandle
import com.example.crittertap.data.CritterCatalog
import com.example.crittertap.data.Language
import com.example.crittertap.settings.ShufflingMode
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class PlayViewModelTest {

    private val critters = CritterCatalog.all

    @Test
    fun `initial state shows the first critter from the shuffler`() {
        val savedStateHandle = SavedStateHandle()
        val viewModel = PlayViewModel(savedStateHandle, critters.size)
        
        val state = viewModel.uiState.value
        assertEquals(critters[state.index], state.critter)
        assertEquals(0, state.interactions)
    }

    @Test
    fun `onSpeakTriggered increments interactions`() {
        val viewModel = PlayViewModel(SavedStateHandle(), critters.size)
        var spoken = false
        
        viewModel.onSpeakTriggered { _, _ -> spoken = true }
        
        assertEquals(1, viewModel.uiState.value.interactions)
        assertTrue(spoken)
    }

    @Test
    fun `onNextCritterTriggered moves to next critter and increments interactions`() {
        val viewModel = PlayViewModel(SavedStateHandle(), critters.size)
        val initialIndex = viewModel.uiState.value.index
        
        viewModel.onNextCritterTriggered { _, _ -> }
        
        val state = viewModel.uiState.value
        assertNotEquals(initialIndex, state.index)
        assertEquals(1, state.interactions)
    }

    @Test
    fun `onRotaryScroll moves by steps and increments interactions`() {
        val viewModel = PlayViewModel(SavedStateHandle(), critters.size)
        val initialIndex = viewModel.uiState.value.index
        
        // Use a step that is guaranteed to change the index if size > 1
        viewModel.onRotaryScroll(1) { _, _ -> }
        
        val state = viewModel.uiState.value
        assertEquals((initialIndex + 1) % critters.size, state.index)
        assertEquals(1, state.interactions)
    }

    @Test
    fun `onLanguageChanged updates text`() {
        val viewModel = PlayViewModel(SavedStateHandle(), critters.size)
        val englishText = viewModel.uiState.value.text
        
        viewModel.onLanguageChanged(Language.ENGLISH)
        viewModel.onLanguageChanged(Language.SPANISH)
        
        val spanishText = viewModel.uiState.value.text
        assertNotEquals(englishText, spanishText)
    }

    @Test
    fun `state survives restoration via SavedStateHandle`() {
        val savedStateHandle = SavedStateHandle()
        val viewModel1 = PlayViewModel(savedStateHandle, critters.size)
        viewModel1.onNextCritterTriggered { _, _ -> }
        val indexAfterNext = viewModel1.uiState.value.index
        val interactionsAfterNext = viewModel1.uiState.value.interactions

        // Create a new ViewModel with the same SavedStateHandle
        val viewModel2 = PlayViewModel(savedStateHandle, critters.size)
        assertEquals(indexAfterNext, viewModel2.uiState.value.index)
        assertEquals(interactionsAfterNext, viewModel2.uiState.value.interactions)
    }

    @Test
    fun `sequential mode follows catalog order`() {
        val viewModel = PlayViewModel(
            SavedStateHandle(), 
            catalogSize = 10, 
            shufflingMode = ShufflingMode.Sequential
        )
        
        // Check first 5 critters
        for (i in 0 until 5) {
            assertEquals(i, viewModel.uiState.value.index)
            viewModel.onNextCritterTriggered { _, _ -> }
        }
    }
}
