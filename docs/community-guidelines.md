# Community Guidelines

Guidelines for contributing legends to the Pantheon Legends ecosystem.

## Overview

Pantheon Legends is a community-driven framework for sharing trading and investment analysis algorithms. These guidelines ensure quality, consistency, and usability across all community contributions.

## Legend Submission Process

### 1. Development Phase

**Create Your Legend:**
```bash
python -m legends create
```

Follow the interactive prompts to generate your legend template.

**Test Thoroughly:**
```python
# Unit tests
pytest test_your_legend.py

# Integration tests  
python examples.py
```

### 2. Documentation Requirements

Each legend must include:

1. **README file** with:
   - Clear description of the algorithm
   - Data sources and requirements
   - Expected performance characteristics
   - Usage examples
   - Author information

2. **Inline documentation:**
   ```python
   class YourLegend:
       """
       Brief description of your legend's purpose.
       
       This legend implements [algorithm name] to detect [market condition].
       It analyzes [data type] over [timeframe] to generate [signal type].
       
       Algorithm Details:
       - Method: Describe your approach
       - Indicators: List technical indicators used
       - Signals: Describe output signals
       
       Data Requirements:
       - Minimum history: X periods
       - Required fields: price, volume, etc.
       - Update frequency: real-time, daily, etc.
       
       Author: Your Name
       Version: 1.0.0
       License: MIT
       """
   ```

### 3. Code Quality Standards

**Structure Requirements:**
```python
class YourLegend:
    @property 
    def name(self) -> str:
        return "YourLegendName"  # Unique, descriptive name
    
    async def run_async(self, request, progress_callback=None):
        # Implementation
        pass
```

**Quality Checklist:**
- [ ] Follows async/await patterns
- [ ] Implements proper error handling  
- [ ] Reports progress for long operations
- [ ] Returns meaningful quality metrics
- [ ] Includes comprehensive type hints
- [ ] Has unit tests with >80% coverage
- [ ] Follows PEP 8 style guidelines
- [ ] No hardcoded credentials or secrets

## Naming Conventions

### Legend Names
- Use PascalCase: `MyAwesomeLegend`
- Be descriptive: `BollingerBandMeanReversion` not `BBMean`
- Avoid version numbers: `TrendFollower` not `TrendFollowerV2`
- Maximum 50 characters

### Signal Names
Standard signal fields (use when applicable):
```python
{
    # Primary signals
    "primary_signal": "buy" | "sell" | "hold",
    "signal_strength": 0.0,  # 0.0 to 1.0
    "signal_type": "breakout" | "reversal" | "continuation" | "neutral",
    
    # Price levels
    "entry_price": float,
    "stop_loss": float, 
    "take_profit": float,
    
    # Trend analysis
    "trend_direction": "bullish" | "bearish" | "sideways",
    "trend_strength": 0.0,  # 0.0 to 1.0
    
    # Risk metrics
    "risk_level": "low" | "medium" | "high",
    "confidence": 0.0,  # 0.0 to 1.0
    
    # Timeframe bias
    "short_term_bias": "bullish" | "bearish" | "neutral",
    "long_term_bias": "bullish" | "bearish" | "neutral"
}
```

Custom fields should be prefixed with your legend name:
```python
{
    "rsi_oversold": True,
    "macd_divergence": "bullish", 
    "volume_spike": 2.3
}
```

## Performance Standards

### Response Time
- **Target**: < 5 seconds for most analyses
- **Maximum**: < 30 seconds (with progress reporting)
- **Timeout**: Implement graceful timeout handling

### Resource Usage
- **Memory**: < 100MB per analysis
- **CPU**: Should not block event loop for > 100ms
- **Network**: Implement connection pooling and retries

### Data Quality
Always assess and report data quality:
```python
def _calculate_quality(self, data) -> QualityMeta:
    return QualityMeta(
        sample_size=len(data),
        freshness_sec=(datetime.now() - data['timestamp']).total_seconds(),
        data_completeness=self._assess_completeness(data)
    )
```

## Security Guidelines

### Data Handling
- Never log sensitive market data
- Implement data retention limits
- Use secure connections (HTTPS/WSS)
- Validate all external data

### API Keys
```python
# ✅ Good: Use environment variables
api_key = os.getenv("YOUR_API_KEY")

# ❌ Bad: Hardcoded secrets  
api_key = "sk-abc123..."
```

### Input Validation
```python
async def run_async(self, request, progress_callback=None):
    # Validate request
    if not request.symbol or len(request.symbol) > 20:
        raise ValueError("Invalid symbol")
    
    if request.timeframe not in ["1m", "5m", "15m", "1h", "4h", "1d"]:
        raise ValueError("Unsupported timeframe")
```

## Testing Requirements

### Unit Tests
Minimum test coverage for legend submission:

```python
import pytest
from datetime import datetime
from legends import LegendRequest

class TestYourLegend:
    
    @pytest.mark.asyncio
    async def test_basic_functionality(self):
        """Test basic legend execution"""
        legend = YourLegend()
        request = LegendRequest("BTC-USD", "1h", datetime.now())
        
        result = await legend.run_async(request)
        
        assert result.legend == legend.name
        assert isinstance(result.facts, dict)
        assert result.quality.sample_size >= 0
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error conditions"""
        legend = YourLegend()
        
        # Test invalid symbol
        request = LegendRequest("", "1h", datetime.now())
        with pytest.raises(ValueError):
            await legend.run_async(request)
    
    @pytest.mark.asyncio
    async def test_progress_reporting(self):
        """Test progress callbacks"""
        legend = YourLegend()
        request = LegendRequest("ETH-USD", "1h", datetime.now())
        
        progress_updates = []
        async def progress_handler(progress):
            progress_updates.append(progress)
        
        await legend.run_async(request, progress_handler)
        assert len(progress_updates) > 0
    
    def test_data_quality_assessment(self):
        """Test quality metrics calculation"""
        legend = YourLegend()
        
        # Test with good data
        good_data = {"prices": list(range(100))}
        quality = legend._calculate_quality(good_data)
        assert quality.sample_size == 100
        
        # Test with insufficient data
        bad_data = {"prices": [1, 2]}
        quality = legend._calculate_quality(bad_data)
        assert quality.sample_size == 2
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_pantheon_integration():
    """Test legend works with Pantheon orchestrator"""
    pantheon = Pantheon()
    pantheon.register_engine(YourLegend())
    
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    results = await pantheon.run_all_legends_async(request)
    
    assert len(results) == 1
    assert results[0].legend == "YourLegendName"
```

## Documentation Standards

### README Template
```markdown
# YourLegend

Brief description of what your legend does.

## Algorithm

Detailed explanation of your approach:
- Technical indicators used
- Signal generation logic
- Risk management features

## Usage

```python
from your_legend import YourLegend
from legends import LegendRequest, Pantheon

# Basic usage
legend = YourLegend()
request = LegendRequest("BTC-USD", "1h", datetime.now())
result = await legend.run_async(request)

# With Pantheon
pantheon = Pantheon()
pantheon.register_engine(YourLegend())
results = await pantheon.run_all_legends_async(request)
```

## Configuration

Environment variables:
- `YOUR_API_KEY`: API key for data source
- `YOUR_SETTING`: Custom configuration

## Signals

| Field | Type | Description |
|-------|------|-------------|
| primary_signal | str | Main trading signal |
| signal_strength | float | Confidence level (0-1) |
| custom_field | any | Your custom signals |

## Performance

- Response time: ~2 seconds
- Memory usage: ~10MB
- Data requirements: 100+ candles

## Author

Your Name (your.email@example.com)

## License

MIT License
```

### Code Comments
```python
class YourLegend:
    async def run_async(self, request, progress_callback=None):
        """
        Execute the legend analysis.
        
        Args:
            request: Analysis parameters
            progress_callback: Optional progress reporting function
            
        Returns:
            LegendEnvelope with analysis results
            
        Raises:
            ValueError: If request parameters are invalid
            DataSourceError: If unable to fetch market data
        """
        
        # Step 1: Fetch market data
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="fetching_data", percent=10.0
            ))
        
        data = await self._fetch_data(request.symbol, request.timeframe)
        
        # Step 2: Calculate technical indicators
        # Using 14-period RSI to identify overbought/oversold conditions
        rsi = self._calculate_rsi(data['prices'], period=14)
        
        # Step 3: Generate signals
        # Signal logic: RSI < 30 = oversold (buy), RSI > 70 = overbought (sell)
        signal = "buy" if rsi < 30 else "sell" if rsi > 70 else "hold"
```

## Submission Process

### 1. Prepare Submission Package
```
your_legend_submission/
├── your_legend.py          # Main legend implementation
├── test_your_legend.py     # Unit tests
├── README.md               # Documentation
├── requirements.txt        # Dependencies (if any)
└── examples/
    └── example_usage.py    # Usage examples
```

### 2. Quality Checklist
Before submission, verify:
- [ ] All tests pass with pytest
- [ ] Code follows style guidelines (run `black` and `flake8`)
- [ ] Documentation is complete and accurate
- [ ] No secrets or credentials in code
- [ ] Performance meets guidelines
- [ ] Error handling is comprehensive
- [ ] Progress reporting is implemented
- [ ] Quality metrics are meaningful

### 3. Submission Methods

**GitHub Pull Request:**
1. Fork the pantheon-legends repository
2. Add your legend to `community_legends/` directory
3. Update `community_legends/README.md` with your legend
4. Submit pull request with description

**Package Distribution:**
1. Create your own Python package
2. Use `pantheon-legends` as dependency
3. Publish to PyPI with `pantheon-legend-` prefix
4. Submit package info for community registry

## Community Support

### Getting Help
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check existing docs and examples
- **Code Review**: Request feedback before submission

### Contributing to Framework
Beyond legend development, you can contribute:
- Bug fixes and improvements
- Documentation enhancements  
- New testing tools
- Performance optimizations
- Integration examples

## License and Legal

### Recommended License
MIT License for maximum compatibility:

```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

### Intellectual Property
- Ensure you have rights to share your algorithm
- Respect third-party API terms of service
- Don't include copyrighted indicators without permission
- Clearly attribute any borrowed concepts or code

### Disclaimer Template
```python
"""
DISCLAIMER: This legend is for educational and research purposes only.
It should not be used as the sole basis for investment decisions.
Past performance does not guarantee future results.
Use at your own risk.
"""
```

## Version Control

### Semantic Versioning
Follow semver for legend versions:
- `1.0.0`: Initial stable release
- `1.0.1`: Bug fixes
- `1.1.0`: New features (backward compatible)
- `2.0.0`: Breaking changes

### Change Log
Maintain a CHANGELOG.md:
```markdown
# Changelog

## [1.1.0] - 2024-01-15
### Added
- Support for additional timeframes
- Volume analysis features

### Fixed  
- Edge case in signal calculation

### Changed
- Improved error handling
```

## Recognition

High-quality community legends may be featured:
- In official documentation
- In example collections
- In performance benchmarks
- At community events

Quality criteria for recognition:
- Consistent performance across market conditions
- Clean, well-documented code
- Active maintenance and support
- Positive community feedback

---

Together, we're building the future of algorithmic trading analysis. Thank you for contributing to the Pantheon Legends community!

Next: [Examples Collection](examples.md)
