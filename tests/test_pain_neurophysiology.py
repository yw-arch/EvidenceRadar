"""Check that the personal profile reaches the existing runtime without legacy queries."""

import unittest
from datetime import date
from pathlib import Path

from tools.radar_control import compile_runtime, load_master, load_master_runtime

ROOT = Path(__file__).resolve().parents[1]


class PainNeurophysiologyTests(unittest.TestCase):
    def test_profile_is_self_contained_and_keeps_source_stages(self):
        master = load_master(ROOT / "config/radar_master.json")
        runtime = compile_runtime(
            master, legacy_streams={}, legacy_scoring={},
            profile_id="pain_neurophysiology",
        )
        self.assertEqual(len(runtime.category_order), 6)
        self.assertEqual(set(runtime.scoring["categories"]), set(runtime.category_order))
        self.assertEqual(set(runtime.source_adapters), {"pubmed", "europe_pmc", "publisher"})
        self.assertEqual(
            runtime.streams["source_check_contract"]["bounded_verification_sources"],
            ["publisher"],
        )
        self.assertEqual(runtime.limits["verification"], master["limits"]["verification"])
        self.assertEqual(runtime.limits["selection"]["final_digest"], {"target": 18, "hard_max": 30})

    def test_provider_rewrite_preserves_scope_and_field_binding(self):
        from tools.run_github_radar_core import _europe_pmc_query

        runtime = load_master_runtime(ROOT / "config/radar_master.json", "pain_neurophysiology")
        for stream_id, stream in runtime.streams["streams"].items():
            with self.subTest(stream=stream_id):
                query, = stream["queries"]
                translated = _europe_pmc_query(query, date(2026, 9, 1), date(2026, 9, 3))
                self.assertNotIn("[Title/Abstract]", translated)
                self.assertEqual(translated.count("TITLE_ABS:"), query.count("[Title/Abstract]"))
                self.assertIn("2026-09-01", translated)
                if stream_id.endswith(("neurophysiology_eeg", "neuromodulation", "pain_rehabilitation")):
                    self.assertIn(") AND (", translated)

    def test_relevant_non_oa_abstracts_survive_metadata_threshold(self):
        from tools.run_github_radar_core import Candidate, score_candidate

        runtime = load_master_runtime(ROOT / "config/radar_master.json", "pain_neurophysiology")
        examples = {
            "pain_neuroscience": "We investigated central sensitization in adults.",
            "headache_migraine": "Participants had migraine.",
            "neurophysiology_eeg": "EEG was used to assess functional connectivity.",
            "neuromodulation": "Median nerve stimulation was investigated in migraine.",
            "qst_sensory_processing": "We measured conditioned pain modulation.",
            "pain_rehabilitation": "Physical therapy was investigated for chronic pain.",
        }
        for category, abstract in examples.items():
            stream_id = "pain_reader_" + category
            stream = runtime.streams["streams"][stream_id]
            candidate = Candidate(
                title="A mechanistic investigation", abstract=abstract,
                stream=stream_id, category=category, source="pubmed",
                publication_date="2026-09-02", pmid="12345678", open_access=False,
            )
            threshold = runtime.scoring["category_min_relevance"][category]
            with self.subTest(category=category):
                self.assertGreaterEqual(score_candidate(candidate, stream["relevance_terms"]), threshold)
                candidate.abstract = "Crop irrigation and soil moisture were measured."
                self.assertLess(score_candidate(candidate, stream["relevance_terms"]), threshold)


if __name__ == "__main__":
    unittest.main()
