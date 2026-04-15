# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

EnergyMatch 1.0

A simple music recommender that finds songs matching your favorite genre, mood, and energy level.

---

## 2. Goal / Task

The system recommends 5 songs that match what a listener wants right now. It tries to predict: "What song matches this person's taste based on their favorite genre, preferred mood, and energy level (like calm vs. intense)?" This is a classroom project to understand how recommenders work, not a real production system.

---

## 3. Data Used

The dataset has 10 songs. Each song has a genre (pop, lofi, rock, jazz, etc.), mood (happy, chill, intense, etc.), and numeric features like energy (0-1 scale), tempo, danceability, and acousticness. There's limited diversity—only 1 jazz song, 1 ambient song, 1 synthwave song. Missing: classical, hip-hop, country, metal. The data is small and handpicked, so it doesn't represent the real world.

---

## 4. Algorithm Summary

The recommender scores each song on three things:
- Genre match: +1 point if the song matches your favorite genre exactly.
- Mood match: +1 point if the song matches your desired mood exactly.
- Energy match: 2 × (1 - difference) where difference is how far the song's energy is from your target. This is weighted twice as heavy as the other factors.

Then it picks the top 5 songs with the highest total score. The system completely ignores other song features like acousticness, even if you say you like acoustic music.

---

## 5. Data Features

The system loads these song attributes from a CSV file:
- id, title, artist: Basic song info
- genre, mood: Text labels for categorization
- energy, tempo_bpm, valence, danceability, acousticness: Numeric features (0-1 scale or beats per minute)

A user profile includes: favorite_genre, favorite_mood, target_energy, and likes_acoustic (a boolean flag that currently does nothing).  

---

## 6. Strengths

The system works really well for users with mid-range energy preferences (around 0.4-0.6). If you like pop music with a happy vibe and want high energy, it will correctly rank "Gym Hero" and "Sunrise City" at the top. Genre and mood matching are accurate when they're the same. If you want lofi + chill, you get lofi + chill songs.

---

## 7. Observed Behavior / Biases 

Energy is a wall, not a preference. The system weighted energy twice as important as genre or mood. This creates a "filter bubble": if you want high-energy music (0.9), you'll almost never see low-energy songs, even if they perfectly match your genre and mood. This traps extreme users in a narrow range. For a gym person who wants intense pop, a beautiful acoustic pop song gets buried because the energy gap is too big.

The system ignores the "likes_acoustic" preference entirely. You can tell the code you love acoustic guitars, but nothing changes. Acoustic lovers get acoustic songs by accident (when they match genre/mood), not by design.

Genre and mood are all-or-nothing. A pop fan searching for "happy" music will never see indie-pop if the genre field says "indie pop" instead of "pop". There's no partial credit. Users with rare tastes (like ambient or jazz) get very few options.

---

## 8. Evaluation Process

I tested 4 user profiles: a gym person (high energy pop fan), a study person (low energy lofi fan), a chill listener (mid-level lofi fan), and an acoustic jazz lover. For each profile, I looked at the top 5 recommendations and checked if they made sense.

The big surprise: extreme energy users (very high or very low) got locked into a narrow energy band. The gym person only saw songs with energy above 0.75. The study person only saw songs below 0.45. In the middle (0.4 energy), recommendations were reasonable. The acoustic preference test showed the system completely ignores it—two songs with 0.89 and 0.71 acousticness scored identically for the same user.

---

## 9. Intended Use and Non-Intended Use

Intended use: This is a classroom learning tool. It's meant to help students understand how music recommenders work, what biases they can have, and how weighting features affects results.

Non-intended use: Do NOT use this to recommend real music to real people. It has too many flaws: it only looks at genre, mood, and energy. It ignores artist diversity, user history, acoustic preferences, and dozens of other factors. Users will get stuck in filter bubbles. The dataset is too small and unrepresentative.

---

## 10. Ideas for Improvement

1. Actually use the "likes_acoustic" field. Add an acousticness score: if a user likes acoustic music, give songs with high acousticness extra points.

2. Reduce energy's power. Instead of weighting it 2×, weight it 1× like the others. Or make energy softer: reward songs within 0.2 of the target, instead of penalizing any difference so harshly. This lets users discover songs from adjacent energy ranges.

3. Add diversity to the top 5. Don't just pick the 5 highest-scoring songs—pick 1 from each genre, or pick songs with varying energy/acousticness even if they score lower. This breaks filter bubbles.

4. (Bonus) Allow partial genre matches. If someone likes "pop," they might also like "indie-pop" or "electropop". Use fuzzy matching or a genre similarity graph instead of exact string matching.  
