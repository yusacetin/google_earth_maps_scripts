## Scripts for Google Earth and Google Maps
Enable custom keyboard shortcuts that aren't officially available on Google Earth and Google Maps. The Google Earth update of October 2023 broke my previous JavaScript Chrome extension and since the new version uses a canvas that doesn't allow its sub elements to be accessed via DOM, I decided to use system-level keyboard shortcuts instead of browser-level.

### Keyboard Shortcuts
Alt + D: Toggle street view

Alt + S: Exit street view

Alt + F: Reset angle to North-top (only on Google Earth)

### Known Issues
Alt + F doesn't work on the Linux X11 script for some reason. Also, since Alt + D is already the default Google Chrome shortcut to focus the URL bar there might be a slight time window where the URL bar flashes every time this shortcut is activated. You can easily change the keys from the script files but I'm used to these keys from my old extension so I plan to keep these defaults for now.