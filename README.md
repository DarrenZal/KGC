# Knowledge Graph Cultivator (KGC)

**A Self-Improving Knowledge Graph Extraction System Using the ACE Framework**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 🌱 Overview

Knowledge Graph Cultivator (KGC) is an autonomous, self-improving system for extracting high-quality knowledge graphs from text using Large Language Models. Built on the **ACE (Agentic Context Engineering)** framework from Zhang et al. (2025), KGC continuously refines its extraction quality through iterative analysis, curation, and application cycles.

### Key Features

- **🤖 ACE-Powered Self-Improvement**: Automatically analyzes extraction quality, generates improvements, and applies them
- **📊 Comprehensive Extraction**: Extracts bibliographic, categorical, compositional, functional, and organizational relationships
- **🎯 High Quality**: Achieves <3% error rate (A++ grade) with 100% attribution and classification
- **📝 Complete Provenance**: Every relationship includes source attribution and statement type classification
- **🔄 Continuous Evolution**: System improves itself through Reflector → Curator → Applicator cycles

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
│  • Classification (FACTUAL, etc.)    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  PASS 2.5: Post-Processing           │
│  • Pronoun resolution                │
│  • Entity enrichment                 │
│  • List splitting                    │
│  • Bibliographic parsing             │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Knowledge Graph Output              │
│  • Relationships with attribution    │
│  • Classification flags              │
│  • Confidence scores                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  ACE SELF-IMPROVEMENT CYCLE          │
├─────────────────────────────────────┤
│  1. REFLECTOR: Analyze quality       │
│     → Identify issues                │
│     → Generate recommendations       │
├─────────────────────────────────────┤
│  2. CURATOR: Generate improvements   │
│     → Create changeset               │
│     → Prioritize changes             │
├─────────────────────────────────────┤
│  3. APPLICATOR: Apply changes        │
│     → Update prompts/code            │
│     → Deploy new version             │
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
# Edit .env and add your OPENAI_API_KEY
```

### Basic Usage

```bash
# Extract knowledge graph from a PDF
python scripts/extract.py --input my_book.pdf --output kg_output.json

# Run quality analysis (Reflector)
python scripts/reflect.py --input kg_output.json --output analysis.json

# Generate improvements (Curator)
python scripts/curate.py --analysis analysis.json --output changeset.json

# Run continuous ACE cycle
python scripts/run_ace_kg_continuous.py
```

### Python API

```python
from kgc.extraction import KGExtractor
from kgc.ace import KGReflector, KGCurator

# Initialize extractor
extractor = KGExtractor(model="gpt-4o-mini")

# Extract knowledge graph
kg = extractor.extract_from_text(text)

# Analyze quality
reflector = KGReflector()
analysis = reflector.analyze(kg)

# Generate improvements
curator = KGCurator()
changeset = curator.curate_improvements(analysis, current_version=10)
```

## 📊 Extraction Results

**V10 System Performance** (Soil Stewardship Handbook):
- **Relationships**: 650-750 comprehensive extractions
- **Quality Issues**: <3% (A++ grade)
- **High Confidence**: 80%+ of relationships
- **Attribution**: 100% (every relationship traced to source)
- **Classification**: 100% (all statements labeled by type)

### Relationship Types Extracted

1. **Bibliographic** (250+): authorship, publication, endorsements
2. **Categorical** (70+): is-a relationships, definitions
3. **Compositional**: contains, includes, provides
4. **Functional**: produces, enhances, stimulates
5. **Organizational**: affiliations, roles, collaborations

## 🎯 Statement Classification

Every extracted relationship is classified by type:

- **FACTUAL** (p_true: 0.7-1.0): Verifiable facts, citations, concrete relationships
- **TESTABLE_CLAIM** (p_true: 0.4-0.9): Scientific assertions with empirical basis
- **PHILOSOPHICAL_CLAIM** (p_true: 0.1-0.4): Existential statements, opinions
- **METAPHOR** (p_true: 0.1-0.4): Figurative language
- **OPINION** (p_true: 0.3-0.6): Subjective viewpoints
- **ABSTRACT_CONCEPT** (p_true: 0.2-0.5): Complex abstract ideas

## 🔄 ACE Framework

The ACE (Agentic Context Engineering) framework enables continuous self-improvement through treating contexts as evolving "playbooks":

### 1. **Reflector** (Analysis)
- Analyzes extraction quality using Claude Sonnet 4.5
- Identifies issues by severity (CRITICAL, HIGH, MEDIUM, MILD)
- Generates improvement recommendations
- Provides quality grades and metrics

### 2. **Curator** (Synthesis)
- Processes Reflector analysis
- Generates concrete changesets (code + prompts)
- Prioritizes changes by impact and risk
- Creates testing strategies

### 3. **Applicator** (Execution)
- Applies changesets to codebase
- Updates prompts and code
- Deploys new versions
- Validates improvements

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)**: Get started in 5 minutes
- **[ACE Framework Deep Dive](docs/ACE_FRAMEWORK.md)**: Understanding the self-improvement cycle
- **[Extraction Guide](docs/EXTRACTION_GUIDE.md)**: Customizing extraction for your domain
- **[V10 Implementation Plan](docs/V10_COMPREHENSIVE_KG_PLAN.md)**: Latest system design
- **[KG Master Guide](docs/KG_MASTER_GUIDE.md)**: Comprehensive system documentation

## 🛠️ Configuration

### Extraction Settings

Edit `kgc/prompts/pass1_extraction_v10.txt` to customize:
- Relationship types to extract
- Entity quality requirements
- Few-shot examples
- Domain-specific instructions

### Evaluation Settings

Edit `kgc/prompts/pass2_evaluation_v10.txt` to adjust:
- Confidence scoring thresholds
- Classification criteria
- Knowledge plausibility calibration

## 🔬 Research & Development

### Version History

- **V10** (Current): Comprehensive factual extraction with <3% error rate
- **V9**: 100% attribution + classification system
- **V8**: ACE Cycle 1 - Curator-generated improvements
- **V7**: Dual-signal evaluation with philosophical filter
- **V6**: Enhanced post-processing modules
- **V5**: Production-ready system with pronoun resolution

### Published Results

See `docs/` for detailed analysis of each version's improvements, including:
- Quality metrics and comparisons
- Reflector analysis reports
- Curator-generated changesets
- Performance benchmarks

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- **New relationship types**: Expand extraction capabilities
- **Domain adaptation**: Customize for specific fields (legal, medical, scientific)
- **Performance optimization**: Speed improvements, batch processing
- **Quality metrics**: New evaluation criteria
- **Documentation**: Tutorials, examples, translations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with OpenAI's GPT-4o-mini and Claude Sonnet 4.5
- ACE framework inspired by **Zhang et al. (2025)**: "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models"
- Developed for the Y on Earth Community

## 📖 References

**Zhang, Q., Hu, C., Xie, W., Liu, W., & Zheng, Y. (2025).** *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models.* arXiv preprint.

> The ACE framework treats contexts as evolving "playbooks" that guide model behavior through modular processes of generation, reflection, and curation. By applying structured, incremental updates (deltas) rather than full context rewrites, ACE prevents context collapse and enables continuous self-improvement. KGC implements this framework for knowledge graph extraction, using Reflector (analysis), Curator (improvement generation), and Applicator (deployment) cycles.

## 📧 Contact

- **Author**: Darren Zal
- **GitHub**: [@DarrenZal](https://github.com/DarrenZal)
- **Project**: [KGC Repository](https://github.com/DarrenZal/KGC)

## 🌟 Star History

If you find KGC useful, please star the repository!

---

**Note**: This is an active research project. The system continuously improves through the ACE framework. See [CHANGELOG.md](CHANGELOG.md) for version updates.
