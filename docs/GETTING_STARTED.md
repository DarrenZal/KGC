# Getting Started with KGC

**Knowledge Graph Construction (KGC)** - A production-ready system for extracting high-quality knowledge graphs from books and documents.

---

## 🎯 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/DarrenZal/KGC.git
cd KGC

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-key-here"
```

### Basic Usage

Extract a knowledge graph from a book:

```bash
python scripts/extract_kg_v14_3_8_incremental.py \
  --book our_biggest_deal \
  --section front_matter \
  --pages 1-30 \
  --author "Aaron William Perry"
```

### Output

The extraction will create:
- **Extracted graph**: `kgc/extraction/output/[book]/v14_3_8/chapters/[section]_v14_3_8_[timestamp].json`
- **Execution manifest**: `kgc/extraction/output/[book]/v14_3_8/manifests/[section]_execution_[timestamp].json`
- **Quality report**: Via reflector analysis (optional)

---

## 📊 Current Performance

**Grade:** A+ (Quality Gate Passed)
- 0 CRITICAL issues
- ≤2 HIGH issues
- ≤2% issue rate
- 116 high-quality relationships extracted from 30 pages

**Improvement:** 93% reduction in issues from baseline

---

## 🔧 Key Features

### 1. Modular Postprocessing Pipeline

The system uses a priority-based pipeline with 18+ specialized modules:

```python
Pipeline Modules (in execution order):
1. FieldNormalizer (5)
2. PraiseQuoteDetector (10)
3. MetadataFilter (11)
4. FrontMatterDetector (12)
5. DedicationNormalizer (18)        # V14.3.8 - Fixes malformed dedications
6. SubtitleJoiner (19)              # V14.3.10 - Dash/newline-aware
7. BibliographicCitationParser (20) # V14.3.9 - Enhanced person detection
8. ContextEnricher (30)
9. ListSplitter (40)
10. PronounResolver (60)
11. PredicateNormalizer (70)
12. PredicateValidator (80)
13. TypeCompatibilityValidator (85)
14. VagueEntityBlocker (90)
15. TitleCompletenessValidator
16. ClaimClassifier                 # V14.3.10 - Moved before filter
17. FigurativeLanguageFilter        # V14.3.10 - Stricter detection
18. Deduplicator
```

### 2. Dual-Pass Extraction

**Pass 1: Initial Extraction**
- Uses GPT-4o with structured outputs
- Extracts entities and relationships from text
- Temperature: 0.0 (deterministic)
- Max tokens: 16,384

**Pass 2: Quality Evaluation**
- Validates extracted relationships
- Assigns confidence scores
- Flags potential issues
- Filters low-quality extractions

### 3. Quality Analysis with Reflector

Run quality analysis on extracted graphs:

```bash
python scripts/run_reflector_incremental.py \
  --input kgc/extraction/output/[book]/v14_3_8/chapters/[file].json \
  --book our_biggest_deal \
  --section front_matter \
  --pages 1-30
```

**Reflector Output:**
- Grade (A+ to F)
- Issue categorization (CRITICAL, HIGH, MEDIUM, MILD)
- Issue rate percentage
- Detailed analysis report

---

## 📖 Example: Extracting "Our Biggest Deal"

### Step 1: Prepare the PDF

Place your book PDF in the data directory:
```
data/books/our_biggest_deal/
├── our_biggest_deal.pdf
└── metadata.json
```

### Step 2: Run Extraction

```bash
python scripts/extract_kg_v14_3_8_incremental.py \
  --book our_biggest_deal \
  --section front_matter \
  --pages 1-30 \
  --author "Aaron William Perry"
```

### Step 3: Review Output

```bash
# Check extraction results
cat kgc/extraction/output/our_biggest_deal/v14_3_8/chapters/front_matter_v14_3_8_*.json

# View execution manifest
cat kgc/extraction/output/our_biggest_deal/v14_3_8/manifests/front_matter_execution_*.json
```

### Step 4: Run Quality Analysis

```bash
python scripts/run_reflector_incremental.py \
  --input kgc/extraction/output/our_biggest_deal/v14_3_8/chapters/front_matter_v14_3_8_*.json \
  --book our_biggest_deal \
  --section front_matter \
  --pages 1-30
```

---

## 🎓 Understanding the Output

### Extracted Relationship Format

```json
{
  "source": "Aaron William Perry",
  "target": "Our Biggest Deal",
  "relationship": "authored",
  "source_type": "Person",
  "target_type": "Book",
  "context": "Aaron William Perry authored Our Biggest Deal...",
  "confidence": 0.95,
  "page_number": 5,
  "flags": {}
}
```

### Key Fields

- **source/target**: The entities in the relationship
- **relationship**: The predicate connecting them
- **source_type/target_type**: Entity types (Person, Book, Organization, etc.)
- **context**: Original text supporting the relationship
- **confidence**: Quality score (0.0-1.0)
- **page_number**: Source location in document
- **flags**: Quality indicators (DEDICATION_NORMALIZED, AUTHORSHIP_REVERSED, etc.)

---

## 🔍 Common Use Cases

### 1. Book Knowledge Graph Extraction

Extract structured knowledge from books for:
- Academic research
- Content analysis
- Citation networks
- Topic modeling

### 2. Incremental Section Processing

Process large books section by section:
```bash
# Front matter (pages 1-30)
python scripts/extract_kg_v14_3_8_incremental.py --book [name] --section front_matter --pages 1-30

# Chapter 1 (pages 31-60)
python scripts/extract_kg_v14_3_8_incremental.py --book [name] --section chapter_1 --pages 31-60

# Chapter 2 (pages 61-90)
python scripts/extract_kg_v14_3_8_incremental.py --book [name] --section chapter_2 --pages 61-90
```

### 3. Quality Assurance Workflow

```bash
# 1. Extract
python scripts/extract_kg_v14_3_8_incremental.py [args]

# 2. Analyze quality
python scripts/run_reflector_incremental.py --input [output_file] [args]

# 3. Review issues and iterate if needed
# If grade < A, review reflector report and adjust prompts/modules
```

---

## ⚙️ Configuration

### Extraction Prompts

Located in `kgc/prompts/`:
- `pass1_extraction_v14_3_1.txt` - Initial extraction instructions
- `pass2_evaluation_v14_3.txt` - Quality evaluation criteria

### Pipeline Customization

Modify pipeline configuration in:
- `kgc/extraction/postprocessing/pipelines/book_pipeline.py`

Add/remove modules or adjust priorities:
```python
def get_book_pipeline_v1438():
    return [
        FieldNormalizer(priority=5),
        PraiseQuoteDetector(priority=10),
        # ... add your custom module here
        CustomModule(priority=15),
        # ...
    ]
```

### Model Configuration

Set in extraction script:
```python
model_config = {
    "pass1_model": "gpt-4o-2024-08-06",
    "pass2_model": "gpt-4o-2024-08-06",
    "temperature": 0.0,
    "max_tokens": 16384
}
```

---

## 🐛 Troubleshooting

### Issue: "No relationships extracted"

**Cause:** Text may not contain extractable relationships or prompts may be too strict.

**Solution:**
1. Check input text quality
2. Review pass1 prompt for overly restrictive criteria
3. Verify page range contains substantial content

### Issue: "High issue rate (>10%)"

**Cause:** Postprocessing modules may need tuning for your content type.

**Solution:**
1. Run reflector to identify issue patterns
2. Adjust module parameters
3. Review V14_3_FINAL_A_PLUS_ACHIEVEMENT.md for examples

### Issue: "JSON serialization errors"

**Cause:** Module returning wrong data structure.

**Solution:**
- Ensure all modules return `List[Any]` (flat list)
- Stats should be stored in `self.stats`, not returned
- See DedicationNormalizer fix in V14_3_FINAL_A_PLUS_ACHIEVEMENT.md

---

## 📚 Next Steps

1. **Read the Architecture Guide**: See `SYSTEM_ARCHITECTURE.md` for technical details
2. **Review Achievement History**: See `V14_3_FINAL_A_PLUS_ACHIEVEMENT.md` for implementation details
3. **Explore Examples**: Check `examples/` directory for sample extractions
4. **Customize Pipeline**: Modify modules for your specific use case

---

## 🤝 Contributing

This system is designed to be extended. To add a new postprocessing module:

1. Create module in `kgc/extraction/postprocessing/[category]/`
2. Inherit from `PostProcessingModule`
3. Implement `process_batch(relationships, context) -> List[Any]`
4. Add to pipeline in `book_pipeline.py`

See existing modules for examples.

---

## 📄 License

See LICENSE file in repository root.

---

**For detailed technical architecture, see [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)**

**For implementation history and lessons learned, see [V14_3_FINAL_A_PLUS_ACHIEVEMENT.md](../V14_3_FINAL_A_PLUS_ACHIEVEMENT.md)**
