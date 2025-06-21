#!/usr/bin/env python3
"""
Test script to verify ADK web server startup with the updated structure.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test orchestrator agent import
        from orchestrator_agent.agent import root_agent
        print("✅ Successfully imported root_agent")
        
        # Test sub-agent imports
        from orchestrator_agent.sub_agents.weather_agent.agent import weather_agent
        print("✅ Successfully imported weather_agent")
        
        from orchestrator_agent.sub_agents.tourist_spots_agent.agent import tourist_spots_agent
        print("✅ Successfully imported tourist_spots_agent")
        
        from orchestrator_agent.sub_agents.blog_writer_agent.agent import blog_writer_agent
        print("✅ Successfully imported blog_writer_agent")
        
        from orchestrator_agent.sub_agents.walking_routes_agent.agent import walking_routes_agent
        print("✅ Successfully imported walking_routes_agent")
        
        from orchestrator_agent.sub_agents.restaurant_recommendation_agent.agent import restaurant_recommendation_agent
        print("✅ Successfully imported restaurant_recommendation_agent")
        
        from orchestrator_agent.sub_agents.photo_story_agent.agent import photo_story_agent
        print("✅ Successfully imported photo_story_agent")
        
        print("\n🎉 All imports successful! The structure is correctly configured.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_adk_web_server():
    """Test that the ADK web server can be imported."""
    try:
        print("\nTesting ADK web server import...")
        import adk_web_server
        print("✅ Successfully imported adk_web_server")
        return True
    except Exception as e:
        print(f"❌ ADK web server import error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Travel Assistant Agent Structure")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_adk_web_server()
    
    if success:
        print("\n✅ All tests passed! You can now run the ADK web server.")
        print("\nTo start the services:")
        print("  ./start_all.sh    # Start all services")
        print("  ./start.sh        # Start with signal handling")
        print("  python adk_web_server.py  # Start ADK web only")
    else:
        print("\n❌ Some tests failed. Please check the structure and imports.")
        sys.exit(1) 