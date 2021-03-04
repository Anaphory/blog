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
and an inherited component shared by all the languages of a family.

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
This is the domain we know least about. We choose a very broad prior for this, a
flat Dirichlet prior for every feature (i.e. Dirichlet(1, 1, 1, 1, 1, 1, 1) for
the basic word order feature), because that makes the outcomes very obvious and
interpretable.

## Inherited features

The main issue lies with the third random component. In the original publication, 
