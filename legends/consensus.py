"""
Automatic consensus analysis for pantheon-legends
Uses real LegendEnvelope results to calculate weighted consensus
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import datetime as dt

from .contracts import LegendEnvelope, ReliabilityLevel


class ConsensusSignal(Enum):
    """Standardized consensus signals"""
    STRONG_BULLISH = "strong_bullish"
    BULLISH = "bullish" 
    NEUTRAL = "neutral"
    BEARISH = "bearish"
    STRONG_BEARISH = "strong_bearish"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass
class ConsensusResult:
    """
    Consensus analysis result from multiple legend engines
    """
    # Overall consensus
    signal: ConsensusSignal
    confidence: float  # 0.0 to 1.0
    strength: float    # 0.0 to 1.0
    
    # Engine breakdown
    engines_analyzed: int
    engines_bullish: int
    engines_bearish: int
    engines_neutral: int
    
    # Reliability weighting
    weighted_score: float  # -1.0 to 1.0 (bearish to bullish)
    reliability_average: float
    
    # Quality metrics
    consensus_quality: str  # "high", "medium", "low"
    
    # Engine contributions
    engine_contributions: Dict[str, Dict[str, Any]]
    
    # Analysis metadata
    analyzed_at: datetime


class ConsensusAnalyzer:
    """
    Analyzes real LegendEnvelope results to generate consensus
    """
    
    def __init__(self):
        self.reliability_weights = {
            ReliabilityLevel.HIGH: 1.0,
            ReliabilityLevel.MEDIUM: 0.7,
            ReliabilityLevel.VARIABLE: 0.5,
            ReliabilityLevel.EXPERIMENTAL: 0.3
        }
        
        self.signal_thresholds = {
            "strong": 0.7,
            "moderate": 0.3
        }
    
    def analyze(
        self,
        results: List[LegendEnvelope],
        min_reliability: Optional[ReliabilityLevel] = None
    ) -> ConsensusResult:
        """
        Calculate consensus from real engine results
        
        Args:
            results: List of LegendEnvelope results from engines
            min_reliability: Filter engines by minimum reliability
            
        Returns:
            ConsensusResult with weighted analysis
        """
        if not results:
            return self._create_insufficient_data_result()
        
        # Filter by reliability if specified
        if min_reliability:
            results = self._filter_by_reliability(results, min_reliability)
        
        if not results:
            return self._create_insufficient_data_result()
        
        # Extract signals from each engine result
        engine_signals = []
        for result in results:
            signal_data = self._extract_signal_from_result(result)
            if signal_data:
                engine_signals.append(signal_data)
        
        if not engine_signals:
            return self._create_insufficient_data_result()
        
        # Calculate weighted consensus
        weighted_score = self._calculate_weighted_score(engine_signals)
        confidence = self._calculate_confidence(engine_signals, weighted_score)
        signal = self._determine_signal(weighted_score)
        strength = abs(weighted_score)
        
        # Generate breakdown
        breakdown = self._generate_breakdown(engine_signals)
        
        # Calculate quality metrics
        reliability_avg = sum(s["reliability_weight"] for s in engine_signals) / len(engine_signals)
        quality = self._assess_quality(len(engine_signals), reliability_avg, confidence)
        
        # Generate contributions
        contributions = self._generate_contributions(engine_signals)
        
        return ConsensusResult(
            signal=signal,
            confidence=confidence,
            strength=strength,
            engines_analyzed=len(engine_signals),
            engines_bullish=breakdown["bullish"],
            engines_bearish=breakdown["bearish"], 
            engines_neutral=breakdown["neutral"],
            weighted_score=weighted_score,
            reliability_average=reliability_avg,
            consensus_quality=quality,
            engine_contributions=contributions,
            analyzed_at=datetime.now(dt.timezone.utc)
        )
    
    def _extract_signal_from_result(self, result: LegendEnvelope) -> Optional[Dict[str, Any]]:
        """Extract signal data from a LegendEnvelope result"""
        facts = result.facts
        
        # Try to find signal in common field names
        signal = None
        confidence = 0.5
        
        # Look for signal indicators
        signal_fields = [
            "signal", "position_bias", "recommendation", 
            "primary_trend", "market_phase", "trend_direction"
        ]
        
        for field in signal_fields:
            if field in facts:
                signal = facts[field]
                break
        
        # Look for confidence indicators  
        confidence_fields = [
            "confidence", "confidence_score", "strength", 
            "signal_strength", "quality_score"
        ]
        
        for field in confidence_fields:
            if field in facts:
                try:
                    confidence = float(facts[field])
                    confidence = max(0.0, min(1.0, confidence))
                    break
                except (ValueError, TypeError):
                    continue
        
        if signal is None:
            return None
        
        # Convert signal to numeric score
        numeric_signal = self._signal_to_numeric(signal)
        
        # Get reliability weight
        reliability_weight = self.reliability_weights.get(
            result.quality.reliability_level,
            0.5
        )
        
        return {
            "engine_name": result.legend,
            "signal": signal,
            "numeric_signal": numeric_signal,
            "confidence": confidence,
            "reliability_level": result.quality.reliability_level,
            "reliability_weight": reliability_weight,
            "final_weight": reliability_weight * confidence,
            "facts": facts
        }
    
    def _signal_to_numeric(self, signal: Any) -> float:
        """Convert signal to numeric score (-1.0 to 1.0)"""
        if isinstance(signal, (int, float)):
            return max(-1.0, min(1.0, float(signal)))
        
        if isinstance(signal, str):
            signal_lower = signal.lower().strip()
            
            # Strong signals
            if any(word in signal_lower for word in [
                "strong_bullish", "very_bullish", "markup", "breakout"
            ]):
                return 0.8
            
            if any(word in signal_lower for word in [
                "strong_bearish", "very_bearish", "markdown", "breakdown" 
            ]):
                return -0.8
            
            # Regular signals
            if any(word in signal_lower for word in [
                "bullish", "buy", "long", "accumulation", "uptrend"
            ]):
                return 0.5
            
            if any(word in signal_lower for word in [
                "bearish", "sell", "short", "distribution", "downtrend"
            ]):
                return -0.5
            
            # Neutral signals
            if any(word in signal_lower for word in [
                "neutral", "hold", "range", "sideways", "undetermined"
            ]):
                return 0.0
        
        return 0.0
    
    def _calculate_weighted_score(self, engine_signals: List[Dict[str, Any]]) -> float:
        """Calculate reliability and confidence weighted score"""
        total_weighted_signal = 0.0
        total_weight = 0.0
        
        for signal_data in engine_signals:
            weighted_signal = signal_data["numeric_signal"] * signal_data["final_weight"]
            total_weighted_signal += weighted_signal
            total_weight += signal_data["final_weight"]
        
        if total_weight == 0:
            return 0.0
        
        return total_weighted_signal / total_weight
    
    def _calculate_confidence(self, engine_signals: List[Dict[str, Any]], weighted_score: float) -> float:
        """Calculate confidence in consensus result"""
        if not engine_signals:
            return 0.0
        
        # Signal strength factor
        signal_strength = abs(weighted_score)
        
        # Agreement factor - how much engines agree
        signals = [s["numeric_signal"] for s in engine_signals]
        same_direction = sum(1 for s in signals if (s > 0) == (weighted_score > 0))
        agreement_factor = same_direction / len(signals)
        
        # Reliability factor
        avg_reliability = sum(s["reliability_weight"] for s in engine_signals) / len(engine_signals)
        
        # Combine factors
        confidence = (signal_strength * 0.4 + agreement_factor * 0.4 + avg_reliability * 0.2)
        return max(0.0, min(1.0, confidence))
    
    def _determine_signal(self, weighted_score: float) -> ConsensusSignal:
        """Determine consensus signal from weighted score"""
        if weighted_score >= self.signal_thresholds["strong"]:
            return ConsensusSignal.STRONG_BULLISH
        elif weighted_score >= self.signal_thresholds["moderate"]:
            return ConsensusSignal.BULLISH
        elif weighted_score <= -self.signal_thresholds["strong"]:
            return ConsensusSignal.STRONG_BEARISH
        elif weighted_score <= -self.signal_thresholds["moderate"]:
            return ConsensusSignal.BEARISH
        else:
            return ConsensusSignal.NEUTRAL
    
    def _generate_breakdown(self, engine_signals: List[Dict[str, Any]]) -> Dict[str, int]:
        """Generate breakdown of engine signals"""
        breakdown = {"bullish": 0, "bearish": 0, "neutral": 0}
        
        for signal_data in engine_signals:
            numeric = signal_data["numeric_signal"]
            if numeric > 0.1:
                breakdown["bullish"] += 1
            elif numeric < -0.1:
                breakdown["bearish"] += 1
            else:
                breakdown["neutral"] += 1
        
        return breakdown
    
    def _assess_quality(self, engine_count: int, reliability_avg: float, confidence: float) -> str:
        """Assess overall consensus quality"""
        if engine_count >= 3 and reliability_avg >= 0.7 and confidence >= 0.7:
            return "high"
        elif engine_count >= 2 and reliability_avg >= 0.5 and confidence >= 0.5:
            return "medium"
        else:
            return "low"
    
    def _generate_contributions(self, engine_signals: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Generate detailed engine contributions"""
        contributions = {}
        
        for signal_data in engine_signals:
            contributions[signal_data["engine_name"]] = {
                "signal": signal_data["signal"],
                "numeric_signal": signal_data["numeric_signal"],
                "confidence": signal_data["confidence"],
                "reliability_level": signal_data["reliability_level"].value,
                "weight_contribution": signal_data["final_weight"]
            }
        
        return contributions
    
    def _filter_by_reliability(self, results: List[LegendEnvelope], min_reliability: ReliabilityLevel) -> List[LegendEnvelope]:
        """Filter results by minimum reliability"""
        reliability_values = {
            ReliabilityLevel.HIGH: 4,
            ReliabilityLevel.MEDIUM: 3,
            ReliabilityLevel.VARIABLE: 2,
            ReliabilityLevel.EXPERIMENTAL: 1
        }
        
        min_value = reliability_values[min_reliability]
        
        return [
            result for result in results
            if reliability_values.get(result.quality.reliability_level, 0) >= min_value
        ]
    
    def _create_insufficient_data_result(self) -> ConsensusResult:
        """Create result when insufficient data"""
        return ConsensusResult(
            signal=ConsensusSignal.INSUFFICIENT_DATA,
            confidence=0.0,
            strength=0.0,
            engines_analyzed=0,
            engines_bullish=0,
            engines_bearish=0,
            engines_neutral=0,
            weighted_score=0.0,
            reliability_average=0.0,
            consensus_quality="insufficient",
            engine_contributions={},
            analyzed_at=datetime.utcnow()
        )
