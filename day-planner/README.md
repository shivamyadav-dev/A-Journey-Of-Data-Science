# Focus Day Planner (Offline PWA)

A lightweight, offline-first planner tailored to your daily anchors in IST, with a 6-month Data Science roadmap, Pomodoro timer, typing and communication practice, and gamified points/streaks.

## Quick Start

- Serve locally (recommended to enable service worker):

```bash
cd /workspace/day-planner
python3 -m http.server 5173
```

Then open the URL your environment provides for port 5173.

- Or simply open `index.html` directly in a browser (service worker will be limited).

## Features

- Auto-plan your day around: Breakfast 08:30, Lunch 13:00, Dinner 21:10, Tuition 16:00–20:30
- 30 min Typing + 30 min Communication practice daily
- Deep Work blocks with Pomodoro timer
- Points and streaks to motivate consistency
- 6-month DS roadmap with weekly tasks
- Offline-ready PWA + Import/Export JSON backup

Data is stored locally in your browser (no server).