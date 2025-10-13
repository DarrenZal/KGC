"""
KG Curator Agent

Uses Claude Sonnet 4.5 to transform Reflector insights into actionable
code/prompt/config changes for the knowledge graph extraction pipeline.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

import anthropic


class KGCuratorAgent:
    """
    The KG Curator transforms Reflector insights into executable changes:
    - Organizes recommendations by type and priority
    - Creates specific code modifications
    - Proposes prompt enhancements
    - Designs configuration tweaks
    - Manages system evolution and version control

    Uses Claude Sonnet 4.5 for strategic planning and code generation.
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

    def curate_improvements(
        self,
        reflector_report: Dict[str, Any],
        current_version: int,
        playbook_state: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Transform Reflector insights into actionable changeset.

        Args:
            reflector_report: Output from KG Reflector analysis
            current_version: Current extraction version number
            playbook_state: Current Playbook files/configs (optional)

        Returns:
            Changeset with specific file operations to evolve system
        """
        # Load current Playbook state if not provided
        if playbook_state is None:
            playbook_state = self._load_playbook_state()

        # Build curation prompt
        prompt = self._build_curation_prompt(
            reflector_report,
            current_version,
            playbook_state
        )

        # Run Claude Sonnet 4.5 curation
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16000,  # Allow for detailed changesets
            temperature=0.4,  # Slightly creative for solutions
            system=self._get_curator_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Parse response
        curation_text = response.content[0].text

        # Extract JSON from response
        try:
            if "```json" in curation_text:
                json_start = curation_text.find("```json") + 7
                json_end = curation_text.find("```", json_start)
                json_str = curation_text[json_start:json_end].strip()
            else:
                json_str = curation_text

            changeset = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse JSON from Claude response: {e}")
            print(f"Response text: {curation_text[:500]}...")
            changeset = {
                "error": "json_parse_failed",
                "raw_response": curation_text
            }

        # Enhance with metadata
        changeset["metadata"] = {
            "curation_date": datetime.now().isoformat(),
            "source_version": current_version,
            "target_version": current_version + 1,
            "reflector_analysis_id": reflector_report.get("metadata", {}).get("analysis_date"),
            "curator_version": "1.0_claude",
            "model_used": self.model
        }

        # Save changeset
        self._save_changeset(changeset, current_version)

        return changeset

    def _get_curator_system_prompt(self) -> str:
        """System prompt for Claude Sonnet 4.5 Curator."""
        return """You are an expert software engineer specializing in knowledge graph extraction systems. Your role is to transform quality analysis insights into specific, executable changes to the extraction pipeline.

You are curating improvements for a multi-stage KG extraction pipeline:
- **Pass 1**: LLM extraction of entities and relationships from book text
- **Pass 2**: Dual-signal validation (text confidence + knowledge plausibility)
- **Pass 2.5**: Post-processing with 7 modules:
  1. BibliographicCitationParser (fix reversed authorship)
  2. ListSplitter (split comma-separated targets)
  3. PronounResolver (resolve He/She/We to entities)
  4. ContextEnricher (expand vague concepts)
  5. TitleCompletenessValidator (flag incomplete titles)
  6. PredicateValidator (validate semantic compatibility)
  7. FigurativeLanguageFilter (detect metaphors)

THE ENTIRE PIPELINE IS YOUR "PLAYBOOK" - YOU CAN MODIFY ANY PART:
- Python code files (.py)
- Extraction prompts (.txt)
- Configuration files (.json)
- Vocabulary lists
- Regular expressions
- Confidence thresholds

Your curation must:
1. **Be Specific**: Target exact files, functions, and line ranges
2. **Be Executable**: Provide old_content and new_content for each change
3. **Be Traced**: Connect each change to a Reflector recommendation
4. **Be Prioritized**: Rank by impact (CRITICAL > HIGH > MEDIUM > LOW)
5. **Be Safe**: Include rollback plans and risk assessments

CHANGE TYPES YOU CAN PROPOSE:
- **CODE_FIX**: Modify Python code (e.g., fix regex in bibliographic_parser.py)
- **PROMPT_ENHANCEMENT**: Update extraction prompts (e.g., add few-shot examples, rephrase instructions)
- **CONFIG_UPDATE**: Change configuration values (e.g., adjust thresholds)
- **NEW_MODULE**: Add new post-processing module (e.g., ChemicalFormulaValidator)

PROMPT vs CODE: When to Choose Each
- Use **PROMPT_ENHANCEMENT** when:
  - Errors occur in Pass 1 extraction (before any code processing)
  - LLM behavior can be guided with clearer instructions
  - Adding constraints/examples would prevent the issue
  - Multiple Pass 2.5 modules are compensating for prompt weakness
  - Example: "Stop extracting pronouns" → add to Pass 1 prompt

- Use **CODE_FIX** when:
  - Pattern is systematic and can be detected with rules
  - LLM output needs deterministic transformation
  - Domain-specific logic is required (e.g., bibliographic citations)
  - Prompt changes alone won't be reliable
  - Example: "Reverse author/title" → code is more reliable than prompt

- Use **BOTH** when:
  - Prompt prevents error from occurring (upstream)
  - Code catches any that slip through (downstream safety net)
  - Example: Prompt says "no pronouns" + PronounResolver as backup

Output ONLY valid JSON with this structure:
{
  "changeset_metadata": {
    "source_version": 5,
    "target_version": 6,
    "total_changes": 12,
    "estimated_impact": "Reduces critical issues by 100%, high priority by 60%"
  },
  "file_operations": [
    {
      "operation_id": "change_001",
      "operation_type": "CODE_FIX",
      "file_path": "modules/pass2_5_postprocessing/bibliographic_parser.py",
      "priority": "CRITICAL",
      "rationale": "Fix reversed authorship by expanding citation pattern detection",
      "risk_level": "low",
      "affected_issue_category": "Reversed Authorship",
      "expected_improvement": "Fixes all 15 reversed authorship errors",

      "edit_details": {
        "target_function": "BibliographicCitationParser.__init__",
        "old_content": "        self.citation_patterns = [\\n            r'^([A-Z][a-z]+,\\\\s+[A-Z][a-z]+)\\\\.', \\n        ]",
        "new_content": "        self.citation_patterns = [\\n            r'^([A-Z][a-z]+,\\\\s+[A-Z][a-z]+)\\\\.', \\n            r'^\\\"([^\\\"]+)\\\"\\\\.\\\\s+([A-Z][a-z]+)',\\n        ]",
        "validation": "Test with V4 reversed authorship examples"
      }
    },
    {
      "operation_id": "change_002",
      "operation_type": "PROMPT_ENHANCEMENT",
      "file_path": "prompts/pass1_extraction_v7.txt",
      "priority": "HIGH",
      "rationale": "Add explicit instruction to prevent pronoun sources",
      "risk_level": "low",
      "affected_issue_category": "Pronoun Sources",
      "expected_improvement": "Reduces pronoun issues by 80%",

      "edit_details": {
        "target_section": "ENTITY RESOLUTION RULES",
        "old_content": "## 📝 OUTPUT FORMAT ##",
        "new_content": "## ⚠️ CRITICAL RULES ##\\n\\n**NEVER use pronouns as entities:**\\n   ❌ BAD: (He, resides in, Colorado)\\n   ❌ BAD: (She, founded, organization)\\n   ❌ BAD: (We, practice, composting)\\n   ✅ GOOD: (Aaron William Perry, resides in, Colorado)\\n   ✅ GOOD: (Maria Rodriguez, founded, Green Earth Initiative)\\n\\n**Always resolve pronouns to specific entities before extracting.**\\n\\n## 📝 OUTPUT FORMAT ##",
        "validation": "Test prompt on sample text with pronouns",
        "prompt_version": "v8"
      }
    },
    {
      "operation_id": "change_003",
      "operation_type": "CONFIG_UPDATE",
      "file_path": "config/vocabularies/metaphorical_terms.json",
      "priority": "MEDIUM",
      "rationale": "Expand metaphorical vocabulary based on novel patterns",
      "risk_level": "low",
      "affected_issue_category": "Figurative Language",
      "expected_improvement": "Catches 10 additional metaphors",

      "edit_details": {
        "json_path": "metaphorical_terms",
        "old_value": ["sacred", "magic", "spiritual"],
        "new_value": ["sacred", "magic", "spiritual", "compass", "journey", "quest"],
        "validation": "Test FigurativeLanguageFilter with new terms"
      }
    },
    {
      "operation_id": "change_004",
      "operation_type": "NEW_MODULE",
      "file_path": "modules/pass2_5_postprocessing/chemical_formula_validator.py",
      "priority": "LOW",
      "rationale": "Handle chemical formulas from PDF extraction",
      "risk_level": "medium",
      "affected_issue_category": "Novel Pattern: Chemical Formulas",
      "expected_improvement": "Fixes 8 chemistry-related errors",

      "create_details": {
        "module_name": "ChemicalFormulaValidator",
        "class_template": "PostProcessingModule",
        "dependencies": ["re", "typing"],
        "content": "class ChemicalFormulaValidator:\\n    def __init__(self):\\n        self.patterns = [r'\\\\b([A-Z][a-z]?\\\\d+)+\\\\b']\\n    def process_batch(self, rels): pass",
        "integration_point": "orchestrator.py:pass_2_5_quality_post_processing",
        "validation": "Unit tests for CO₂, H₂O, CH₄"
      }
    }
  ],
  "priorities": {
    "immediate": [
      "change_001: Fix reversed authorship (CRITICAL)",
      "change_002: Add pronoun prevention prompt (HIGH)"
    ],
    "short_term": [
      "change_003: Expand metaphorical terms (MEDIUM)"
    ],
    "long_term": [
      "change_004: Add chemical formula validator (LOW)"
    ]
  },
  "testing_strategy": {
    "unit_tests": ["Test each modified module independently"],
    "integration_tests": ["Run V6 extraction on Soil Handbook sample"],
    "regression_tests": ["Compare V6 vs V5 on same input"],
    "success_criteria": ["Critical issues: 15 → 0", "Total issues: 10% → 5%"]
  },
  "rollback_plan": {
    "backup_location": "kg_extraction_playbook_backups/v5/",
    "rollback_command": "python scripts/rollback_version.py --to v5",
    "rollback_conditions": [
      "If V6 quality worse than V5",
      "If V6 extraction crashes",
      "If tests fail"
    ]
  }
}

Be thorough, specific, and actionable. Every change must be traceable to a Reflector insight and have clear expected impact."""

    def _build_curation_prompt(
        self,
        reflector_report: Dict[str, Any],
        current_version: int,
        playbook_state: Dict[str, Any]
    ) -> str:
        """Build the curation prompt for Claude."""

        prompt = f"""Transform the following Reflector analysis into an executable changeset.

## REFLECTOR ANALYSIS

{json.dumps(reflector_report, indent=2)}

## CURRENT SYSTEM STATE

Version: V{current_version}
Target Version: V{current_version + 1}

Current Playbook Structure:
{json.dumps(playbook_state, indent=2)}

## YOUR TASK

Based on the Reflector's analysis, create a changeset that:

1. **Addresses Critical Issues First**: Focus on issues that affect >5% of relationships
2. **Targets Root Causes**: Don't just fix symptoms - fix the underlying module/prompt/config
3. **Provides Exact Changes**: Specify old_content and new_content for every edit
4. **Estimates Impact**: Predict how many relationships each change will fix
5. **Manages Risk**: Mark changes as low/medium/high risk

PRIORITIES:
- **CRITICAL**: Reversed authorship, broken extraction logic → Fix immediately
- **HIGH**: Pronouns, lists, vague entities → High-impact patterns
- **MEDIUM**: Incomplete titles, wrong predicates → Quality improvements
- **LOW**: Metaphorical language, minor edge cases → Polish

For each Reflector recommendation, propose:
- Specific file path to modify
- Exact code/prompt/config changes
- Rationale connecting to the issue
- Expected improvement (quantified if possible)
- Risk level and rollback plan

Output your changeset as JSON matching the schema in your system prompt."""

        return prompt

    def _load_playbook_state(self) -> Dict[str, Any]:
        """Load current Playbook structure and key files."""
        state = {
            "modules": [],
            "prompts": [],
            "configs": [],
            "vocabularies": []
        }

        # Scan Playbook directory structure
        if self.playbook_path.exists():
            # List modules
            modules_dir = self.playbook_path / "modules"
            if modules_dir.exists():
                state["modules"] = [str(f.relative_to(self.playbook_path))
                                   for f in modules_dir.rglob("*.py")]

            # List prompts
            prompts_dir = self.playbook_path / "prompts"
            if prompts_dir.exists():
                state["prompts"] = [str(f.relative_to(self.playbook_path))
                                   for f in prompts_dir.rglob("*.txt")]

            # List configs
            configs_dir = self.playbook_path / "config"
            if configs_dir.exists():
                state["configs"] = [str(f.relative_to(self.playbook_path))
                                   for f in configs_dir.rglob("*.json")]

        return state

    def _save_changeset(self, changeset: Dict[str, Any], version: int) -> None:
        """Save changeset for review and application."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        changesets_dir = self.playbook_path / "changesets"
        changesets_dir.mkdir(parents=True, exist_ok=True)

        output_path = changesets_dir / f"changeset_v{version}_to_v{version+1}_{timestamp}.json"

        with open(output_path, 'w') as f:
            json.dump(changeset, f, indent=2)

        print(f"✅ Changeset saved to: {output_path}")

    def apply_changeset(
        self,
        changeset: Dict[str, Any],
        dry_run: bool = False,
        auto_apply_low_risk: bool = True
    ) -> Dict[str, Any]:
        """
        Apply changeset to evolve Playbook.

        Args:
            changeset: Output from curate_improvements()
            dry_run: If True, show changes but don't apply
            auto_apply_low_risk: Automatically apply low-risk changes

        Returns:
            Application results with success/failure status
        """
        results = {
            "applied": [],
            "skipped": [],
            "failed": [],
            "requires_approval": []
        }

        print(f"\n{'='*60}")
        print(f"APPLYING CHANGESET: V{changeset['metadata']['source_version']} → V{changeset['metadata']['target_version']}")
        print(f"{'='*60}\n")

        for operation in changeset.get("file_operations", []):
            op_id = operation.get("operation_id", "unknown")
            priority = operation.get("priority", "MEDIUM")
            risk = operation.get("risk_level", "medium")
            file_path = operation.get("file_path", "unknown")

            print(f"\n[{op_id}] {operation.get('operation_type')} - {file_path}")
            print(f"  Priority: {priority}, Risk: {risk}")
            print(f"  Rationale: {operation.get('rationale', 'N/A')}")

            # Decide whether to apply
            should_apply = False

            if dry_run:
                print(f"  ⏸️  DRY RUN - Would apply")
                results["skipped"].append(operation)
                continue

            if auto_apply_low_risk and risk == "low":
                should_apply = True
                print(f"  ⚡ AUTO-APPLYING (low risk)")
            else:
                print(f"  ⏸️  REQUIRES APPROVAL (risk: {risk})")
                results["requires_approval"].append(operation)
                continue

            if should_apply:
                try:
                    self._apply_file_operation(operation)
                    results["applied"].append(operation)
                    print(f"  ✅ APPLIED")
                except Exception as e:
                    print(f"  ❌ FAILED: {e}")
                    results["failed"].append({
                        "operation": operation,
                        "error": str(e)
                    })

        # Summary
        print(f"\n{'='*60}")
        print(f"CHANGESET APPLICATION COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Applied: {len(results['applied'])}")
        print(f"⏸️  Requires Approval: {len(results['requires_approval'])}")
        print(f"⏭️  Skipped: {len(results['skipped'])}")
        print(f"❌ Failed: {len(results['failed'])}")

        return results

    def _apply_file_operation(self, operation: Dict[str, Any]) -> None:
        """Apply a single file operation."""
        op_type = operation.get("operation_type")
        file_path_str = operation.get("file_path")
        file_path = self.playbook_path / file_path_str

        if op_type == "CODE_FIX":
            # Edit existing code file
            edit_details = operation.get("edit_details", {})
            old_content = edit_details.get("old_content", "")
            new_content = edit_details.get("new_content", "")

            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r') as f:
                content = f.read()

            if old_content not in content:
                raise ValueError(f"Old content not found in {file_path}")

            updated_content = content.replace(old_content, new_content, 1)

            with open(file_path, 'w') as f:
                f.write(updated_content)

        elif op_type == "PROMPT_ENHANCEMENT":
            # Edit prompt file with versioning
            edit_details = operation.get("edit_details", {})
            old_content = edit_details.get("old_content", "")
            new_content = edit_details.get("new_content", "")
            new_version = edit_details.get("prompt_version")  # e.g., "v8"

            if not file_path.exists():
                raise FileNotFoundError(f"Prompt file not found: {file_path}")

            # Read current prompt
            with open(file_path, 'r') as f:
                content = f.read()

            if old_content not in content:
                raise ValueError(f"Old content not found in {file_path}")

            # Apply changes
            updated_content = content.replace(old_content, new_content, 1)

            # Save as new version if specified
            if new_version:
                # Extract prompt name from path: "prompts/pass1_extraction_v7.txt" → "pass1_extraction"
                prompt_name = file_path.stem.rsplit('_', 1)[0]  # Remove version suffix
                new_file_path = self.playbook_path / "prompts" / f"{prompt_name}_{new_version}.txt"

                with open(new_file_path, 'w') as f:
                    f.write(updated_content)

                print(f"  📝 Created new prompt version: {new_file_path.name}")
            else:
                # Update in place (no version change)
                with open(file_path, 'w') as f:
                    f.write(updated_content)

        elif op_type == "CONFIG_UPDATE":
            # Update JSON config
            edit_details = operation.get("edit_details", {})
            json_path = edit_details.get("json_path", "")
            new_value = edit_details.get("new_value")

            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r') as f:
                config = json.load(f)

            # Navigate to setting
            keys = json_path.split('.')
            current = config
            for key in keys[:-1]:
                current = current[key]

            # Update value
            current[keys[-1]] = new_value

            with open(file_path, 'w') as f:
                json.dump(config, f, indent=2)

        elif op_type == "NEW_MODULE":
            # Create new file
            create_details = operation.get("create_details", {})
            content = create_details.get("content", "")

            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w') as f:
                f.write(content)

        else:
            raise ValueError(f"Unknown operation type: {op_type}")


if __name__ == "__main__":
    # Example usage
    curator = KGCuratorAgent()

    # Load sample Reflector report
    sample_report = {
        "critical_issues": 15,
        "recommendations": [
            {
                "priority": "CRITICAL",
                "type": "CODE_FIX",
                "target_file": "modules/bibliographic_parser.py"
            }
        ]
    }

    changeset = curator.curate_improvements(
        reflector_report=sample_report,
        current_version=5
    )

    print(json.dumps(changeset, indent=2))
