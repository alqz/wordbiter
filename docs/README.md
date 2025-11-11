# Word Bites AI Solver - GitHub Pages Version

This is the static web version of the Word Bites AI Solver, ready for GitHub Pages deployment.

## What's Included

- `index.html` - Main web interface
- `style.css` - Styling
- `script.js` - Frontend logic with dual-mode support (local/server)
- `solver.js` - Browser-based word-finding algorithm
- `scrabble_words.txt` - Dictionary file (178,590 words, 1.7MB)

## How It Works

The solver runs entirely in your browser:
1. Dictionary loads on page load (~1.7MB, one-time download)
2. All word-finding happens client-side using JavaScript
3. No server required after initial page load

## Local Testing

To test locally before deploying:

```bash
# From this directory
python3 -m http.server 8080

# Then open http://localhost:8080 in your browser
```

## Deploying to GitHub Pages

### Step 1: Push to GitHub

If you haven't already, initialize a git repository and push to GitHub:

```bash
# From the wordbiter root directory
git init
git add .
git commit -m "Add Word Bites AI Solver with GitHub Pages support"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** → **Pages** (in the left sidebar)
3. Under "Source", select **Deploy from a branch**
4. Under "Branch", select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

### Step 3: Access Your Site

After a few minutes, your site will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

## Features

- **Local Solver Mode (Default)**: All computation happens in browser
- **Server Mode**: Falls back to API if you deploy with a backend
- **Fast Performance**: Prefix pruning and efficient backtracking
- **Mobile Responsive**: Works on all devices
- **No Installation**: Just open the URL and start solving

## Note

The "Server (API)" mode will not work on GitHub Pages since it's static hosting only. The solver defaults to "Local (Browser)" mode which works perfectly without any server.
