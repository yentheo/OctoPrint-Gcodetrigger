# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import urllib2

class GcodetriggerPlugin(octoprint.plugin.SettingsPlugin,
                         octoprint.plugin.AssetPlugin,
                         octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/gcodetrigger.js"],
			css=["css/gcodetrigger.css"],
			less=["less/gcodetrigger.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			gcodetrigger=dict(
				displayName="Gcodetrigger Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="yentheo",
				repo="OctoPrint-Gcodetrigger",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/yentheo/OctoPrint-Gcodetrigger/archive/{target_version}.zip"
			)
		)

	def handle_camera_trigger(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode and gcode == "M240":
			self._logger.info("Just sent M240: {cmd}".format(**locals()))
			contents = urllib2.urlopen("http://192.168.1.55:5000/api/trigger-camera").read()



# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Gcodetrigger Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = GcodetriggerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.sent": __plugin_implementation__.handle_camera_trigger
	}

