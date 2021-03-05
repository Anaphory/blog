# I know that I know nothing

A *linguistic area*, also known as a *Sprachbund* (a German loan word that means
“language federation”), is a region where the languages have acquired structural
similarities through language contact. Examples for such features are definite
articles attached to the noun in the Balkans; click consonants in many southern
African languages; or suffixes as verbal person markers in languages of the
Andes. Another explanation for structural similarities is that languages
inherited them from a common ancestor, like the fact that European languages
mark the person and number of the subject (I vs. it vs. we etc.) using suffixes
on verbs (eg. ENG put/puts, DEU lege/legt/legen). Because of this, language
areas that connect unrelated or distantly related languages are particularly
clear-cut and interesting for the study of language contact.

Two of my colleagues have written [‘sbayes’, a tool to analyse linguistic
areas](https://github.com/derpetermann/sbayes) [@ranacher2021sbayes]. This is
interesting to our project [“Out of
Asia”](https://www.outofasia.uzh.ch/en.html), which aims to understand the
linguistic diversity of the Americas. (The name alludes to the “Out of Africa”
theory, which explains human diversity worldwide based on the fact that humans
evolved in Africa.) In the initial publication, sbayes was applied to the
Balkans and to Andes, two parts of the world that are well-known to be
interesting for areal linguistics. Now we want to apply it to topological data
for the Americas, to find quantitative evidence for linguistic areas that have
been proposed based on impressionistic observations and limited data before.

The model behind sbayes is a spatial Bayesian model (as the name alludes to).
Using three different random components, it tries to find consistent
explanations (high likelihood and high prior probability) for the structural
features of the languages in the sample. The three components are a contribution
from universal tendencies in language (eg. due to biases in cognitive
processes), contributions from the linguistic area a language may be part of,
and an inherited component shared by all the languages of a family. In addition
to these three contributions, sbayes infers the weight with which they influence
our observations.

Let us look at the order of Subject, Verb and Object as one example for a
feature. In reality, some of our features are very specific, so they are not
generally described in big databases. This means some colleagues in the
linguistics department are going through great lengths to extract the data we
need from well-chosen grammars (documents describing the linguistic system of a
language). But for illustrating the S/V/O word order feature, we can use
existing typological databases: The World Atlas of Language structures, WALS
[@wals], contains “Order of Subject, Object and Verb” as [feature
81A](https://wals.info/feature/81A), and the South American Indigenous Language
Structures database, SAILS, has it as [feature
NP2](https://sails.clld.org/parameters/NP2#5/1.746/289.565).

## Universal tendencies

The first random component is a base line, given by the universal distribution
of the feature in the languages of the world. Of course, this universal
distribution is not actually known, but we can take a careful sample of
languages worldwide and assume that it contains enough information to narrow
down at least a ‘hyperprior’ for the universal distribution for that feature.
Because we don't want to double-use data points, and because we want our sample
for the Americas to be as dense as possible, we need the hyperprior to be
informed by the non-American languages only.

```

```

So we count the following frequencies of the different word orders outside the Americas.

| Word order        | Count |
| :---------        | ----: |
| No dominant order |    76 |
| SOV               |   129 |
| SVO               |    40 |
| VSO               |    38 |
| VOS               |    11 |
| OVS               |     7 |
| OSV               |     1 |

We can then assume that the universal tendency for word order might follow (at
least very roughly – there are more elaborate ways to infer this) a Dirichlet
prior with weights 77, 130, 41, 39, 11, 8, and 2.

## Areality of features

The second random component deals with the contribution of each linguistic area.
The question which language features are easily or rarely transmitted through
areal diffusion is the domain of these three we know least about. Because this
is the intended research outcome, there is nothing much to say about it a
priori. Instead, we want to generate results in a data-driven way. We choose a
very broad prior for this, a flat Dirichlet prior for every feature (i.e.
Dirichlet(1, 1, 1, 1, 1, 1, 1) for the basic word order feature), because that
makes the outcomes very obvious and interpretable: The outcome will tell us how
many languages would *effectively* have each feature, if influences from
language families and universal tendencies didn't exist.

## Inherited features

The main issue lies with the third random component. In the original
publication, the sample did not cover any language family exhaustively. If that
is the case, we can use the features of related languages outside our sample to
inform the prior for each family inside the sample. This is a bit coarse,
presumably the languages inside the sample are near each other and because they
are more closely related to each other than to languages outside the sample. But
we currently don't take the closeness of relation into account anyway, there is
only one level: related or unrelated. So this is appropriate for the level we
model – and if the majority of languages from a family is inside the sample, the
prior is not very strong and easily overruled by the family members inside the
sample.

But how should we deal with the situation where one language family is
completely inside our sample? When we run our model on the entire two continents
of North and South America, nearly all language families will be either
completely inside or completely outside our sample. The exceptions are the one
or two language families spoken in Siberia and North America, namely
Eskimo-Aleut and Dené-Yeniseian. (The connection between Na-Dené languages and
Yeniseian languages is still discussed in linguistics, and I know too little
about them to decide whether to count them or not.) If we were to follow the
argument from the previous paragraph, we would assume that we have no data
outside the sample, and therefore use a flat prior.

But actually, we know a bit more than nothing about language families for which
we know nothing specific a priori. If we go back in time, our underlying
universal distribution presumably stays the same. This assumption is known as
‘Uniformitarian Hypothesis’. It is not actually true (eg.
[phonemes](PhonemeFrequencies.md) have been shown to be influenced by food
habits, and thus change over time [@blasi]) – and definitely quite wrong when
applied to the realized relative frequencies, instead of the underlying
distribution. However, it's still a useful first approximation.

By this assumption, the ancestral language of a family has features ‘randomly
drawn’ according to the universal background distribution. This may be, in
itself, an outlier in that distribution. If we were to isolate each descendant
languages and wait an extremely long time, we would expect to see the universal
distribution again. For present-day languages, we will observe something in
between: The descendants of a common ancestor are not going to be as widely
distributed as languages overall, but they are also not identical to each other
and their common ancestor.

If we quantify where a ‘typical’ feature in a ‘typical’ language family is on
the path from a homgenous state, potentially an outlier in the universal
distribution, towards showing the universal distribution itself, we can use this
knowledge for the language families we know nothing about. (Of course, we are
thinking in a Bayesian way here, so we are not just assuming one typical thing,
but all the possible things with their probabilities. But that's hard to phrase
without formulas.)

But! Now, we are looking to infer, in a data-driven way, the weight of the
feature of the common ancestor of a family versus the weight of the universal
background distribution it refers to. This is exactly one of the tasks sbayes
was built for: Instead of three weights – between the universal background, the
areas and the families – we need only two weights; and instead of inferring
effective frequencies, we want to get the likely feature configuration of the
ancestor of the language family.

Our actual language sample for the Americas study tries to maximize the number
of independent data points and therefore contains only one or two languages per
family, so we cannot use that. That's actually a benefit in disguise: We should
not use the same data twice, once to infer probability distributions and once to
use those probability distributions as priors for an analysis using the same
data and use these weights in the process afterwards.
