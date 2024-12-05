# Copyright Jiaqi Liu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest

import yaml

from wilhelm_python_sdk.german_parser import get_declension_attributes
from wilhelm_python_sdk.vocabulary_parser import GERMAN
from wilhelm_python_sdk.vocabulary_parser import get_attributes
from wilhelm_python_sdk.vocabulary_parser import get_definition_tokens
from wilhelm_python_sdk.vocabulary_parser import get_definitions
from wilhelm_python_sdk.vocabulary_parser import get_inferred_links
from wilhelm_python_sdk.vocabulary_parser import \
    get_inferred_tokenization_links
from wilhelm_python_sdk.vocabulary_parser import get_inflection_tokens
from wilhelm_python_sdk.vocabulary_parser import get_structurally_similar_links
from wilhelm_python_sdk.vocabulary_parser import get_term_tokens
from wilhelm_python_sdk.vocabulary_parser import is_structurally_similar

UNKOWN_DECLENSION_NOUN_YAML = """
    term: die Grilltomate
    definition: the grilled tomato
    declension: Unknown
"""

LABEL_KEY = "label"


class TestVocabularyParser(unittest.TestCase):

    def test_get_definitions(self):
        self.assertEqual(
            [("adj.", "same"), ("adv.", "namely"), (None, "because")],
            get_definitions({
                "definition": ["(adj.) same", "(adv.) namely", "because"]
            }),
        )

    def test_single_definition_term(self):
        self.assertEqual(
            [(None, "one")],
            get_definitions({
                "definition": "one"
            }),
        )

    def test_numerical_definition(self):
        self.assertEqual(
            [(None, "1")],
            get_definitions({
                "definition": 1
            }),
        )

    def test_missing_definition(self):
        with self.assertRaises(ValueError):
            get_definitions({"defintion": "I'm 23 years old."})

    def test_get_attributes_basic(self):
        self.assertEqual(
            {"label": "der Hut", "language": "German"},
            get_attributes({"term": "der Hut", "definition": "the hat"}, GERMAN, LABEL_KEY),
        )

    def test_get_attributes_with_custom_inflection(self):
        self.assertEqual(
            {"label": "der Hut", "language": "German", "inflection": {"declension": "..."}},
            get_attributes(
                {
                    "term": "der Hut",
                    "definition": "the hat",
                    "inflection": {"declension": "...", "inflection": None}
                },
                GERMAN,
                LABEL_KEY,
                lambda word: {"inflection": {"declension": "..."}}
            ),
        )

    def test_get_attributes_with_audio(self):
        self.assertEqual(
            {
                "label": "der Hut",
                "language": "German",
                "audio": "https://upload.wikimedia.org/wikipedia/commons/e/e9/De-Hut.ogg"
            },
            get_attributes(
                {
                    "term": "der Hut",
                    "definition": "the hat",
                    "audio": "https://upload.wikimedia.org/wikipedia/commons/e/e9/De-Hut.ogg"
                },
                GERMAN,
                LABEL_KEY
            ),
        )

    def test_get_inferred_links_on_unrelated_terms(self):
        vocabulary = yaml.safe_load("""
            vocabulary:
              - term: der Beruf
                definition: job
                declension:
                  - ["",         singular,          plural ]
                  - [nominative, Beruf,             Berufe ]
                  - [genitive,   "Berufes, Berufs", Berufe ]
                  - [dative,     Beruf,             Berufen]
                  - [accusative, Beruf,             Berufe ]
              - term: der Qualitätswein
                definition: The vintage wine
                declension:
                  - ["",         singular,                          plural         ]
                  - [nominative, Qualitätswein,                     Qualitätsweine ]
                  - [genitive,   "Qualitätsweines, Qualitätsweins", Qualitätsweine ]
                  - [dative,     Qualitätswein,                     Qualitätsweinen]
                  - [accusative, Qualitätswein,                     Qualitätsweine ]
        """)["vocabulary"]
        label_key = LABEL_KEY

        self.assertEqual(
            [],
            get_inferred_links(vocabulary, label_key, get_declension_attributes)
        )

    def test_get_inferred_links_on_unrelated_terms_with_same_definite_article(self):
        vocabulary = yaml.safe_load("""
            vocabulary:
              - term: die Biographie
                definition: (alternative spelling of) die Biografie
                declension:
                  - ["",         singular,   plural     ]
                  - [nominative, Biographie, Biographien]
                  - [genitive,   Biographie, Biographien]
                  - [dative,     Biographie, Biographien]
                  - [accusative, Biographie, Biographien]
              - term: die Mittagspause
                definition: the lunchbreak
                declension:
                  - ["",         singular,     plural       ]
                  - [nominative, Mittagspause, Mittagspausen]
                  - [genitive,   Mittagspause, Mittagspausen]
                  - [dative,     Mittagspause, Mittagspausen]
                  - [accusative, Mittagspause, Mittagspausen]
        """)["vocabulary"]  # "die Biographie" has "die" in its definition
        label_key = LABEL_KEY

        self.assertEqual(
            [],
            get_inferred_links(vocabulary, label_key, get_declension_attributes)
        )

    def test_get_definition_tokens(self):
        vocabulary = yaml.safe_load("""
                    vocabulary:
                      - term: morgens
                        definition:
                          - (adv.) in the morning
                          - (adv.) a.m.
                """)["vocabulary"]
        self.assertEqual(
            {"morning", "a.m."},
            get_definition_tokens(vocabulary[0])
        )

    def test_get_term_tokens(self):
        vocabulary = yaml.safe_load("""
                    vocabulary:
                      - term: Viertel vor sieben
                        definition: (clock time) a quarter before eight
                """)["vocabulary"]
        self.assertEqual(
            {"sieben", "vor", "viertel"},
            get_term_tokens(vocabulary[0])
        )

    def test_get_term_tokens_do_not_include_indefinite_articles(self):
        vocabulary = yaml.safe_load("""
                    vocabulary:
                      - term: der Brief
                      - term: die Biographie
                      - term: das Jahr
                """)["vocabulary"]
        self.assertEqual({"brief"}, get_term_tokens(vocabulary[0]))
        self.assertEqual({"biographie"}, get_term_tokens(vocabulary[1]))
        self.assertEqual({"jahr"}, get_term_tokens(vocabulary[2]))

    def test_get_declension_tokens(self):
        vocabulary = yaml.safe_load("""
                    vocabulary:
                      - term: das Jahr
                        definition: the year
                        declension:
                          - ["",         singular,        plural        ]
                          - [nominative, Jahr,            "Jahre, Jahr" ]
                          - [genitive,   "Jahres, Jahrs", "Jahre, Jahr" ]
                          - [dative,     Jahr,            "Jahren, Jahr"]
                          - [accusative, Jahr,            "Jahre, Jahr" ]
                """)["vocabulary"]
        self.assertEqual(
            {"jahres", "jahre", "jahr", "jahren", "jahrs"},
            get_inflection_tokens(vocabulary[0], get_declension_attributes)
        )

    def test_two_words_shring_some_same_declension_table_entries(self):
        vocabulary = yaml.safe_load("""
            vocabulary:
              - term: die Reise
                definition: the travel
                declension:
                  - ["",         singular, plural]
                  - [nominative, Reise,    Reisen]
                  - [genitive,   Reise,    Reisen]
                  - [dative,     Reise,    Reisen]
                  - [accusative, Reise,    Reisen]
              - term: der Reis
                definition: the rice
                declension:
                  - ["",         singular, plural]
                  - [nominative, Reis,     Reise ]
                  - [genitive,   Reises,   Reise ]
                  - [dative,     Reis,     Reisen]
                  - [accusative, Reis,     Reise ]
        """)["vocabulary"]

        self.assertEqual(
            [
                {
                    'attributes': {LABEL_KEY: 'term related'},
                    'source_label': 'die Reise',
                    'target_label': 'der Reis'
                }
            ],
            get_inferred_tokenization_links(vocabulary, LABEL_KEY, get_declension_attributes)
        )

    def test_get_inferred_tokenization_links(self):
        vocabulary = yaml.safe_load("""
            vocabulary:
              - term: das Jahr
                definition: the year
                declension:
                  - ["",         singular,        plural        ]
                  - [nominative, Jahr,            "Jahre, Jahr" ]
                  - [genitive,   "Jahres, Jahrs", "Jahre, Jahr" ]
                  - [dative,     Jahr,            "Jahren, Jahr"]
                  - [accusative, Jahr,            "Jahre, Jahr" ]
              - term: seit zwei Jahren
                definition: for two years
              - term: letzte
                definition: (adj.) last
              - term: in den letzten Jahren
                definition: in recent years
        """)["vocabulary"]

        self.assertEqual(
            [
                {
                    'attributes': {LABEL_KEY: 'term related'},
                    'source_label': 'seit zwei Jahren',
                    'target_label': 'das Jahr'
                },
                {
                    'attributes': {LABEL_KEY: 'term related'},
                    'source_label': 'seit zwei Jahren',
                    'target_label': 'in den letzten Jahren'
                },
                {
                    'attributes': {LABEL_KEY: 'term related'},
                    'source_label': 'in den letzten Jahren',
                    'target_label': 'das Jahr'
                },
                {
                    'attributes': {LABEL_KEY: 'term related'},
                    'source_label': 'in den letzten Jahren',
                    'target_label': 'seit zwei Jahren'
                }
            ],
            get_inferred_tokenization_links(vocabulary, LABEL_KEY, get_declension_attributes)
        )

    def test_get_structurally_similar_links(self):
        vocabulary = yaml.safe_load("""
            vocabulary:
              - term: anschließen
                definition: to connect
              - term: anschließend
                definition:
                  - (adj.) following
                  - (adv.) afterwards
              - term: nachher
                definition: (adv.) afterwards
        """)["vocabulary"]
        label_key = LABEL_KEY

        self.assertEqual(
            [
                {
                    'attributes': {LABEL_KEY: 'structurally similar'},
                    'source_label': 'anschließen',
                    'target_label': 'anschließend'
                },
                {
                    'attributes': {LABEL_KEY: 'structurally similar'},
                    'source_label': 'anschließend',
                    'target_label': 'anschließen'
                }
            ],
            get_structurally_similar_links(vocabulary, label_key)
        )

    def test_get_structurally_similar_links_small_edit_distance_but_different_stem(self):
        vocabulary = yaml.safe_load("""
            vocabulary:
              - term: die Bank
              - term: die Sahne
        """)["vocabulary"]
        label_key = LABEL_KEY

        self.assertEqual(
            [],
            get_structurally_similar_links(vocabulary, label_key)
        )

    def test_is_structurally_similar(self):
        self.assertTrue(is_structurally_similar("anschließen", "anschließend"))
        self.assertTrue(is_structurally_similar("anschließend", "anschließen"))
        self.assertFalse(is_structurally_similar("die Bank", "die Sahne"))
