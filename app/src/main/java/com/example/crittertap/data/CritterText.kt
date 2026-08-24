package com.example.crittertap.data

/**
 * What the watch shows and says for one critter.
 *
 * A single tap speaks [description] and then [noise] — first the words that
 * describe the animal, then the sound the animal makes.
 */
data class CritterText(
    val label: String,
    val description: String,
    val noise: String,
)

object CritterTexts {

    private val english = mapOf(
        "cat" to CritterText("Cat", "A cat. It has soft paws and sharp claws.", "Meow! Meow!"),
        "dog" to CritterText("Dog", "A dog. It wags its tail when it is happy.", "Woof! Woof!"),
        "cow" to CritterText("Cow", "A cow. It grazes in the field all day.", "Mooo!"),
        "duck" to CritterText("Duck", "A duck. It paddles across the pond.", "Quack! Quack!"),
        "frog" to CritterText("Frog", "A frog. It hops and catches flies.", "Ribbit! Ribbit!"),
        "lion" to CritterText("Lion", "A lion. It has a great golden mane.", "Roaaar!"),
        "bee" to CritterText("Bee", "A bee. It gathers nectar from the flowers.", "Bzzzzz!"),
        "sheep" to CritterText("Sheep", "A sheep. Its wool is thick and warm.", "Baaa!"),
        "owl" to CritterText("Owl", "An owl. It hunts quietly at night.", "Hoo! Hoo!"),
        "pig" to CritterText("Pig", "A pig. It loves rolling in the mud.", "Oink! Oink!"),
        "horse" to CritterText("Horse", "A horse. It gallops across the meadow.", "Neigh!"),
        "elephant" to CritterText("Elephant", "An elephant. It drinks with its long trunk.", "Pawooo!"),
        "monkey" to CritterText("Monkey", "A monkey. It swings from tree to tree.", "Ooh ooh ah ah!"),
        "penguin" to CritterText("Penguin", "A penguin. It slides across the ice.", "Squawk! Squawk!"),
        "tiger" to CritterText("Tiger", "A tiger. Its orange coat is full of stripes.", "Rrrroar!"),
        "bear" to CritterText("Bear", "A bear. It sleeps all through the winter.", "Grrrr!"),
        "rabbit" to CritterText("Rabbit", "A rabbit. It hops fast on long back legs.", "Thump! Thump!"),
        "mouse" to CritterText("Mouse", "A mouse. It is tiny and nibbles at the cheese.", "Squeak! Squeak!"),
        "fox" to CritterText("Fox", "A fox. It is clever and very quick.", "Yip! Yip!"),
        "wolf" to CritterText("Wolf", "A wolf. It howls at the moon.", "Awoooo!"),
        "rooster" to CritterText("Rooster", "A rooster. It wakes the farm at sunrise.", "Cock-a-doodle-doo!"),
        "goat" to CritterText("Goat", "A goat. It climbs the steepest rocks.", "Maaa! Maaa!"),
        "donkey" to CritterText("Donkey", "A donkey. It carries the heavy loads.", "Hee-haw! Hee-haw!"),
        "panda" to CritterText("Panda", "A panda. It eats bamboo all day long.", "Bleat! Bleat!"),
        "koala" to CritterText("Koala", "A koala. It sleeps up in the eucalyptus tree.", "Grunt! Grunt!"),
        "giraffe" to CritterText("Giraffe", "A giraffe. Its neck reaches the tallest leaves.", "Hummm!"),
        "hippo" to CritterText("Hippo", "A hippo. It wallows in the warm river.", "Snort! Snort!"),
        "crocodile" to CritterText("Crocodile", "A crocodile. It waits quietly in the water.", "Snap! Snap!"),
        "snake" to CritterText("Snake", "A snake. It slithers through the grass.", "Hisssss!"),
        "parrot" to CritterText("Parrot", "A parrot. It copies the words that you say.", "Squawk! Hello!"),
    )

    private val spanish = mapOf(
        "cat" to CritterText("Gato", "Un gato. Tiene patas suaves y garras afiladas.", "¡Miau! ¡Miau!"),
        "dog" to CritterText("Perro", "Un perro. Mueve la cola cuando está contento.", "¡Guau! ¡Guau!"),
        "cow" to CritterText("Vaca", "Una vaca. Pasta en el campo todo el día.", "¡Muuu!"),
        "duck" to CritterText("Pato", "Un pato. Nada por el estanque.", "¡Cuac! ¡Cuac!"),
        "frog" to CritterText("Rana", "Una rana. Salta y caza moscas.", "¡Croac! ¡Croac!"),
        "lion" to CritterText("León", "Un león. Tiene una gran melena dorada.", "¡Grrroar!"),
        "bee" to CritterText("Abeja", "Una abeja. Recoge néctar de las flores.", "¡Bzzzzz!"),
        "sheep" to CritterText("Oveja", "Una oveja. Su lana es espesa y cálida.", "¡Beee!"),
        "owl" to CritterText("Búho", "Un búho. Caza en silencio por la noche.", "¡Uh! ¡Uh!"),
        "pig" to CritterText("Cerdo", "Un cerdo. Le encanta revolcarse en el barro.", "¡Oink! ¡Oink!"),
        "horse" to CritterText("Caballo", "Un caballo. Galopa por la pradera.", "¡Iiiih!"),
        "elephant" to CritterText("Elefante", "Un elefante. Bebe con su larga trompa.", "¡Pruuu!"),
        "monkey" to CritterText("Mono", "Un mono. Se columpia de árbol en árbol.", "¡U u ah ah!"),
        "penguin" to CritterText("Pingüino", "Un pingüino. Se desliza sobre el hielo.", "¡Uak! ¡Uak!"),
        "tiger" to CritterText("Tigre", "Un tigre. Su pelaje naranja está lleno de rayas.", "¡Grrroar!"),
        "bear" to CritterText("Oso", "Un oso. Duerme durante todo el invierno.", "¡Grrrr!"),
        "rabbit" to CritterText("Conejo", "Un conejo. Salta rápido con sus patas traseras.", "¡Tup! ¡Tup!"),
        "mouse" to CritterText("Ratón", "Un ratón. Es diminuto y mordisquea el queso.", "¡Iik! ¡Iik!"),
        "fox" to CritterText("Zorro", "Un zorro. Es astuto y muy veloz.", "¡Yip! ¡Yip!"),
        "wolf" to CritterText("Lobo", "Un lobo. Aúlla a la luna.", "¡Auuuu!"),
        "rooster" to CritterText("Gallo", "Un gallo. Despierta la granja al amanecer.", "¡Quiquiriquí!"),
        "goat" to CritterText("Cabra", "Una cabra. Trepa por las rocas más empinadas.", "¡Meee! ¡Meee!"),
        "donkey" to CritterText("Burro", "Un burro. Carga con los fardos más pesados.", "¡Hiaaa! ¡Hiaaa!"),
        "panda" to CritterText("Panda", "Un panda. Come bambú todo el día.", "¡Beee! ¡Beee!"),
        "koala" to CritterText("Koala", "Un koala. Duerme en lo alto del eucalipto.", "¡Gruu! ¡Gruu!"),
        "giraffe" to CritterText("Jirafa", "Una jirafa. Su cuello alcanza las hojas más altas.", "¡Mmmm!"),
        "hippo" to CritterText("Hipopótamo", "Un hipopótamo. Se revuelca en el río templado.", "¡Grunf! ¡Grunf!"),
        "crocodile" to CritterText("Cocodrilo", "Un cocodrilo. Espera en silencio dentro del agua.", "¡Clac! ¡Clac!"),
        "snake" to CritterText("Serpiente", "Una serpiente. Se desliza entre la hierba.", "¡Sssss!"),
        "parrot" to CritterText("Loro", "Un loro. Repite las palabras que le dices.", "¡Grak! ¡Hola!"),
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
