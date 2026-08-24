package com.example.crittertap.audio

import com.example.crittertap.data.Critter
import com.example.crittertap.data.CritterCatalog
import com.example.crittertap.data.CritterText
import com.example.crittertap.data.CritterTexts
import com.example.crittertap.data.Language
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * The Wear emulator has no text-to-speech engine, so none of this can be
 * confirmed by listening. These tests are the only check that a tap produces
 * the description, then a pause, then the noise.
 */
class CritterVoiceTest {

    private val cat = CritterCatalog["cat"]
    private val text = CritterTexts.of("cat", Language.ENGLISH)

    private fun voice(
        engine: FakeSpeechEngine = FakeSpeechEngine(),
        player: FakeSoundPlayer = FakeSoundPlayer(),
        ready: Boolean = true,
    ): Triple<CritterVoice, FakeSpeechEngine, FakeSoundPlayer> {
        val v = CritterVoice(engine, player)
        engine.becomeReady(ready)
        return Triple(v, engine, player)
    }

    @Test
    fun `a tap speaks the description, then a gap, then the noise`() {
        val (v, engine, _) = voice()
        v.say(cat, text)

        val speech = engine.calls.filterIsInstance<FakeSpeechEngine.Call.Speak>()
        val gaps = engine.calls.filterIsInstance<FakeSpeechEngine.Call.Silence>()

        assertEquals(listOf(text.description, text.noise), speech.map { it.text })
        assertEquals(1, gaps.size)
        assertEquals(CritterVoice.GAP_MILLIS, gaps.single().millis)

        // and in that order, with the gap between the two
        val order = engine.calls.filter { it !is FakeSpeechEngine.Call.Stop }
        assertEquals(3, order.size)
        assertTrue(order[0] is FakeSpeechEngine.Call.Speak)
        assertTrue(order[1] is FakeSpeechEngine.Call.Silence)
        assertTrue(order[2] is FakeSpeechEngine.Call.Speak)
    }

    @Test
    fun `the description flushes the queue and the noise appends to it`() {
        val (v, engine, _) = voice()
        v.say(cat, text)
        val speech = engine.calls.filterIsInstance<FakeSpeechEngine.Call.Speak>()
        assertTrue("description should cut off whatever was playing", speech[0].flush)
        assertTrue("noise must not cut off the description", !speech[1].flush)
    }

    @Test
    fun `a request made before the engine is ready is spoken once it is`() {
        val engine = FakeSpeechEngine()
        val v = CritterVoice(engine, FakeSoundPlayer())
        assertEquals(CritterVoice.Status.Starting, v.status)

        v.say(cat, text)
        assertEquals("nothing should be spoken yet", emptyList<String>(), engine.spoken)

        engine.becomeReady()
        assertEquals(CritterVoice.Status.Ready, v.status)
        assertEquals(listOf(text.description, text.noise), engine.spoken)
    }

    @Test
    fun `a watch with no engine goes quiet instead of crashing`() {
        val (v, engine, _) = voice(ready = false)
        v.say(cat, text)
        assertEquals(CritterVoice.Status.Unavailable, v.status)
        assertEquals(emptyList<String>(), engine.spoken)
    }

    @Test
    fun `muting stops it speaking at all`() {
        val (v, engine, _) = voice()
        v.setVolume(0f)
        v.say(cat, text)
        assertEquals(emptyList<String>(), engine.spoken)
    }

    @Test
    fun `the volume setting reaches every utterance`() {
        val (v, engine, player) = voice()
        v.setVolume(0.4f)
        v.say(cat, text)
        val speech = engine.calls.filterIsInstance<FakeSpeechEngine.Call.Speak>()
        assertTrue(speech.isNotEmpty())
        assertTrue(speech.all { it.volume == 0.4f })
        assertEquals(0.4f, player.volume, 1e-6f)
    }

    @Test
    fun `volume is clamped to a sane range`() {
        val (v, _, player) = voice()
        v.setVolume(4f)
        assertEquals(1f, player.volume, 1e-6f)
        v.setVolume(-2f)
        assertEquals(0f, player.volume, 1e-6f)
    }

    @Test
    fun `switching language re-points the engine`() {
        val (v, engine, _) = voice()
        v.setLanguage(Language.SPANISH)
        assertEquals("es-ES", engine.languages.last().toLanguageTag())
        assertNull(v.missingVoiceFor)
    }

    @Test
    fun `a language the watch cannot speak is reported, not hidden`() {
        val engine = FakeSpeechEngine(supported = setOf("en-US"))
        val v = CritterVoice(engine, FakeSoundPlayer())
        engine.becomeReady()

        assertNull("English is fine on this pretend watch", v.missingVoiceFor)
        v.setLanguage(Language.SPANISH)
        assertEquals(Language.SPANISH, v.missingVoiceFor)

        v.setLanguage(Language.ENGLISH)
        assertNull("switching back should clear the warning", v.missingVoiceFor)
    }

    @Test
    fun `a bundled recording replaces the spoken noise and waits its turn`() {
        val engine = FakeSpeechEngine()
        val player = FakeSoundPlayer()
        val v = CritterVoice(engine, player)
        engine.becomeReady()

        val withSound = Critter(
            id = "cat", assetPath = cat.assetPath, accent = cat.accent, soundRes = 4242)
        v.say(withSound, text)

        assertEquals("only the description is spoken", listOf(text.description), engine.spoken)
        assertEquals("the recording waits for the description", emptyList<Pair<Int, Float>>(),
            player.played)

        engine.finish("cat${CritterVoice.DESCRIBE_SUFFIX}")
        assertEquals(listOf(4242 to 1f), player.played)
    }

    @Test
    fun `an unrelated utterance finishing does not fire the recording`() {
        val engine = FakeSpeechEngine()
        val player = FakeSoundPlayer()
        val v = CritterVoice(engine, player)
        engine.becomeReady()
        v.say(Critter("cat", cat.assetPath, cat.accent, soundRes = 7), text)

        engine.finish("cat-noise")
        engine.finish("cat-gap")
        assertEquals(emptyList<Pair<Int, Float>>(), player.played)
    }

    @Test
    fun `a new tap cuts off whatever was playing`() {
        val (v, engine, player) = voice()
        v.say(cat, text)
        val before = player.stops
        v.say(CritterCatalog["dog"], CritterTexts.of("dog", Language.ENGLISH))

        assertTrue("the engine should be stopped first",
            engine.calls.any { it is FakeSpeechEngine.Call.Stop })
        assertTrue("any recording should be stopped too", player.stops > before)
    }

    @Test
    fun `shutdown releases the engine`() {
        val (v, engine, _) = voice()
        v.shutdown()
        assertTrue(engine.calls.any { it is FakeSpeechEngine.Call.Shutdown })
        assertEquals(CritterVoice.Status.Unavailable, v.status)
    }

    @Test
    fun `each language speaks its own words`() {
        Language.entries.forEach { language ->
            val engine = FakeSpeechEngine()
            val v = CritterVoice(engine, FakeSoundPlayer())
            engine.becomeReady()
            v.setLanguage(language)

            val expected: CritterText = CritterTexts.of("cow", language)
            v.say(CritterCatalog["cow"], expected)
            assertEquals(listOf(expected.description, expected.noise), engine.spoken)
        }
    }
}
