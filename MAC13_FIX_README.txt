JOBHUNTERX — macOS 13 (Ventura) FIX

If you previously saw:
  ERROR: Playwright does not support chromium on mac13-arm64

Run:
  chmod +x FIX_MAC13_PLAYWRIGHT.sh
  ./FIX_MAC13_PLAYWRIGHT.sh
  ./START_JOBHUNTERX_MAC_LINUX.sh

This package pins Playwright 1.57.0 on macOS 13 because that release still provides Chromium downloads for mac13-arm64.

For macOS 14+, the same UI can be used normally.
