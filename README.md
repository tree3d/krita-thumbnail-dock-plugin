# krita-thumbnail-docker-plugin

Simple Krita Docker plugin that creates a dock with "clickable" thumbnail previews from the .kra files stored in a selected folder, ordered by date created descending.

## Description

This plugin provides a lightweight dock inside Krita that shows thumbnail previews for .kra files found in a user-selected folder. Thumbnails are displayed in descending order by file creation date so the most recent files appear first. Each thumbnail is clickable so you can quickly open the corresponding .kra file in Krita.

The project is packaged to run in a Docker environment to simplify dependencies and isolation for development and distribution, hence the "docker-plugin" name. The aim is to make browsing and opening recent Krita documents fast and convenient from within the Krita UI.

## Features

- Displays thumbnails for .kra files in a selected folder
- Orders thumbnails by creation date (newest first)
- Clickable thumbnails to open files in Krita
- Minimal, focused UI (dock) that integrates into Krita

## How it works (high level)

The plugin scans the configured folder for files with the .kra extension, generates or reads thumbnails for each file, sorts them by the file creation timestamp (descending), and renders them inside a dock panel in Krita. Clicking a thumbnail triggers opening that file in Krita.

## Prerequisites

- Krita (version compatible with Python plugins)

## Installation (overview)

1. Build or pull the Docker image provided in this repository (if you want to use Docker packaging).
2. Run the container or copy the plugin files into your Krita Python plugin directory.
3. Restart Krita and enable the plugin from the settings/plugins dialog (if required).
4. Use the plugin UI to select the folder containing your .kra files.

Note: Exact build/run commands and paths depend on your environment; see the repository's scripts or Dockerfile for specifics.

## Usage

- Open Krita.
- Open the plugin dock.
- Select the folder that contains your .kra files.
- Browse thumbnails (newest first) and click any thumbnail to open that file.

## Development

- The repository includes code to package and run the plugin in Docker for easier testing and distribution.
- To develop locally without Docker, copy the plugin into Krita's Python plugin directory and restart Krita to load the plugin.
