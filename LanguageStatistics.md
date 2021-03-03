# Grammar versus Lexicon

Broadly speaking, linguistic knowledge comes in two flavors: We know about the vocabulary or *lexicon* of a language, that is all the words, their meanings and connotations; and we know how to modify words and string them together to form sentences. Modifying a single word according to grammatical rules is the domain of *morphology*, while the rules that govern which word can come after which constitute the *syntax* of a language.

All of this is a vast simplification, of course; the boundary between morphology and syntax is fuzzy (see [haspelmath] for a discussion and look at the ‘n't’ in English ‘don't’ for a quick example). And while there are studies that distinguish between the brain action to recall lexical and grammatical knowledge [], down to showing that some grammatical features are stored together with the word inside your mental lexicon [], this is not a hard boundary either. [...].

So if we want to understand whether there is a difference in the sounds used for lexicon functions and those used for grammatical functions, like done in [] and suggested by some of my colleagues recently, we first need to be very careful in considering which sounds we count for one and which ones for the other. In the best case, the language is well-studied and has conventions for word boundaries, and the morphology works only concatenative, that is, by adding material (nothing like sing/sang/sung in the grammar where words change internally). Then we would know syntax and morphology explicitly, and we could clearly say for most [phonemes]() (sounds) whether they carry a lexical or grammatical function. There remain several broad classes of words that bear a lot of grammatical function. We would have to decide whether to count them as grammatical or lexical, but hopefully that could be done by class in a principled way.

Now, what kinds of sound patterns should we expect in such an ideal language? What would be a noteworthy difference between lexical and grammatical phonemes?
I wrote a small Python script that generates ‘sentences’ (without syntax or meaning, just following some general statistical patterns) in a synthetic language.

```{python}
import random
import bisect
from collections import Counter


class DiscreteProbabilities:
    def __init__(self, ps):
        keys, values = zip(*sorted(ps.items(), key=lambda kv: kv[1], reverse=True))
        self.values = numpy.cumsum(values)
        self.values /= self.values[-1]
        self.keys = keys

    def generate(self):
        x = numpy.random.random()
        i = bisect.bisect(self.values, x)
        return self.keys[i]


def phonemes():
    """Generate the phoneme inventory of a simulated language.
    
    The phonemes are 18 very frequent consonant phonemes in the languages of the world, and four vowels.
    They are each given probabilites according to some Zipf-like power law distribution.
    """
    return {
        "c": DiscreteProbabilities(
            {
                k: 1 / i
                for i, k in enumerate(
                    [
                        "p",
                        "b",
                        "t",
                        "d",
                        "c",
                        "k",
                        "g",
                        "'",
                        "f",
                        "s",
                        "h",
                        "m",
                        "n",
                        "ŋ",
                        "w",
                        "l",
                        "r",
                        "j",
                    ],
                    1,
                )
            }
        ),
        "v": DiscreteProbabilities({"a": 0.5, "ə": 0.33333333, "i": 0.25, "u": 0.2}),
    }


def morphemes(inventory):
    """Generate the morpheme inventory of a simulated language
    
    Generate random words with a CV syllable structure using the given phoneme inventory.
    Aggregate a dictionary of 1000 bisyllabic ‘nouns’, 10 monosyllabic ‘noun suffixes’, 1000 bisyllabic ‘verbs’, 10 monosyllabic ‘verb suffixes’, 100 monosyllabic ‘other words’ and 100 monosyllabic ‘other word affixes’.
    
    """
    nouns = DiscreteProbabilities(
        {
            (
                inventory["c"].generate(),
                inventory["v"].generate(),
                inventory["c"].generate(),
                inventory["v"].generate(),
            ): 1.0
            / i
            for i in range(1, 1001)
        }
    )
    noun_affixes = DiscreteProbabilities(
        {
            (inventory["c"].generate(), inventory["v"].generate()): 1.0 / i
            for i in range(1, 11)
        }
    )
    verbs = DiscreteProbabilities(
        {
            (
                inventory["c"].generate(),
                inventory["v"].generate(),
                inventory["c"].generate(),
                inventory["v"].generate(),
            ): 1.0
            / i
            for i in range(1, 1001)
        }
    )
    verb_affixes = DiscreteProbabilities(
        {
            (inventory["c"].generate(), inventory["v"].generate()): 1.0 / i
            for i in range(1, 11)
        }
    )
    other_lexicon = DiscreteProbabilities(
        {
            (inventory["c"].generate(), inventory["v"].generate()): 1.0 / i
            for i in range(1, 101)
        }
    )
    other_grammar = DiscreteProbabilities(
        {
            (inventory["c"].generate(), inventory["v"].generate()): 1.0 / i
            for i in range(1, 101)
        }
    )
    return {
        "n": nouns,
        "ng": noun_affixes,
        "v": verbs,
        "vg": verb_affixes,
        "o": other_lexicon,
        "og": other_grammar,
    }


def sentence(morphemes, g=Counter(), l=Counter()):
    """Generate a random sentence in a simulated language.
    
    Given a morpheme inventory, generate a sentence with 3 to 10 words. Each word is either a verb (probability 1/6) or a noun (probability 1/3) or another word (probability 1/2) and has random affix for its class with probability 1/2.
    
    Count the grammatical and lexical phonemes in the sentence separately, re-using the existing counter if none was passed.
    
    Returns:
      S: The sentence, as string
      G: The cumulative count of grammatical phonemes
      L: The cumulative count of lexical phonemes
    
    """
    s = ()
    for i in range(numpy.random.randint(3, 10)):
        segment = ["o", "o", "o", "n", "n", "v"][numpy.random.randint(6)]
        form = morphemes[segment].generate()
        if numpy.random.random() < 0.5:
            morph = morphemes[segment + "g"].generate()
        else:
            morph = ()
        s = s + form + morph + (" ",)
        g.update(morph)
        l.update(form)
    return "".join(s) + ".", g, l


# Generate 130 sentences in a random language

inventory = phonemes()
morphemes = morphemes(inventory)
for i in range(130):
    s, g, l = sentence(morphemes)
    print(s)
print(g)
print(l)
print(sum(g.values()) + sum(l.values()))
```

The output of this script might look like this.
```
```

Or the counts might look like this.
| Section   | Phonemes      |
| :-------- | :------------ |
| Lexicon   | ...           |
| Grammar   | ...           |

So, you see that there is an immense chance for random effects to accumulate. Making any sort of statistical statement about ‘grammatical’ vs. ‘lexical’ sounds won't get us very far. We might see some interesting patterns. But what they tell us is some rough indication of the morphology. And that we needed to know in much greater detail in the first place, in order to make the distinction between grammar and lexicon.
