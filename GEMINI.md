# GEMINI.md — Quick-Reference Commandments

1. **Data before prose**: Update `data/profile.json`, then run `python3 tools/profile_builder/build.py`.
2. **Verify before commit**:
   ```bash
   python3 -m compileall -q tools && \
   python3 tools/profile_builder/build.py --selftest && \
   python3 tools/profile_builder/build.py --check && \
   python3 -m unittest discover -s tools/profile_builder -v
   ```
3. **Zero emojis, zero private repo links, `CYBER RANGES` always uppercase two words.**
4. **3-tier promotion**: `beta/profile-rewrite` -> `staging` -> `main` (`--ff-only`), tagged via Lagopus taxonomy.
