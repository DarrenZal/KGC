"""
Book Pipeline Configuration

Pre-configured pipeline for book extraction with all V14.1 enhancements.

Modules included (in priority order):
1. VagueEntityBlocker (30) - Filter overly vague entities early
2. ListSplitter (40) - Split list targets early (V11.2: enhanced "and" support)
3. ContextEnricher (50) - Enrich vague entities with context
4. PronounResolver (60) - Resolve pronouns to antecedents
5. PredicateNormalizer (70) - Normalize verbose predicates
6. PredicateValidator (80) - Validate predicate logic
7. TitleCompletenessValidator (90) - Validate book titles
8. FigurativeLanguageFilter (100) - Normalize metaphors
9. ClaimClassifier (105) - Classify relationships (V11.2: NEW)
10. Deduplicator (110) - Remove duplicates (V11.2: NEW)
11. SemanticDeduplicator (115) - Remove semantic duplicates using embeddings (V14.1: NEW)
12. ConfidenceFilter (120) - Apply p_true thresholds with flag-specific overrides (V14: NEW)

Book-specific modules:
- PraiseQuoteDetector (10) - Detect praise quotes in front matter
- MetadataFilter (11) - Filter book metadata relationships (V14: NEW)
- BibliographicCitationParser (20) - Parse bibliographic citations (V11.2: fixed dedication logic)

V14.1 Enhancement:
- SemanticDeduplicator addresses V14.0's 25 redundant 'is-a' relationship issues (4.2% of total)
"""

from typing import Optional, Dict, Any

from ..base import PipelineOrchestrator
from ..universal import (
    VagueEntityBlocker,
    ListSplitter,
    ContextEnricher,
    PronounResolver,
    PredicateNormalizer,
    PredicateValidator,
    ClaimClassifier,
    Deduplicator,
    SemanticDeduplicator,
    ConfidenceFilter,
)
from ..content_specific.books import (
    PraiseQuoteDetector,
    MetadataFilter,
    FrontMatterDetector,
    BibliographicCitationParser,
    TitleCompletenessValidator,
    FigurativeLanguageFilter,
    SubjectiveContentFilter,
)


def get_book_pipeline(config: Optional[Dict[str, Any]] = None, version: str = 'v14') -> PipelineOrchestrator:
    """
    Get a pre-configured pipeline for book extraction.

    This pipeline includes all V8 enhancements and is optimized for
    extracting knowledge graphs from books.

    Args:
        config: Optional configuration dictionary for modules
        version: Pipeline version:
            - 'v13' (12 modules, A- baseline)
            - 'v14' (15 modules, current)
            - 'v14_3_1' (13 modules, V13 + SubjectiveContentFilter)
            - 'v14_3_2' (14 modules, V14.3.1 + resolve-then-block + CRITICAL fixes)

    Returns:
        PipelineOrchestrator with book-optimized modules
    """
    if config is None:
        config = {}

    if version == 'v14_3_2':
        # V14.3.2 Configuration (14 modules, A+ target with resolve-then-block workflow)
        # V14.3.1 + Enhanced vague entity resolution:
        # - ContextEnricher (priority 30) tries to RESOLVE vague entities FIRST
        # - VagueEntityBlocker (priority 85) BLOCKS only unresolved entities
        # - BibliographicCitationParser fixes authorship + dedication issues
        # V14.3.2.1 additions:
        # - PraiseQuoteDetector v1.5.0 with author whitelist
        # - FrontMatterDetector (priority 12) for foreword signature correction
        modules = [
            # Book-specific (run first)
            PraiseQuoteDetector(config.get('praise_quote_detector', {})),  # V14.3.2.1: Enhanced with author whitelist
            MetadataFilter(config.get('metadata_filter', {})),
            FrontMatterDetector(config.get('front_matter_detector', {})),  # V14.3.2.1: NEW - Correct foreword signatures
            SubjectiveContentFilter(config.get('subjective_filter', {})),
            BibliographicCitationParser(config.get('bibliographic_parser', {})),  # V14.3.2: Enhanced authorship + dedication

            # Universal processing (resolve-then-block order)
            ContextEnricher(config.get('context_enricher', {})),  # V14.3.2: MOVED to priority 30, enhanced resolution
            ListSplitter(config.get('list_splitter', {})),
            PronounResolver(config.get('pronoun_resolver', {})),
            PredicateNormalizer(config.get('predicate_normalizer', {})),
            PredicateValidator(config.get('predicate_validator', {})),
            VagueEntityBlocker(config.get('vague_entity_blocker', {})),  # V14.3.2: MOVED to priority 85, flag-based blocking

            # Book-specific validation
            TitleCompletenessValidator(config.get('title_validator', {})),
            FigurativeLanguageFilter(config.get('figurative_filter', {})),

            # V11.2: Classification and deduplication
            ClaimClassifier(config.get('claim_classifier', {})),
            Deduplicator(config.get('deduplicator', {})),
        ]
    elif version == 'v14_3_1':
        # V14.3.1 Configuration (13 modules, A- target with factual-only filtering)
        # V13 + SubjectiveContentFilter for removing philosophical/metaphorical content
        modules = [
            # Book-specific (run first)
            PraiseQuoteDetector(config.get('praise_quote_detector', {})),
            SubjectiveContentFilter(config.get('subjective_filter', {})),  # NEW: Filter subjective content early
            BibliographicCitationParser(config.get('bibliographic_parser', {})),

            # Universal processing
            VagueEntityBlocker(config.get('vague_entity_blocker', {})),
            ListSplitter(config.get('list_splitter', {})),
            ContextEnricher(config.get('context_enricher', {})),
            PronounResolver(config.get('pronoun_resolver', {})),  # Enhanced with V14.3.1 fallback rules
            PredicateNormalizer(config.get('predicate_normalizer', {})),
            PredicateValidator(config.get('predicate_validator', {})),

            # Book-specific validation
            TitleCompletenessValidator(config.get('title_validator', {})),
            FigurativeLanguageFilter(config.get('figurative_filter', {})),

            # V11.2: Classification and deduplication
            ClaimClassifier(config.get('claim_classifier', {})),
            Deduplicator(config.get('deduplicator', {})),
        ]
    elif version == 'v13':
        # V13.1 Configuration (12 modules, A- grade baseline)
        # Removes: MetadataFilter, SemanticDeduplicator, ConfidenceFilter
        modules = [
            # Book-specific (run first)
            PraiseQuoteDetector(config.get('praise_quote_detector', {})),
            BibliographicCitationParser(config.get('bibliographic_parser', {})),

            # Universal processing
            VagueEntityBlocker(config.get('vague_entity_blocker', {})),
            ListSplitter(config.get('list_splitter', {})),
            ContextEnricher(config.get('context_enricher', {})),
            PronounResolver(config.get('pronoun_resolver', {})),
            PredicateNormalizer(config.get('predicate_normalizer', {})),
            PredicateValidator(config.get('predicate_validator', {})),

            # Book-specific validation
            TitleCompletenessValidator(config.get('title_validator', {})),
            FigurativeLanguageFilter(config.get('figurative_filter', {})),

            # V11.2: Classification and deduplication
            ClaimClassifier(config.get('claim_classifier', {})),
            Deduplicator(config.get('deduplicator', {})),
        ]
    else:
        # V14/V14.1 Configuration (15 modules, current)
        modules = [
            # Book-specific (run first)
            PraiseQuoteDetector(config.get('praise_quote_detector', {})),
            MetadataFilter(config.get('metadata_filter', {})),
            BibliographicCitationParser(config.get('bibliographic_parser', {})),

            # Universal processing
            VagueEntityBlocker(config.get('vague_entity_blocker', {})),
            ListSplitter(config.get('list_splitter', {})),
            ContextEnricher(config.get('context_enricher', {})),
            PronounResolver(config.get('pronoun_resolver', {})),
            PredicateNormalizer(config.get('predicate_normalizer', {})),
            PredicateValidator(config.get('predicate_validator', {})),

            # Book-specific validation
            TitleCompletenessValidator(config.get('title_validator', {})),
            FigurativeLanguageFilter(config.get('figurative_filter', {})),

            # V11.2 NEW: Classification and deduplication
            ClaimClassifier(config.get('claim_classifier', {})),
            Deduplicator(config.get('deduplicator', {})),

            # V14.1 NEW: Semantic deduplication using embeddings
            SemanticDeduplicator(config.get('semantic_deduplicator', {})),

            # V14 NEW: Confidence-based filtering (final module)
            ConfidenceFilter(config.get('confidence_filter', {})),
        ]

    # Create and return orchestrator
    return PipelineOrchestrator(modules)
