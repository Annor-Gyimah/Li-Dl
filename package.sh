#!/bin/sh
# Create folders.
[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/opt/main
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

# Copy files (change icon names, add lines for non-scaled icons)
cp -r Lin_Exec/main package/opt/main/
cp  Lin_Exec/penguin.png package/usr/share/icons/hicolor/scalable/apps/penguin.png
cp  Lin_Exec/main.desktop package/usr/share/applications

# Change permissions
find package/opt/main -type f -exec chmod 644 -- {} +
find package/opt/main -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/main/main
