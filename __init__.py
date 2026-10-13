"""Release Type in Title"""
#
# Copyright (C) 2026 Bob Swift
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <https://www.gnu.org/licenses/>.

# This plugin is based on the Picard 2 plugin "Release Type" by Elliot Chance.
# See original code at
# https://github.com/metabrainz/picard-plugins/blob/2.0/plugins/release_type/release_type.py

import re

from picard.plugin3.api import (
    Album,
    Metadata,
    OptionsPage,
    PluginApi,
    t_,
)

from .ui_options_release_type_in_title import Ui_ReleaseTypeInTitleOptionsPage


USER_GUIDE_URL = 'https://picard-plugins-user-guides.readthedocs.io/en/latest/release_type_in_title/user_guide.html'


class ReleaseTypeInTitleOptionsPage(OptionsPage):
    TITLE = t_("manifest.name", "Release Type in Title")
    HELP_URL = USER_GUIDE_URL

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ReleaseTypeInTitleOptionsPage()
        self.ui.setupUi(self)

        self.ui.cb_ep.clicked.connect(self._set_text_edit_states)
        self.ui.cb_single.clicked.connect(self._set_text_edit_states)
        self.ui.cb_soundtrack.clicked.connect(self._set_text_edit_states)
        self.ui.cb_live.clicked.connect(self._set_text_edit_states)
        self.ui.cb_remix.clicked.connect(self._set_text_edit_states)
        self.ui.cb_demo.clicked.connect(self._set_text_edit_states)

    def _set_text_edit_states(self):
        self.ui.add_text_ep.setEnabled(self.ui.cb_ep.isChecked())
        self.ui.add_text_single.setEnabled(self.ui.cb_single.isChecked())
        self.ui.add_text_soundtrack.setEnabled(self.ui.cb_soundtrack.isChecked())
        self.ui.add_text_live.setEnabled(self.ui.cb_live.isChecked())
        self.ui.add_text_remix.setEnabled(self.ui.cb_remix.isChecked())
        self.ui.add_text_demo.setEnabled(self.ui.cb_demo.isChecked())

        self.ui.words_ep.setEnabled(self.ui.cb_ep.isChecked())
        self.ui.words_single.setEnabled(self.ui.cb_single.isChecked())
        self.ui.words_soundtrack.setEnabled(self.ui.cb_soundtrack.isChecked())
        self.ui.words_live.setEnabled(self.ui.cb_live.isChecked())
        self.ui.words_remix.setEnabled(self.ui.cb_remix.isChecked())
        self.ui.words_demo.setEnabled(self.ui.cb_demo.isChecked())

    def load(self):
        self.ui.cb_ep.setChecked(self.api.plugin_config['enable_ep'])
        self.ui.cb_single.setChecked(self.api.plugin_config['enable_single'])
        self.ui.cb_soundtrack.setChecked(self.api.plugin_config['enable_soundtrack'])
        self.ui.cb_live.setChecked(self.api.plugin_config['enable_live'])
        self.ui.cb_remix.setChecked(self.api.plugin_config['enable_remix'])
        self.ui.cb_demo.setChecked(self.api.plugin_config['enable_demo'])

        self.ui.add_text_ep.setText(self.api.plugin_config['text_ep'])
        self.ui.add_text_single.setText(self.api.plugin_config['text_single'])
        self.ui.add_text_soundtrack.setText(self.api.plugin_config['text_soundtrack'])
        self.ui.add_text_live.setText(self.api.plugin_config['text_live'])
        self.ui.add_text_remix.setText(self.api.plugin_config['text_remix'])
        self.ui.add_text_demo.setText(self.api.plugin_config['text_demo'])

        self.ui.words_ep.setText(self.api.plugin_config['words_ep'])
        self.ui.words_single.setText(self.api.plugin_config['words_single'])
        self.ui.words_soundtrack.setText(self.api.plugin_config['words_soundtrack'])
        self.ui.words_live.setText(self.api.plugin_config['words_live'])
        self.ui.words_remix.setText(self.api.plugin_config['words_remix'])
        self.ui.words_demo.setText(self.api.plugin_config['words_demo'])

        self._set_text_edit_states()

    def save(self):
        self.api.plugin_config['enable_ep'] = self.ui.cb_ep.isChecked()
        self.api.plugin_config['enable_single'] = self.ui.cb_single.isChecked()
        self.api.plugin_config['enable_soundtrack'] = self.ui.cb_soundtrack.isChecked()
        self.api.plugin_config['enable_live'] = self.ui.cb_live.isChecked()
        self.api.plugin_config['enable_remix'] = self.ui.cb_remix.isChecked()
        self.api.plugin_config['enable_demo'] = self.ui.cb_demo.isChecked()

        self.api.plugin_config['text_ep'] = self.ui.add_text_ep.text()
        self.api.plugin_config['text_single'] = self.ui.add_text_single.text()
        self.api.plugin_config['text_soundtrack'] = self.ui.add_text_soundtrack.text()
        self.api.plugin_config['text_live'] = self.ui.add_text_live.text()
        self.api.plugin_config['text_remix'] = self.ui.add_text_remix.text()
        self.api.plugin_config['text_demo'] = self.ui.add_text_demo.text()

        self.api.plugin_config['words_ep'] = self.ui.words_ep.text().strip()
        self.api.plugin_config['words_single'] = self.ui.words_single.text().strip()
        self.api.plugin_config['words_soundtrack'] = self.ui.words_soundtrack.text().strip()
        self.api.plugin_config['words_live'] = self.ui.words_live.text().strip()
        self.api.plugin_config['words_remix'] = self.ui.words_remix.text().strip()
        self.api.plugin_config['words_demo'] = self.ui.words_demo.text().strip()

    def restore_defaults(self):
        super().restore_defaults()


def add_release_type(api: PluginApi, album: Album, album_metadata: Metadata, release_metadata: dict):

    title: str = album_metadata['album']
    words = set(re.findall(r'[a-z0-9\.]+', title.lower()))

    for r_type in ['ep', 'single', 'soundtrack', 'live', 'remix', 'demo']:
        if not api.plugin_config[f"enable_{r_type}"]:
            continue

        # Check if album is of the specified release type
        if r_type != album_metadata["~primaryreleasetype"] and r_type not in album_metadata["~secondaryreleasetype"]:
            continue

        # Check if replacement is defined
        replacement = str(api.plugin_config[f"text_{r_type}"])
        if not replacement.strip():
            continue

        # Check if replacement is already in the title
        if replacement.strip().lower() in title.lower():
            continue

        maps = set(str(api.plugin_config[f"words_{r_type}"]).lower().split())
        if not maps or words.intersection(maps):
            continue

        title += f" {replacement}"

    # Update title
    album_metadata['album'] = title


def enable(api: PluginApi):
    """Called when plugin is enabled."""

    # Register option settings
    api.plugin_config.register_option('enable_ep', True)
    api.plugin_config.register_option('enable_single', True)
    api.plugin_config.register_option('enable_soundtrack', False)
    api.plugin_config.register_option('enable_live', False)
    api.plugin_config.register_option('enable_remix', False)
    api.plugin_config.register_option('enable_demo', False)
    api.plugin_config.register_option('text_ep', api.tr("ui.option.ep.title", "(EP)"))
    api.plugin_config.register_option('text_single', api.tr("ui.option.single.title", "(Single)"))
    api.plugin_config.register_option('text_soundtrack', api.tr("ui.option.soundtrack.title", "(Soundtrack)"))
    api.plugin_config.register_option('text_live', api.tr("ui.option.live.title", "(Live)"))
    api.plugin_config.register_option('text_remix', api.tr("ui.option.remix.title", "(Remix)"))
    api.plugin_config.register_option('text_demo', api.tr("ui.option.demo.title", "(Demo)"))
    api.plugin_config.register_option('words_ep', "ep e.p.")
    api.plugin_config.register_option('words_single', "single")
    api.plugin_config.register_option('words_soundtrack', "soundtrack")
    api.plugin_config.register_option('words_live', "live")
    api.plugin_config.register_option('words_remix', "remix")
    api.plugin_config.register_option('words_demo', "demo demonstation")

    # Register options page
    api.register_options_page(ReleaseTypeInTitleOptionsPage)

    # Register album processor
    api.register_album_metadata_processor(add_release_type)
