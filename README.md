# Release Type in Title

## Overview

This plugin automatically places selected release type information in the title of the release.

The plugin is based on the Picard 2 plugin "Release Type" by Elliot Chance. See https://github.com/metabrainz/picard-plugins/blob/2.0/plugins/release_type/release_type.py for the original Picard 2 plugin code.

---

## What it Does

The plugin checks the existing release title to determine whether the release type already appears in the title. If not, and the release type is one of those selected for inclusion, the release type is added to the release title.

The release types to include, and the text to add are defined by the user in the plugin's option settings.

---

## Contributing

Please see the [Contribution Guidelines for MusicBrainz Picard Plugins](https://github.com/metabrainz/picard-plugins-registry/blob/main/PLUGIN_CONTRIBUTING.md) on how to help with development of this plugin.
