# API Reference

Complete API documentation for the Pantheon Legends framework.

## Core Contracts

### LegendRequest

```python
@dataclass
class LegendRequest:
    """Request parameters for legend analysis"""
    symbol: str        # Trading symbol (e.g., "BTC-USD")
    timeframe: str     # Analysis timeframe (e.g., "1h", "1d")
    as_of: datetime    # Analysis timestamp
```

**Usage:**
```python
from datetime import datetime
from legends import LegendRequest

request = LegendRequest(
    symbol="ETH-USD",
    timeframe="4h", 
    as_of=datetime.now()
)
```

### LegendEnvelope

```python
@dataclass
class LegendEnvelope:
    """Result container from legend analysis"""
    legend: str           # Name of the legend that generated this result
    at: datetime         # When the analysis was performed
    tf: str             # Timeframe analyzed
    facts: Dict[str, Any]  # Analysis results and signals
    quality: QualityMeta   # Data quality metrics
```

**Usage:**
```python
from legends import LegendEnvelope, QualityMeta

result = LegendEnvelope(
    legend="MyLegend",
    at=datetime.now(),
    tf="1h",
    facts={
        "primary_signal": "buy",
        "signal_strength": 0.85,
        "entry_price": 45000.0
    },
    quality=QualityMeta(100.0, 30.0, 1.0)
)
```

### QualityMeta

```python
@dataclass
class QualityMeta:
    """Data quality assessment metrics"""
    sample_size: float      # Number of data points analyzed
    freshness_sec: float    # Age of data in seconds
    data_completeness: float # Percentage of expected data present (0.0-1.0)
```

**Usage:**
```python
quality = QualityMeta(
    sample_size=168.0,      # Analyzed 168 hourly candles (1 week)
    freshness_sec=45.0,     # Data is 45 seconds old
    data_completeness=0.98  # 98% of expected data points present
)
```

### ProgressCallback

```python
ProgressCallback = Callable[[LegendProgress], Awaitable[None]]
```

**Usage:**
```python
async def progress_handler(progress: LegendProgress):
    print(f"{progress.legend}: {progress.stage} ({progress.percent:.1f}%)")
    if progress.note:
        print(f"  Note: {progress.note}")

# Use with legend
result = await legend.run_async(request, progress_handler)
```

### LegendProgress

```python
@dataclass
class LegendProgress:
    """Progress reporting for legend execution"""
    legend: str            # Name of the legend reporting progress
    stage: str            # Current processing stage
    percent: float        # Completion percentage (0.0-100.0)
    note: Optional[str] = None  # Additional progress information
```

## Interfaces

### ILegendEngine

```python
class ILegendEngine(Protocol):
    """Protocol that all legend engines must implement"""
    
    @property
    def name(self) -> str:
        """Unique identifier for this legend"""
        ...
    
    async def run_async(
        self, 
        request: LegendRequest, 
        progress_callback: Optional[ProgressCallback] = None
    ) -> LegendEnvelope:
        """Execute legend analysis asynchronously"""
        ...
```

**Implementation Example:**
```python
from legends import ILegendEngine, LegendRequest, LegendEnvelope

class MyLegend:
    @property
    def name(self) -> str:
        return "MyCustomLegend"
    
    async def run_async(self, request, progress_callback=None):
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name,
                stage="initializing",
                percent=0.0
            ))
        
        # Your analysis logic here
        facts = {"primary_signal": "hold"}
        quality = QualityMeta(0.0, 0.0, 0.0)
        
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name,
                stage="complete",
                percent=100.0
            ))
        
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts=facts,
            quality=quality
        )
```

## Core Classes

### Pantheon

```python
class Pantheon:
    """Orchestrator for managing multiple legend engines"""
    
    def __init__(self):
        """Initialize empty pantheon"""
    
    def register_engine(self, engine: ILegendEngine) -> None:
        """Register a legend engine"""
    
    def get_registered_engines(self) -> List[str]:
        """Get list of registered engine names"""
    
    async def run_single_legend_async(
        self, 
        legend_name: str, 
        request: LegendRequest,
        progress_callback: Optional[ProgressCallback] = None
    ) -> LegendEnvelope:
        """Run a specific legend engine"""
    
    async def run_all_legends_async(
        self, 
        request: LegendRequest,
        progress_callback: Optional[ProgressCallback] = None
    ) -> List[LegendEnvelope]:
        """Run all registered legend engines concurrently"""
    
    async def run_multiple_legends_async(
        self, 
        legend_names: List[str], 
        request: LegendRequest,
        progress_callback: Optional[ProgressCallback] = None
    ) -> List[LegendEnvelope]:
        """Run specified legend engines concurrently"""
```

**Usage Example:**
```python
import asyncio
from datetime import datetime
from legends import Pantheon, LegendRequest

async def main():
    # Create pantheon
    pantheon = Pantheon()
    
    # Register engines
    pantheon.register_engine(MyLegend())
    pantheon.register_engine(AnotherLegend())
    
    # Create request
    request = LegendRequest(
        symbol="BTC-USD",
        timeframe="1h",
        as_of=datetime.now()
    )
    
    # Run all legends
    results = await pantheon.run_all_legends_async(request)
    
    for result in results:
        print(f"{result.legend}: {result.facts}")

asyncio.run(main())
```

## Built-in Legend Engines

### DowLegendEngine

```python
class DowLegendEngine:
    """Demo implementation of Dow Theory principles"""
    
    @property
    def name(self) -> str:
        return "DowTheory"
    
    async def run_async(self, request, progress_callback=None) -> LegendEnvelope:
        """Analyze trends based on Dow Theory"""
```

**Facts Generated:**
- `primary_trend`: "bullish", "bearish", or "sideways"
- `trend_strength`: 0.0 to 1.0
- `trend_duration_days`: Number of days trend has been active
- `support_level`: Identified support price level
- `resistance_level`: Identified resistance price level

### WyckoffLegendEngine

```python
class WyckoffLegendEngine:
    """Demo implementation of Wyckoff market cycle analysis"""
    
    @property
    def name(self) -> str:
        return "Wyckoff"
    
    async def run_async(self, request, progress_callback=None) -> LegendEnvelope:
        """Analyze market phase based on Wyckoff method"""
```

**Facts Generated:**
- `market_phase`: "accumulation", "markup", "distribution", or "markdown"
- `phase_confidence`: 0.0 to 1.0
- `volume_analysis`: "increasing", "decreasing", or "stable"
- `price_action`: "strong", "weak", or "neutral"
- `cycle_position`: "early", "middle", or "late"

## CLI Tools

### Scaffold Command

Create new legend from existing scanner code:

```bash
python -m legends create
```

**Interactive Prompts:**
1. Scanner name
2. Description
3. Analysis type (Technical/Fundamental/Sentiment)
4. Signal types generated
5. Data sources used
6. Output file location

**Generated Files:**
- `{scanner_name}_legend.py` - Legend implementation template
- `test_{scanner_name}_legend.py` - Unit test template
- `README_{scanner_name}.md` - Documentation template

## Utility Functions

### test_installation

```python
def test_installation() -> bool:
    """Test if package is properly installed"""
```

**Usage:**
```python
from legends import test_installation

if test_installation():
    print("Package installed correctly!")
else:
    print("Package installation issues detected")
```

## Exception Handling

### Common Exceptions

```python
# Data-related errors
class InsufficientDataError(Exception):
    """Raised when not enough data for analysis"""
    pass

# API-related errors  
class DataSourceError(Exception):
    """Raised when data source is unavailable"""
    pass

# Analysis errors
class AnalysisError(Exception):
    """Raised when analysis computation fails"""
    pass
```

**Error Handling Pattern:**
```python
async def run_async(self, request, progress_callback=None):
    try:
        data = await self._fetch_data(request.symbol)
        return await self._analyze(data, request)
    except InsufficientDataError:
        # Return neutral result
        return self._create_neutral_result(request, "Insufficient data")
    except DataSourceError as e:
        # Log error and return error result
        self.logger.error(f"Data source error: {e}")
        return self._create_error_result(request, str(e))
    except Exception as e:
        # Unexpected error
        self.logger.exception("Unexpected error in analysis")
        return self._create_error_result(request, "Analysis failed")
```

## Type Hints Reference

### Import Statements
```python
from typing import Dict, List, Any, Optional, Callable, Awaitable, Protocol
from dataclasses import dataclass
from datetime import datetime
```

### Common Type Aliases
```python
# Market data structure
MarketData = Dict[str, Any]

# Signal dictionary
SignalDict = Dict[str, Any]

# Progress callback function
ProgressCallback = Callable[[LegendProgress], Awaitable[None]]

# Legend engine list
EngineList = List[ILegendEngine]
```

## Configuration

### Environment Variables

```bash
# Data source configuration
MARKET_API_KEY=your_api_key_here
MARKET_API_URL=https://api.yourprovider.com
REQUEST_TIMEOUT=30

# Caching configuration
CACHE_TTL=60
CACHE_MAX_SIZE=1000

# Logging configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Configuration Class
```python
@dataclass
class LegendConfig:
    api_key: str = ""
    base_url: str = "https://api.example.com"
    timeout: int = 30
    cache_ttl: int = 60
    max_retries: int = 3
    
    @classmethod
    def from_env(cls) -> 'LegendConfig':
        """Load configuration from environment variables"""
        return cls(
            api_key=os.getenv("MARKET_API_KEY", ""),
            base_url=os.getenv("MARKET_API_URL", "https://api.example.com"),
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            cache_ttl=int(os.getenv("CACHE_TTL", "60")),
            max_retries=int(os.getenv("MAX_RETRIES", "3"))
        )
```

## Version Information

Current package version: `0.1.0`

**Compatibility:**
- Python 3.8+
- AsyncIO support required
- Type hints supported

**Dependencies:**
- No external dependencies required for core functionality
- Optional: `aiohttp` for HTTP requests
- Optional: `pandas` for data analysis
- Optional: `numpy` for numerical computations

## Migration Guide

### From Version 0.0.x to 0.1.0

No breaking changes in this version.

Next: [Community Guidelines](community-guidelines.md)
