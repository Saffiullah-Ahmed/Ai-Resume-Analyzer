from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class ResumeSchema:
    """
    Structured data schema representing extracted information from a resume.
    """
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    education: List[Dict[str, Any]] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    experience: List[Dict[str, Any]] = field(default_factory=list)
    projects: List[Dict[str, Any]] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the dataclass instance to a standard Python dictionary.
        """
        return asdict(self)