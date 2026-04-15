# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
from pathlib import Path
import math

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommends k songs for a user based on their profile.
        
        Args:
            user (UserProfile): User preferences
            k (int): Number of recommendations
            
        Returns:
            List[Song]: Top k recommended songs
        """
        # Convert UserProfile to dict format for scoring
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy
        }
        
        # Convert Song objects to dicts for scoring
        song_dicts = [
            {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness
            }
            for song in self.songs
        ]
        
        # Get recommendations with scores
        scored = recommend_songs(user_prefs, song_dicts, k)
        
        # Convert back to Song objects
        recommended_songs = []
        for song_dict, score, explanation in scored:
            song = Song(
                id=song_dict['id'],
                title=song_dict['title'],
                artist=song_dict['artist'],
                genre=song_dict['genre'],
                mood=song_dict['mood'],
                energy=song_dict['energy'],
                tempo_bpm=song_dict['tempo_bpm'],
                valence=song_dict['valence'],
                danceability=song_dict['danceability'],
                acousticness=song_dict['acousticness']
            )
            recommended_songs.append(song)
        
        return recommended_songs

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explains why a song was recommended for a user.
        
        Args:
            user (UserProfile): User preferences
            song (Song): The song to explain
            
        Returns:
            str: Explanation of the recommendation score
        """
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy
        }
        
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness
        }
        
        result = score_song(user_prefs, song_dict)
        score = result['total_score']
        reasons = ' | '.join(result['reasons'])
        return f"Score: {score:.2f} | {reasons}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and converts types appropriately.
    
    Args:
        csv_path (str): Path to the CSV file containing song data.
        
    Returns:
        List[Dict]: List of dictionaries where each dict represents a song.
        
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing or type conversion fails.
        
    Type Conversions:
        - id: int
        - energy, valence, danceability, acousticness: float (0.0-1.0)
        - tempo_bpm: int (beats per minute)
        - All other fields: str
    """
    # Validate file exists
    path = Path(csv_path)
    
    if not path.exists():
        raise FileNotFoundError(f"❌ CSV file not found: {csv_path}")
    
    songs = []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Validate header exists
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or has no header row")
            
            # Define which columns need type conversion
            float_fields = {'energy', 'valence', 'danceability', 'acousticness'}
            int_fields = {'id', 'tempo_bpm'}
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (skip header in count)
                try:
                    # Convert numeric fields
                    for field in float_fields:
                        if field in row:
                            value = row[field].strip()
                            row[field] = float(value)
                            # Validate range [0, 1] for normalized features
                            if not (0.0 <= row[field] <= 1.0):
                                raise ValueError(
                                    f"{field} must be between 0.0 and 1.0, got {row[field]}"
                                )
                    
                    for field in int_fields:
                        if field in row:
                            value = row[field].strip()
                            row[field] = int(value)
                            # Validate id and tempo are positive
                            if row[field] < 0:
                                raise ValueError(
                                    f"{field} must be non-negative, got {row[field]}"
                                )
                    
                    # Strip whitespace from string fields
                    for key in row:
                        if isinstance(row[key], str):
                            row[key] = row[key].strip()
                    
                    songs.append(row)
                    
                except (ValueError, KeyError) as e:
                    print(f"[WARNING] Skipping row {row_num}: {e}")
                    continue
        
        if not songs:
            raise ValueError("No valid songs were loaded from the CSV file")
        
        print(f"[OK] Successfully loaded {len(songs)} songs from {csv_path}")
        return songs
    
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"[ERROR] Error reading CSV file: {e}")

def score_song(user_prefs: Dict, song: Dict) -> Dict:
    """Scores a single song based on user preferences using genre, mood, and energy matching."""
    # Initialize
    total_score = 0.0
    reasons = []
    
    # Genre Match: +1.0 if matches (halved from +2.0)
    if song.get('genre', '').lower() == user_prefs.get('favorite_genre', '').lower():
        total_score += 1.0
        reasons.append('Matched favorite genre (+1.0)')
    
    # Mood Match: +1.0 if matches
    if song.get('mood', '').lower() == user_prefs.get('favorite_mood', '').lower():
        total_score += 1.0
        reasons.append('Matched desired mood (+1.0)')
    
    # Energy Score: 2 * (1 - abs(difference)) [doubled importance]
    target_energy = user_prefs.get('target_energy', 0.5)
    song_energy = song.get('energy', 0.5)
    energy_score = 2.0 * (1.0 - abs(song_energy - target_energy))
    total_score += energy_score
    reasons.append(f'Energy similarity ({energy_score:.2f})')
    
    return {
        'total_score': total_score,
        'reasons': reasons
    }


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns top k song recommendations scored and sorted by match to user preferences."""
    if not songs:
        return []
    
    # Pythonic approach: List comprehension to score all songs in one pass
    scored_songs = [
        (song, result['total_score'], ' | '.join(result['reasons']))
        for song in songs
        for result in [score_song(user_prefs, song)]  # Nested loop to capture result
    ]
    
    # Use sorted() to return new sorted list, sliced to top k results
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
