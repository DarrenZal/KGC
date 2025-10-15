"""
Book-Specific Post-Processing Modules

Modules specifically designed for processing relationships extracted from books:
- Front matter processing (praise quotes, dedications, forewords)
- Bibliographic citation parsing
- Title validation and rehydration
- Figurative language handling
"""

from .praise_quote_detector import PraiseQuoteDetector
from .metadata_filter import MetadataFilter
from .front_matter_detector import FrontMatterDetector
from .dedication_normalizer import DedicationNormalizer
from .subtitle_joiner import SubtitleJoiner
from .bibliographic_citation_parser import BibliographicCitationParser
from .title_completeness_validator import TitleCompletenessValidator
from .figurative_language_filter import FigurativeLanguageFilter
from .subjective_content_filter import SubjectiveContentFilter

__all__ = [
    "PraiseQuoteDetector",
    "MetadataFilter",
    "FrontMatterDetector",
    "DedicationNormalizer",
    "SubtitleJoiner",
    "BibliographicCitationParser",
    "TitleCompletenessValidator",
    "FigurativeLanguageFilter",
    "SubjectiveContentFilter",
]
