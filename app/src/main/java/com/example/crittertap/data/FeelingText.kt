package com.example.crittertap.data

/**
 * What the watch shows and says for one feeling. Mirrors [CritterTexts], but
 * every entry's `noise` is null — a feeling makes no sound of its own, so a
 * tap speaks only its description.
 */
object FeelingTexts {

    private val english = mapOf(
        "happy" to CritterText("Happy", "Happy. A warm, bright feeling when everything is good."),
        "sad" to CritterText("Sad", "Sad. A heavy feeling when you miss something or someone."),
        "angry" to CritterText("Angry", "Angry. A hot feeling when something feels unfair."),
        "scared" to CritterText("Scared", "Scared. A jumpy feeling when something feels dangerous."),
        "surprised" to CritterText("Surprised", "Surprised. A sudden feeling when something you did not expect happens."),
        "disgusted" to CritterText("Disgusted", "Disgusted. A wrinkled-nose feeling when something is yucky."),
        "calm" to CritterText("Calm", "Calm. A quiet, peaceful feeling when everything is still."),
        "excited" to CritterText("Excited", "Excited. A bouncy feeling when something fun is about to happen."),
        "tired" to CritterText("Tired", "Tired. A sleepy feeling when your body wants to rest."),
        "proud" to CritterText("Proud", "Proud. A tall feeling when you did something well."),
        "embarrassed" to CritterText("Embarrassed", "Embarrassed. A shy, blushing feeling when everyone is looking at you."),
        "confused" to CritterText("Confused", "Confused. A puzzled feeling when something does not make sense."),
        "jealous" to CritterText("Jealous", "Jealous. A wanting feeling when someone else has something you like."),
        "grateful" to CritterText("Grateful", "Grateful. A thankful feeling when someone is kind to you."),
        "lonely" to CritterText("Lonely", "Lonely. A feeling of missing company when you are on your own."),
        "hopeful" to CritterText("Hopeful", "Hopeful. A hopeful feeling that something good is coming."),
        "nervous" to CritterText("Nervous", "Nervous. A fluttery feeling before doing something new."),
        "bored" to CritterText("Bored", "Bored. A flat feeling when there is nothing to do."),
        "curious" to CritterText("Curious", "Curious. A wondering feeling when you want to know more."),
        "loving" to CritterText("Loving", "Loving. A warm feeling of caring about someone very much."),
    )

    private val spanish = mapOf(
        "happy" to CritterText("Feliz", "Feliz. Una sensación cálida y brillante cuando todo va bien."),
        "sad" to CritterText("Triste", "Triste. Una sensación pesada cuando echas de menos algo o a alguien."),
        "angry" to CritterText("Enfadado", "Enfadado. Una sensación caliente cuando algo parece injusto."),
        "scared" to CritterText("Asustado", "Asustado. Una sensación de sobresalto cuando algo parece peligroso."),
        "surprised" to CritterText("Sorprendido", "Sorprendido. Una sensación repentina cuando pasa algo que no esperabas."),
        "disgusted" to CritterText("Asqueado", "Asqueado. Una sensación de arrugar la nariz cuando algo da asco."),
        "calm" to CritterText("Tranquilo", "Tranquilo. Una sensación silenciosa y en paz cuando todo está en calma."),
        "excited" to CritterText("Emocionado", "Emocionado. Una sensación saltarina cuando algo divertido va a pasar."),
        "tired" to CritterText("Cansado", "Cansado. Una sensación de sueño cuando tu cuerpo quiere descansar."),
        "proud" to CritterText("Orgulloso", "Orgulloso. Una sensación de crecer por dentro cuando haces algo bien."),
        "embarrassed" to CritterText("Avergonzado", "Avergonzado. Una sensación tímida y de sonrojo cuando todos te miran."),
        "confused" to CritterText("Confundido", "Confundido. Una sensación de duda cuando algo no tiene sentido."),
        "jealous" to CritterText("Celoso", "Celoso. Una sensación de querer algo que tiene otra persona."),
        "grateful" to CritterText("Agradecido", "Agradecido. Una sensación de gratitud cuando alguien es amable contigo."),
        "lonely" to CritterText("Solo", "Solo. Una sensación de extrañar compañía cuando estás sin nadie."),
        "hopeful" to CritterText("Esperanzado", "Esperanzado. Una sensación de esperanza de que algo bueno va a llegar."),
        "nervous" to CritterText("Nervioso", "Nervioso. Una sensación de cosquillas antes de hacer algo nuevo."),
        "bored" to CritterText("Aburrido", "Aburrido. Una sensación plana cuando no hay nada que hacer."),
        "curious" to CritterText("Curioso", "Curioso. Una sensación de preguntarte cuando quieres saber más."),
        "loving" to CritterText("Cariñoso", "Cariñoso. Una sensación cálida de querer mucho a alguien."),
    )

    private fun table(language: Language) = when (language) {
        Language.ENGLISH -> english
        Language.SPANISH -> spanish
    }

    /** Falls back to English so a half-translated catalog still shows something. */
    fun of(id: String, language: Language): CritterText =
        table(language)[id] ?: english.getValue(id)

    /** Ids that have no entry in [language] — used by the tests to catch gaps. */
    fun missingIn(language: Language, ids: Collection<String>): List<String> =
        ids.filterNot { table(language).containsKey(it) }
}
