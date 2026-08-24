package com.example.crittertap.data

import java.util.Locale

/** The languages the app speaks and writes in. */
enum class Language(val tag: String, val label: String) {
    ENGLISH("en-US", "English"),
    SPANISH("es-ES", "Español");

    val locale: Locale get() = Locale.forLanguageTag(tag)

    companion object {
        fun fromTag(tag: String?): Language =
            entries.firstOrNull { it.tag == tag } ?: ENGLISH
    }
}
