#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e
set -x  # Enable debug mode

# Define the directory containing .deb files
DEB_DIR="./debs"

# Ensure the debs directory exists
if [ ! -d "$DEB_DIR" ]; then
  echo "Directory $DEB_DIR does not exist."
  exit 1
fi

# List contents of DEB_DIR for debugging
ls -l "$DEB_DIR"

# Generate the new Packages file
dpkg-scanpackages -m "$DEB_DIR" > Packages.new

# If the existing Packages file exists, merge it with the new Packages file
if [ -f Packages ]; then
  # Backup the existing Packages file
  cp Packages Packages.old
  
  # Merge the Packages files, retaining descriptions from the old file
  awk 'BEGIN { RS = "" } FNR==NR { pkgs[$2] = $0; next } $2 in pkgs { sub($0, pkgs[$2]); } { print $0 "\n" }' FS='\n' RS='\n\n' Packages.new Packages.old > Packages
else
  mv Packages.new Packages
fi

# Compress the Packages file
bzip2 -fks Packages
gzip -fk Packages

# Create the Release file
cat <<EOF > Release
Origin: Axs Repo
Label: Axs Repo
Suite: stable
Version: 1.0
Codename: Axs Repo
Architectures: iphoneos-arm64 iphoneos-arm64e
Components: main
Description: 自用插件分享，有问题请卸载！！！
EOF
