const widthModes = ['normal', 'wide', 'full'];
const widthLabels = {
  normal: 'Normal',
  wide: 'Wide',
  full: 'Full'
};

function toggleWidth() {
  const current = localStorage.getItem('widthMode') || 'normal';
  const idx = widthModes.indexOf(current);
  const next = widthModes[(idx + 1) % widthModes.length];
  localStorage.setItem('widthMode', next);
  applyWidth(next);
  updateWidthIcon(next);
}

function applyWidth(mode) {
  document.body.classList.remove('width-normal', 'width-wide', 'width-full');
  document.body.classList.add('width-' + mode);
  document.documentElement.classList.remove('width-normal', 'width-wide', 'width-full');
  document.documentElement.classList.add('width-' + mode);
}

function updateWidthIcon(mode) {
  const btn = document.getElementById('width-toggle');
  if (!btn) return;
  btn.innerHTML = widthLabels[mode];
  btn.title = 'Display size: ' + widthLabels[mode];
}

function toggleDarkMode() {
  const isDark = document.body.classList.toggle('dark-mode');
  if (isDark) {
    document.documentElement.classList.add('dark-mode');
  } else {
    document.documentElement.classList.remove('dark-mode');
  }
  localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
  updateIcon(isDark);
}

function updateIcon(isDark) {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  if (isDark) {
    btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 0 0 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>';
  } else {
    btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const isDark = localStorage.getItem('darkMode') !== 'disabled';
  if (isDark) {
    document.body.classList.add('dark-mode');
    document.documentElement.classList.add('dark-mode');
  }
  updateIcon(isDark);

  const widthMode = localStorage.getItem('widthMode') || 'normal';
  applyWidth(widthMode);
  updateWidthIcon(widthMode);
});
