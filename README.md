# Knowledge Graph Cultivator (KGC)

**A Self-Improving Knowledge Graph Extraction System Using the ACE Framework**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 🌱 Overview

Knowledge Graph Cultivator (KGC) is an autonomous, self-improving system for extracting high-quality knowledge graphs from text using Large Language Models. Built on the **ACE (Agentic Context Engineering)** framework, KGC continuously refines its extraction quality through iterative analysis, curation, and application cycles.

###  Key Features

- **🤖 Meta-ACE Self-Improvement**: System improves both extraction AND improvement agents themselves
- **📊 Comprehensive Extraction**: Extracts bibliographic, categorical, compositional, functional relationships
- **🎯 High Quality**: Achieved 7.86% error rate (B+ grade) in V11.2.2, targeting <4.5% (A- grade)
- **📝 Complete Provenance**: Every relationship includes source attribution and confidence scores
- **🔄 Continuous Evolution**: Reflector → Curator → Applicator cycles with automated validation
- **📈 Stat

istically Rigorous**: Automated testing with 95% confidence validation gates

## 🏗️ Architecture

```
┌─────────────┐
│   Text      │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  PASS 1: Comprehensive Extraction    │
│  (GPT-4o-mini + Structured Outputs)  │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  PASS 2: Dual-Signal Evaluation      │
│  • Text Confidence (0.0-1.0)         │
│  • Knowledge Plausibility (0.0-1.0)  │
│  • p_true = (text + knowledge) / 2   │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  PASS 2.5: Modular Postprocessing    │
│  • Pronoun resolution (V1.5.0)       │
│  • Predicate normalization (V1.3.0)  │
│  • Generic is-a filtering            │
│  • Praise quote detection            │
│  • List splitting (POS tagging)      │
│  • 12+ specialized modules           │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Knowledge Graph Output              │
│  • Relationships with p_true ≥ 0.5   │
│  • Source attribution                │
│  • Confidence scores                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  META-ACE IMPROVEMENT CYCLE          │
├─────────────────────────────────────┤
│  1. REFLECTOR: Analyze quality       │
│     → Identify ALL issues            │
│     → Root cause analysis            │
│     → Generate recommendations       │
├─────────────────────────────────────┤
│  2. CURATOR: Generate improvements   │
│     → Strategic changesets           │
│     → Prioritized by impact/risk     │
│     → Both code AND prompts          │
├─────────────────────────────────────┤
│  3. APPLICATOR: Intelligent apply    │
│     → Claude-powered implementation  │
│     → Reads current code             │
│     → Implements strategic guidance  │
├─────────────────────────────────────┤
│  4. VALIDATION GATE: Test before     │
│     → Test 30-50 problematic chunks  │
│     → Full pipeline (P1+P2+P2.5)     │
│     → Require ≥30% improvement       │
│     → 95% confidence, ±10% margin    │
├─────────────────────────────────────┤
│  5. META-ACE: Improve the improvers  │
│     → Fix Reflector if needed        │
│     → Fix Curator if needed          │
│     → Iterate until excellent        │
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/DarrenZal/KGC.git
cd KGC

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and ANTHROPIC_API_KEY
```

### Basic Usage

```bash
# Extract knowledge graph from a PDF (current version)
python scripts/extract_kg_v11_2_2_book.py

# Run quality analysis (Reflector)
python scripts/run_reflector_generic.py

# Generate improvements (Curator)
python scripts/run_curator_generic.py

# Apply improvements (Applicator)
python scripts/apply_changeset_generic.py

# Automated full ACE cycle (future)
python scripts/run_ace_cycle_automated.py
```

### Python API

```python
from src.ace_kg import KGReflectorAgent, KGCuratorAgent

# Analyze extraction quality
reflector = KGReflectorAgent()
analysis = reflector.analyze_kg_extraction(
    relationships=extracted_rels,
    source_text=book_text,
    extraction_metadata={'version': 'v11.2.2'}
)

# Generate improvements
curator = KGCuratorAgent()
changeset = curator.generate_changeset(
    reflection_analysis=analysis,
    current_version=11.2
)

# Generate detailed issues for validation testing
detailed_issues = reflector.generate_detailed_issues_for_testing(
    relationships=extracted_rels,
    source_text=book_text,
    analysis=analysis,
    version='v11.2.2',
    sample_size=30  # For statistical validation
)
```

## 📊 System Evolution & Results

### Version History

| Version | Date | Error Rate | Grade | Key Improvements |
|---------|------|------------|-------|------------------|
| **V11.2.2** | Oct 2025 | **7.86%** | **B+** | **Current validated baseline** |
| V11.2.1 | Oct 2025 | 21.85% | C- | Buggy baseline (3 module bugs discovered) |
| V11 | Oct 2025 | ~15% | B | ACE Cycle 1 baseline |
| V10 | Oct 2025 | ~20% | C+ | Comprehensive extraction |
| V9 | Sept 2025 | ~25% | C | Complete discourse graph |
| V8 | Sept 2025 | ~30% | D+ | First ACE cycle |
| V7 | Sept 2025 | ~35% | D | Dual-signal evaluation |

### V11.2.2 Quality Metrics

- **Total Relationships**: 891 extracted
- **Issues Identified**: 70 (7.86% error rate)
- **Issue Breakdown**:
  - CRITICAL: 0 ✅
  - HIGH: 8 (possessive pronouns, vague entities)
  - MEDIUM: 47 (praise quotes, philosophical claims, predicate fragmentation)
  - MILD: 15 (generic is-a, demonstrative pronouns)
- **Predicate Consistency**: 125 unique predicates (target: ~80)
- **Attribution**: 100% (every relationship traced to source)

### Meta-ACE Improvements

**Meta-Cycle 1** (V11.2.2 → V12):
1. ✅ **Fixed Curator**: Improved path resolution (A → A+, 36/40 → 39/40)
2. ✅ **10/10 Changes Applied**: All V12 improvements deployed
   - Enhanced pronoun resolution (possessive pronouns)
   - V12 extraction prompts (prevent vague entities)
   - V12 evaluation prompts (entity quality checks)
   - Enhanced predicate normalization (V1.3.0)
   - New generic is-a filter
   - Expanded praise quote detection
3. ✅ **Built Automated Testing**: Full pipeline validation system
4. ✅ **Enhanced Reflector**: Outputs all issues for statistical testing

**Target for V12**: <4.5% error rate (A- grade, ~40 issues)

## 🔬 Technical Innovation

### 1. **Meta-ACE**: Improving the Improvers

Unlike standard ACE which only improves extraction, our system improves THE IMPROVEMENT AGENTS themselves:

- **Reflector Meta-ACE**: If Reflector misses issues, we improve Reflector first
- **Curator Meta-ACE**: If Curator generates bad changes, we fix Curator and retry
- **Version Control**: Immutable baselines for safe iteration
- **Scoring System**: 40-point rubric for agent quality (strategic insight, technical depth, etc.)

### 2. **Intelligent Applicator**

Strategic changes are implemented by Claude, not string replacement:

- **Reads current code**: Understands context and existing implementation
- **Implements strategic guidance**: "Make X better" → intelligent code changes
- **Handles complexity**: Can implement multi-file changes, refactors, new features
- **Safe execution**: Tracks successes/failures, rollback on critical errors

### 3. **Automated Validation Gates**

Before running expensive full extractions, test improvements on statistically significant samples:

- **Sample Size**: 30-50 issues (95% confidence, ±10% margin of error)
- **Stratified Sampling**: Proportional by severity (CRITICAL, HIGH, MEDIUM, MILD)
- **Full Pipeline Testing**: Pass 1 → Pass 2 → Pass 2.5 on each sample
- **Automated Decisions**: Proceed only if ≥30% improvement observed
- **Time Savings**: 5 min validation vs 40 min full extraction

### 4. **Modular Postprocessing Pipeline**

Pass 2.5 uses 12+ specialized modules, each versioned independently:

- **PronounResolver** (V1.5.0): Anaphoric, generic, and possessive pronouns
- **PredicateNormalizer** (V1.3.0): 173 → ~80 unique predicates
- **GenericIsAFilter** (V1.0): Filters metaphorical and generic is-a relationships
- **PraiseQuoteDetector** (V1.3.0): Identifies endorsement language
- **ListSplitter** (V1.2): POS tagging for intelligent list splitting
- **BibliographicCitationParser** (V1.2): Authorship, dedications, endorsements
- **ClaimClassifier** (V1.1.0): FACTUAL, PHILOSOPHICAL, OPINION, RECOMMENDATION

Each module is independently testable and improvable.

## 📚 Documentation

- **[Quick Start](docs/KG_SYSTEM_OVERVIEW.md)**: System overview and basic usage
- **[ACE Framework Guide](docs/ACE_KG_EXTRACTION_VISION.md)**: Understanding self-improvement
- **[Master Guide](docs/KG_MASTER_GUIDE.md)**: Comprehensive technical documentation
- **[Meta-ACE](../docs/knowledge_graph/ACE_META_TUNING_RECOMMENDATIONS.md)**: Improving the improvement agents
- **[Full Automation Plan](../docs/knowledge_graph/ACE_FULL_AUTOMATION_PLAN.md)**: Future automated testing

## 🛠️ Configuration

### Extraction Settings

Prompts are versioned and located in `kg_extraction_playbook/prompts/`:
- `pass1_extraction_v12.txt`: Entity and relationship extraction
- `pass2_evaluation_v12.txt`: Dual-signal confidence scoring
- Each prompt includes constraints, examples, and quality requirements

### Postprocessing Modules

Located in `src/knowledge_graph/postprocessing/`:
- **Universal modules**: `/universal/` (pronoun resolution, normalization, etc.)
- **Book-specific**: `/content_specific/books/` (bibliographic parsing, praise detection)
- Each module has version history and can be independently updated

## 🔄 Running an ACE Cycle

### Manual Process

```bash
# 1. Run extraction (current version)
python scripts/extract_kg_v11_2_2_book.py

# 2. Run Reflector to analyze quality
python scripts/run_reflector_generic.py
# → Outputs: analysis_reports/reflection_v11.2.2_TIMESTAMP.json

# 3. Run Curator to generate improvements
python scripts/run_curator_generic.py
# → Outputs: changesets/changeset_v12_TIMESTAMP.json

# 4. Review changeset (check priority, risk, recommendations)
cat kg_extraction_playbook/changesets/changeset_v12_*.json | python -m json.tool

# 5. Apply changeset (uses Intelligent Applicator)
python scripts/apply_changeset_generic.py
# → Reads latest changeset, applies all operations

# 6. Run new extraction to validate
python scripts/extract_kg_v12_book.py
```

### Automated Process (Future)

```bash
# Run complete ACE cycle with validation
python scripts/run_ace_cycle_automated.py

# This will:
# 1. Generate detailed issues from last Reflector run
# 2. Run Curator to create improvements
# 3. Apply changeset
# 4. TEST on 30-50 problematic chunks (5 minutes)
# 5. If ≥30% improvement: proceed to full extraction
# 6. If <30%: iterate Curator, retry
# 7. Run Reflector on new version
# 8. Compare metrics, decide next steps
```

## 🤝 Contributing

We welcome contributions! Areas of interest:

- **New relationship types**: Expand extraction capabilities
- **Domain adaptation**: Customize for specific fields (legal, medical, scientific)
- **Performance optimization**: Batch processing, parallel execution
- **Agent improvements**: Better Reflector/Curator strategies
- **Testing infrastructure**: More robust validation

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Built with OpenAI GPT-4o-mini and Anthropic Claude Sonnet 4.5
- ACE framework inspired by **Zhang et al. (2025)**: "Agentic Context Engineering"
- Developed for the Y on Earth Community

## 📖 Citation

If you use KGC in your research, please cite:

```bibtex
@software{kgc2025,
  author = {Zal, Darren},
  title = {Knowledge Graph Cultivator: A Self-Improving KG Extraction System},
  year = {2025},
  url = {https://github.com/DarrenZal/KGC}
}
```

## 📧 Contact

- **Author**: Darren Zal
- **GitHub**: [@DarrenZal](https://github.com/DarrenZal)
- **Project**: [KGC Repository](https://github.com/DarrenZal/KGC)

---

**Current Status**: V11.2.2 validated (7.86% error, B+ grade). V12 in progress targeting <4.5% (A- grade). Meta-ACE improvements complete. Automated validation gates implemented.

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.
