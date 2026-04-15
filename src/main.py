# -*- coding: utf-8 -*-
"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # Try relative import (when run as module: python -m src.main)
    from .recommender import load_songs, recommend_songs
except ImportError:
    # Fallback to absolute import (when run as script: python src/main.py)
    from recommender import load_songs, recommend_songs


def main() -> None:
    # Step 1: Load songs from CSV
    songs = load_songs("data/songs.csv")
    print(f"[OK] Loaded songs: {len(songs)}\n")

    # ========== PHASE 4: TEST PROFILES ==========
    
    # STANDARD PROFILES
    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9
    }
    
    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35
    }
    
    deep_intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.85
    }
    
    # ADVERSARIAL/EDGE CASE PROFILES
    # The Conflict: User wants high energy but a mood that doesn't exist in data
    the_conflict = {
        "favorite_genre": "pop",
        "favorite_mood": "sad",  # Doesn't exist in data
        "target_energy": 0.9
    }
    
    # The Outlier: User wants a genre that doesn't exist in data
    the_outlier = {
        "favorite_genre": "trance",  # Doesn't exist in data
        "favorite_mood": "happy",
        "target_energy": 0.7
    }
    
    # The Neutralist: User has mid-range energy and no specific preferences
    the_neutralist = {
        "favorite_genre": "",
        "favorite_mood": "",
        "target_energy": 0.5
    }
    
    # Step 2: Create user preference profile
    # Example user profile: "Chill Study" - lofi, calm mood, low energy
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "calm",
        "target_energy": 0.2
    }
    
    print("[PROFILE] User Profile:")
    print(f"   Genre: {user_prefs['favorite_genre'].upper()}")
    print(f"   Mood:  {user_prefs['favorite_mood'].upper()}")
    print(f"   Energy Level: {user_prefs['target_energy']:.1%}\n")

    # Step 3: Get recommendations
    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Display recommendations with clean formatting
    print("=" * 75)
    print("[MUSIC] TOP 5 RECOMMENDATIONS")
    print("=" * 75 + "\n")
    
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        # Parse reasons from explanation string
        reasons = explanation.split(' | ')
        
        # Format header
        print(f"#{rank} [*] {score:.2f} points")
        print(f"   {song['title']}")
        print(f"   by {song['artist']}")
        
        # Format reasons with bullet points
        print(f"   Why we picked this:")
        for reason in reasons:
            print(f"      - {reason}")
        
        # Add separator between recommendations
        if rank < len(recommendations):
            print("\n" + "-" * 75 + "\n")
        else:
            print("\n" + "=" * 75)


if __name__ == "__main__":
    main()
