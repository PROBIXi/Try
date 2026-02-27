"""Core parsing logic for defensive search-query analysis."""

from __future__ import annotations

import json
import re
import shlex
from dataclasses import asdict, dataclass
from typing import Dict, List

SUPPORTED_OPERATORS = {
    "site",
    "filetype",
    "inurl",
    "intitle",
    "intext",
    "ext",
    "cache",
}

RISKY_PATTERNS: Dict[str, re.Pattern[str]] = {
    "credential_keyword": re.compile(r"\b(password|passwd|secret|api[_-]?key|token)\b", re.IGNORECASE),
    "sensitive_file": re.compile(r"(\.env|id_rsa|wp-config\.php|config\.json|database\.sql)", re.IGNORECASE),
    "directory_listing": re.compile(r"\bindex\s+of\b", re.IGNORECASE),
}


@dataclass
class TokenInfo:
    kind: str
    value: str


@dataclass
class AnalysisResult:
    original_query: str
    tokens: List[TokenInfo]
    operators: Dict[str, List[str]]
    plain_terms: List[str]
    unsupported_operators: List[str]
    risk_signals: List[str]
    risk_score: int
    recommendation: str


def tokenize(query: str) -> List[str]:
    return shlex.split(query)


def parse_query(query: str) -> AnalysisResult:
    raw_tokens = tokenize(query)
    tokens: List[TokenInfo] = []
    operators: Dict[str, List[str]] = {op: [] for op in sorted(SUPPORTED_OPERATORS)}
    plain_terms: List[str] = []
    unsupported_ops: List[str] = []

    for token in raw_tokens:
        if ":" in token and not token.startswith('"'):
            maybe_op, operand = token.split(":", 1)
            op = maybe_op.lower()
            if op in SUPPORTED_OPERATORS:
                operators[op].append(operand)
                tokens.append(TokenInfo(kind="operator", value=token))
            else:
                unsupported_ops.append(op)
                tokens.append(TokenInfo(kind="unknown_operator", value=token))
        else:
            plain_terms.append(token)
            tokens.append(TokenInfo(kind="term", value=token))

    risk_signals: List[str] = []
    for key, pattern in RISKY_PATTERNS.items():
        if pattern.search(query):
            risk_signals.append(key)

    risk_score = min(len(risk_signals) * 30 + len(unsupported_ops) * 10, 100)

    if risk_score >= 60:
        recommendation = "High-risk query detected. Restrict execution and require manual approval."
    elif risk_score >= 30:
        recommendation = "Moderate risk. Log and review before use in automated workflows."
    else:
        recommendation = "Low risk for defensive/research usage."

    return AnalysisResult(
        original_query=query,
        tokens=tokens,
        operators={k: v for k, v in operators.items() if v},
        plain_terms=plain_terms,
        unsupported_operators=sorted(set(unsupported_ops)),
        risk_signals=sorted(risk_signals),
        risk_score=risk_score,
        recommendation=recommendation,
    )


def to_json(result: AnalysisResult) -> str:
    payload = asdict(result)
    payload["tokens"] = [asdict(t) for t in result.tokens]
    return json.dumps(payload, indent=2)
