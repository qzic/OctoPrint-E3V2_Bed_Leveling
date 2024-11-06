# OctoPrint Bed Leveling Plugin. Allows user to easily level 3D printer.
# Copyright (C) 2018  electr0sheep
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email: electr0sheep@electr0sheep.com

from __future__ import absolute_import

from octoprint.settings import settings
import octoprint.plugin


class E3V2_LevelingPlugin(octoprint.plugin.AssetPlugin,
                          octoprint.plugin.TemplatePlugin,
                          octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.StartupPlugin):

    def on_after_startup(self):
        s = settings()

        controlList = s.get(["controls"])

        for item in controlList:
            if (item['name'] == 'Bed Leveling++'):
                controlList.remove(item)

        s.set(["controls"], controlList)

    def get_settings_defaults(self):
        return dict(bed_temp=60, nozzle_temp=200, play_tune=True,
                    wait_for_heat=True, front_left_x=30, front_left_y=30,
                    front_right_x=190, front_right_y=30, back_left_x=30,
                    back_left_y=190, back_right_x=190, back_right_y=190,
                    center_x=110, center_y=110, lower_z=0, upper_z=10, final_z=40,
                    wait_for_tweak=5000, wait_after_tweak=2000, feed_rate=3600, heat_simultaneously=False, autolevel="")

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def get_assets(self):
        return dict(js=["e3v2leveling.js"])

    def get_update_information(self):
        return dict(
            E3V2_Leveling=dict(
                displayName="Bed Leveling Plugin++",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="qzic",
                repo="OctoPrint-E3V2_Leveling",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/qzic/OctoPrint-E3V2_Leveling/archive/{target_version}.zip"
            )
        )


__plugin_name__ = "Bed Leveling Plugin++"
__plugin_pythoncompat__ = ">=2.7, <4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = E3V2_LevelingPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
