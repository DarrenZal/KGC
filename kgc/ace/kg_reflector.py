"""
KG Reflector Agent

Uses Claude Sonnet 4.5 to analyze knowledge graph extraction quality
and identify improvement opportunities.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

import anthropic


class KGReflectorAgent:
    """
    The KG Reflector analyzes extracted knowledge graphs to identify:
    - Quality issues (pronouns, lists, reversed authorship, etc.)
    - Root causes in code/prompts/configs
    - Specific, actionable improvement recommendations

    Uses Claude Sonnet 4.5 for superior analytical reasoning.
    """

    def __init__(
        self,
        playbook_path: str = "/home/claudeuser/yonearth-gaia-chatbot/kg_extraction_playbook",
        model: str = "claude-sonnet-4-5-20250929"
    ):
        self.playbook_path = Path(playbook_path)
        self.model = model

        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

        self.client = anthropic.Anthropic(api_key=api_key)

    def analyze_kg_extraction(
        self,
        relationships: List[Dict[str, Any]],
        source_text: str,
        extraction_metadata: Dict[str, Any],
        v4_quality_reports: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze knowledge graph extraction quality.

        Args:
            relationships: Extracted relationships from current version
            source_text: Original book text
            extraction_metadata: Extraction run information
            v4_quality_reports: Historical quality reports for training

        Returns:
            Quality analysis report with issues and recommendations
        """
        # Build analysis prompt
        prompt = self._build_analysis_prompt(
            relationships,
            source_text,
            extraction_metadata,
            v4_quality_reports
        )

        # Run Claude Sonnet 4.5 analysis
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16000,  # Allow for detailed analysis
            temperature=0.3,  # Lower for analytical tasks
            system=self._get_reflector_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Parse response
        analysis_text = response.content[0].text

        # Extract JSON from response (Claude may wrap it in markdown)
        try:
            if "```json" in analysis_text:
                json_start = analysis_text.find("```json") + 7
                json_end = analysis_text.find("```", json_start)
                json_str = analysis_text[json_start:json_end].strip()
            else:
                json_str = analysis_text

            analysis = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse JSON from Claude response: {e}")
            print(f"Response text: {analysis_text[:500]}...")
            # Return basic structure with raw text
            analysis = {
                "error": "json_parse_failed",
                "raw_response": analysis_text
            }

        # Enhance with metadata
        analysis["metadata"] = {
            "analysis_date": datetime.now().isoformat(),
            "relationships_analyzed": len(relationships),
            "reflector_version": "1.0_claude",
            "model_used": self.model,
            "extraction_version": extraction_metadata.get("version", "unknown")
        }

        # Save analysis
        self._save_analysis(analysis, extraction_metadata.get("version", "unknown"))

        return analysis

    def _get_reflector_system_prompt(self) -> str:
        """System prompt for Claude Sonnet 4.5 Reflector."""
        return """You are an expert QA analyst for knowledge graph extraction systems. Your role is to analyze extracted knowledge graphs and identify quality issues that need to be fixed.

You are analyzing relationships extracted from books using a multi-stage pipeline:
- Pass 1: LLM extraction of entities and relationships (PROMPT-DRIVEN)
- Type Validation: Filter invalid entity types
- Pass 2: Dual-signal evaluation (text confidence + knowledge plausibility) (PROMPT-DRIVEN)
- Pass 2.5: Post-processing with 7 modules (pronoun resolution, list splitting, etc.) (CODE-DRIVEN)

CRITICAL: You can now analyze and recommend changes to BOTH code AND prompts!

KNOWN ERROR PATTERNS FROM V4 (use as training data):
1. **Reversed Authorship** (12%): Book titles as source instead of author
   - Example: (Permaculture Manual, authored, Bill Mollison) ❌
   - Should be: (Bill Mollison, authored, Permaculture Manual) ✅

2. **List Targets** (11.5%): Comma-separated items in single relationship
   - Example: (biochar, used for, houseplants, gardens, yards) ❌
   - Should be 3 separate relationships ✅

3. **Pronoun Sources/Targets** (8.6%): "He", "She", "We", "It" not resolved
   - Example: (we, cultivate, victory gardens) ❌
   - Should resolve to actual entity ✅

4. **Vague Entities** (6.4%): "the amount", "the process", "this handbook"
   - Example: (the amount, is, 243 billion tons) ❌
   - Should be: (atmospheric carbon increase, is, 243 billion tons) ✅

5. **Incomplete Titles** (8%): Titles ending with prepositions/conjunctions
6. **Wrong Predicates** (6%): Semantically incompatible predicates
7. **Figurative Language** (5%): Metaphors treated as factual

EXPANDED DETECTION PATTERNS (Meta-ACE Improvements):
- **Possessive Pronouns**: "my people", "our tradition", "their practices" (should resolve to specific entity)
- **Demonstrative Pronouns**: "this", "that", "these", "those" (should resolve to antecedent)
- **Abstract Vague Patterns**: "the way", "the answer", "the solution", "the problem" (too abstract)
- **Philosophical Statements**: Overly abstract relationships that don't convey concrete information
- **Praise Quotes**: Endorsement language misinterpreted as factual claims

SEVERITY LEVELS (use these exactly):
- **CRITICAL**: Factually wrong, reversed relationships, breaks KG utility
- **HIGH**: Missing entity resolution, unusable relationships
- **MEDIUM**: Vague but potentially useful, clarity issues
- **MILD**: Minor clarity issues, doesn't harm KG utility (e.g., "my people" instead of "Slovenians" when context is clear)

Your analysis must:
1. Count issues in each category
2. Find NEW error patterns not in the V4 list
3. Trace each issue to root cause (which module/prompt/config failed?)
4. **ANALYZE PROMPTS**: Identify if Pass 1 or Pass 2 prompts contribute to issues
5. Provide specific, actionable recommendations for fixes (code AND prompts)
6. Prioritize by severity: CRITICAL > HIGH > MEDIUM > MILD
7. Classify issues accurately by severity - don't over-flag MILD issues as HIGH

PROMPT ANALYSIS GUIDELINES:
- **Pass 1 Issues**: If entities are extracted incorrectly from the start (e.g., pronouns, vague terms), consider if the extraction prompt encourages these errors
- **Pass 2 Issues**: If evaluation scores are miscalibrated (e.g., conflict detection too sensitive), consider if the evaluation prompt is unclear
- **Prompt Patterns to Watch For**:
  - Overly broad instructions ("extract ALL") may cause over-extraction
  - Missing constraints may allow pronouns/vague entities through
  - Unclear signal definitions may confuse text vs knowledge evaluation
  - Lack of few-shot examples may reduce quality
- **When to Recommend Prompt Changes**:
  - If errors appear BEFORE Pass 2.5 modules can fix them
  - If multiple Pass 2.5 modules are working around a upstream prompt issue
  - If the pattern affects >10% of relationships
  - If code fixes seem hacky/brittle compared to clearer prompts

Output ONLY valid JSON with this structure:
{
  "extraction_metadata": {
    "version": "v5",
    "total_relationships": 1023,
    "analysis_timestamp": "ISO-8601"
  },
  "quality_summary": {
    "critical_issues": 15,
    "high_priority_issues": 45,
    "medium_priority_issues": 30,
    "mild_issues": 20,
    "total_issues": 110,
    "issue_rate_percent": 10.7,
    "estimated_false_negative_rate": 0.13,
    "estimated_total_issues_with_fn": 125,
    "adjusted_issue_rate_percent": 12.2,
    "grade_confirmed": "B+",
    "grade_adjusted": "B",
    "note": "Adjusted metrics include estimated mild issues not flagged (13% FN rate based on meta-validation)"
  },
  "issue_categories": [
    {
      "category_name": "Reversed Authorship",
      "severity": "CRITICAL|HIGH|MEDIUM|MILD",
      "count": 15,
      "percentage": 1.5,
      "description": "Clear description of the issue",
      "root_cause_hypothesis": "Specific module/prompt that failed",
      "affected_module": "modules/pass2_5_postprocessing/bibliographic_parser.py",
      "affected_prompt": "prompts/pass1_extraction_v7.txt",
      "affected_config": null,
      "examples": [
        {
          "source": "bad source",
          "relationship": "predicate",
          "target": "bad target",
          "evidence_text": "evidence from book",
          "page": 41,
          "what_is_wrong": "explanation",
          "should_be": {
            "source": "correct source",
            "relationship": "predicate",
            "target": "correct target"
          }
        }
      ]
    }
  ],
  "novel_error_patterns": [
    {
      "pattern_name": "New pattern discovered",
      "severity": "CRITICAL|HIGH|MEDIUM|MILD",
      "count": 8,
      "description": "What the pattern is",
      "root_cause_hypothesis": "Why it happens",
      "affected_module": "file path",
      "examples": [...]
    }
  ],
  "improvement_recommendations": [
    {
      "priority": "CRITICAL",
      "type": "CODE_FIX|PROMPT_ENHANCEMENT|CONFIG_UPDATE|NEW_MODULE",
      "target_file": "specific file path",
      "recommendation": "Exact change to make",
      "expected_impact": "What this fixes",
      "rationale": "Why this approach is better than alternatives"
    }
  ],
  "prompt_analysis": {
    "pass1_extraction_issues": [
      {
        "issue": "Description of prompt-level issue",
        "current_wording": "Relevant excerpt from current prompt",
        "suggested_fix": "How to rephrase or enhance the prompt",
        "examples_needed": "Whether few-shot examples would help"
      }
    ],
    "pass2_evaluation_issues": [
      {
        "issue": "Description of evaluation prompt issue",
        "current_wording": "Relevant excerpt",
        "suggested_fix": "Improved wording"
      }
    ]
  },
  "system_health": {
    "meets_production_criteria": false,
    "target_quality_threshold": 0.05,
    "current_quality_issue_rate": 0.107
  }
}

Be thorough, specific, and actionable. Your analysis drives the improvement loop."""

    def _build_analysis_prompt(
        self,
        relationships: List[Dict[str, Any]],
        source_text: str,
        extraction_metadata: Dict[str, Any],
        v4_quality_reports: List[Dict[str, Any]]
    ) -> str:
        """Build the analysis prompt for Claude."""

        # Sample relationships for analysis (first 100 for prompt length)
        sample_rels = relationships[:100]

        # Load current prompts for analysis
        version = extraction_metadata.get('version', 'v7')
        try:
            from pathlib import Path
            import sys
            sys.path.insert(0, str(Path(self.playbook_path)))
            from prompt_loader import PromptLoader

            loader = PromptLoader(str(self.playbook_path))
            pass1_prompt = loader.load_prompt("pass1_extraction", version)
            pass2_prompt = loader.load_prompt("pass2_evaluation", version)
        except Exception as e:
            print(f"⚠️  Could not load prompts for analysis: {e}")
            print(f"⚠️  Using fallback prompt placeholders")
            pass1_prompt = "(Prompt not available for analysis)"
            pass2_prompt = "(Prompt not available for analysis)"

        prompt = f"""Analyze this knowledge graph extraction for quality issues.

## EXTRACTION METADATA

Version: {extraction_metadata.get('version', 'unknown')}
Book: {extraction_metadata.get('book_title', 'unknown')}
Total Relationships: {len(relationships)}
Extraction Date: {extraction_metadata.get('date', 'unknown')}

## CURRENT PROMPTS (ANALYZE THESE!)

### Pass 1 Extraction Prompt:
```
{pass1_prompt[:1500]}...
```

### Pass 2 Evaluation Prompt:
```
{pass2_prompt[:1000]}...
```

## SOURCE TEXT SAMPLE

{source_text[:2000]}...

## EXTRACTED RELATIONSHIPS (sample of {len(sample_rels)}/{len(relationships)})

```json
{json.dumps(sample_rels, indent=2)}
```

## HISTORICAL QUALITY REPORTS (V4)

"""

        if v4_quality_reports:
            for report in v4_quality_reports[:2]:  # Include top 2 reports
                prompt += f"\n### {report.get('title', 'V4 Report')}\n"
                prompt += f"{json.dumps(report, indent=2)[:3000]}...\n"
        else:
            prompt += "No historical reports available.\n"

        prompt += """

## YOUR TASK

Analyze the extracted relationships and provide:

1. **Issue Count by Category**: Count how many relationships have each known error type
2. **Novel Patterns**: Identify NEW error patterns not in V4 reports
3. **Root Cause Analysis**: For each issue category, hypothesize which module/prompt/config caused it
4. **Recommendations**: Specific, actionable changes to fix each issue
5. **Priority Ranking**: Rank recommendations by impact (critical > high > medium > low)

Focus on issues that are:
- Systematic (not one-off mistakes)
- Fixable through code/prompt/config changes
- High-impact (affect many relationships or critical quality)

Output your analysis as JSON matching the schema in your system prompt."""

        return prompt

    def _save_analysis(self, analysis: Dict[str, Any], version: str) -> None:
        """Save analysis report for Curator agent."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_dir = self.playbook_path / "analysis_reports"
        analysis_dir.mkdir(parents=True, exist_ok=True)

        output_path = analysis_dir / f"reflection_{version}_{timestamp}.json"

        with open(output_path, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"✅ Analysis saved to: {output_path}")


if __name__ == "__main__":
    # Example usage
    reflector = KGReflectorAgent()

    # Load sample extraction data
    sample_rels = []  # Load from extraction output
    source_text = ""  # Load book text

    analysis = reflector.analyze_kg_extraction(
        relationships=sample_rels,
        source_text=source_text,
        extraction_metadata={"version": "v5", "book_title": "Soil Stewardship Handbook"}
    )

    print(json.dumps(analysis, indent=2))
