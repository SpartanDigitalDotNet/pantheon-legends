"""
Pantheon Legends Python Package

A Python implementation of the Pantheon Legends model for financial market analysis.
"""

from .contracts import (
    LegendRequest,
    LegendProgress,
    LegendEnvelope,
    QualityMeta,
    ILegendEngine
)
from .engines import DowLegendEngine
from .pantheon import Pantheon

__version__ = "0.1.0"
__all__ = [
    "LegendRequest",
    "LegendProgress", 
    "LegendEnvelope",
    "QualityMeta",
    "ILegendEngine",
    "DowLegendEngine",
    "Pantheon",
    "test_installation"
]


def test_installation():
    """
    Test if Pantheon Legends is properly installed and working.
    
    Returns:
        bool: True if installation is working correctly
    """
    try:
        # Test imports
        from datetime import datetime
        
        # Test basic functionality
        pantheon = Pantheon.create_default()
        engines = pantheon.available_engines
        
        # Test creating a request
        request = LegendRequest(
            symbol="TEST",
            timeframe="1d",
            as_of=datetime.now()
        )
        
        print("✅ Pantheon Legends Installation Test PASSED!")
        print(f"📦 Version: {__version__}")
        print(f"🔧 Available engines: {', '.join(sorted(engines))}")
        print(f"📋 Test request created: {request.symbol} ({request.timeframe})")
        print("🎉 Package is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Pantheon Legends Installation Test FAILED!")
        print(f"Error: {e}")
        return False
