package com.example.crittertap.data

/** What the play screen shows: the animal critters, or human feelings. */
enum class Category(val tag: String) {
    ANIMALS("animals"),
    FEELINGS("feelings");

    companion object {
        fun fromTag(tag: String?): Category =
            entries.firstOrNull { it.tag == tag } ?: ANIMALS
    }
}
