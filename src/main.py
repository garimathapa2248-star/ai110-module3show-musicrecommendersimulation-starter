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
