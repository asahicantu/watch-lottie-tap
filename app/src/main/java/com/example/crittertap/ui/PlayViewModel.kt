package com.example.crittertap.ui

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.createSavedStateHandle
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.crittertap.data.Critter
import com.example.crittertap.data.CritterCatalog
import com.example.crittertap.data.CritterShuffler
import com.example.crittertap.data.CritterText
import com.example.crittertap.data.CritterTexts
import com.example.crittertap.data.Language
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

/**
 * UI state for the Play Screen.
 *
 * @property critter The critter currently being shown.
 * @property text The localized description and noise for the critter.
 * @property interactions How many times the user has poked a critter in this session.
 * Used to trigger animations and track progress through hints.
 * @property index The current critter's position in the catalog.
 */
data class PlayUiState(
    val critter: Critter,
    val text: CritterText,
    val interactions: Int = 0,
    val index: Int
)

private const val KEY_SHUFFLER_STATE = "shuffler_state"
private const val KEY_INTERACTIONS = "interactions"

/**
 * ViewModel for the Play Screen, managing the critter catalog, shuffling,
 * and current interaction state.
 *
 * This survives configuration changes and, via [SavedStateHandle], process death.
 */
class PlayViewModel(
    private val savedStateHandle: SavedStateHandle,
    private val critters: List<Critter> = CritterCatalog.all,
) : ViewModel() {

    private val shuffler = CritterShuffler(critters.size).apply {
        savedStateHandle.get<List<Int>>(KEY_SHUFFLER_STATE)?.let { restore(it) }
    }

    private val _uiState = MutableStateFlow(
        PlayUiState(
            critter = critters[shuffler.current.takeIf { it >= 0 } ?: shuffler.next().also { saveShuffler() }],
            text = CritterTexts.of(critters[shuffler.current].id, Language.ENGLISH), // Initial, will be updated by Screen
            index = shuffler.current,
            interactions = savedStateHandle[KEY_INTERACTIONS] ?: 0
        )
    )

    /** The current state of the play screen. */
    val uiState: StateFlow<PlayUiState> = _uiState.asStateFlow()

    private var currentLanguage = Language.ENGLISH

    /** Updates the state with the current [Language] and its associated text. */
    fun onLanguageChanged(newLanguage: Language) {
        currentLanguage = newLanguage
        _uiState.update { it.copy(text = CritterTexts.of(it.critter.id, newLanguage)) }
    }

    /** Triggers the voice for the current critter and increments interactions. */
    fun onSpeakTriggered(onSpeak: (Critter, CritterText) -> Unit) {
        val newInteractions = _uiState.value.interactions + 1
        savedStateHandle[KEY_INTERACTIONS] = newInteractions
        _uiState.update { it.copy(interactions = newInteractions) }
        onSpeak(_uiState.value.critter, _uiState.value.text)
    }

    /** Moves to the next critter in the deck and increments interactions. */
    fun onNextCritterTriggered(onIntroduce: (Critter, CritterText) -> Unit) {
        val nextIndex = shuffler.next()
        saveShuffler()
        updateCritter(nextIndex, onIntroduce)
    }

    /** Jumps to a specific critter based on rotary input steps. */
    fun onRotaryScroll(steps: Int, onIntroduce: (Critter, CritterText) -> Unit) {
        if (steps == 0) return
        val size = critters.size
        val nextIndex = ((_uiState.value.index + steps) % size + size) % size
        shuffler.jumpTo(nextIndex)
        saveShuffler()
        updateCritter(nextIndex, onIntroduce)
    }

    private fun updateCritter(index: Int, onIntroduce: (Critter, CritterText) -> Unit) {
        val critter = critters[index]
        val text = CritterTexts.of(critter.id, currentLanguage)
        val newInteractions = _uiState.value.interactions + 1
        savedStateHandle[KEY_INTERACTIONS] = newInteractions
        _uiState.update {
            it.copy(
                critter = critter,
                text = text,
                index = index,
                interactions = newInteractions
            )
        }
        onIntroduce(critter, text)
    }

    private fun saveShuffler() {
        savedStateHandle[KEY_SHUFFLER_STATE] = shuffler.state
    }

    companion object {
        /** Default factory for creating [PlayViewModel] with [SavedStateHandle]. */
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val savedStateHandle = createSavedStateHandle()
                PlayViewModel(savedStateHandle)
            }
        }
    }
}
