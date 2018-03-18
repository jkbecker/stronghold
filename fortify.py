# FORTIFY
# @author Aaron Lichtman

# TODO
# -----
# install homebrew + brew securing steps (?)
#
# (When/where does this break? Valid version #s needed)
# Test to make sure this works with different versions
#
# Maybe turn this into a wrapper for: https://github.com/kristovatlas/osx-config-check/blob/master/app.py

import subprocess as sp
import sys


def prompt_yes_no(question):
	"""Print question and return True or False. Thanks, @shobrook"""
	valid = {"yes": True, "y": True, "ye": True, "": True, "no": False, "n": False}
	prompt = " [Y/n] "

	while True:
		print(question + prompt)
		choice = input().lower()
		if choice in valid:
			return valid[choice]
		else:
			print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def print_section_header(title):
	print("\n########\n" + "# " + title + "\n########\n")


def splash_intro():
	print(
		"\n88888888888                                       ad88 \n" +
		"88                                  ,d     **    d8/ \n" +
		"88                                  88           88 \n" +
		"88aaaaa   ,adPPYba,   8b,dPPYba,  MM88MMM  88  MM88MMM  8b       d8 \n" +
		"88`````  a8       8a  88P`   `Y8    88     88    88      8b     d8 \n" +
		"88       8b       d8  88            88     88    88       8b   d8 \n" +
		"88        8a,   ,a8   88            88,    88    88        8b,d8 \n" +
		"88         `YbbdP`    88            \Y888  88    88         Y88 \n" +
		"                                                            d8 \n" +
		"                                                           d8 \n")

	print("Fortify is a security configuration tool for MacOS Sierra and High Sierra.")
	print("You may be asked for the sudo password.")

	print_section_header("BEFORE RUNNING")

	print("Ensure you have up-to-date backups.")

	print_section_header("WARNINGS")

	print("\t1. This script modifies system settings. There is always the possibility it will damage your system.")
	print("\t2. Do not key-mash through this script. Things you do not want to happen might happen.\n")

	if not prompt_yes_no("I have read the above and want to continue."):
		sys.exit(0)


# I prayed to the sudo gods many times that these commands would work.
# Proceed at your own risk.

def connectivity_config():
	if prompt_yes_no("Turn on firewall?"):

		print("Enabling firewall...")
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setglobalstate', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("\n\tTurn on logging?"):
			print("Enabling logging...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setloggingmode', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("\n\tTurn on stealth mode?"):
			print("Enabling stealth mode...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setstealthmode', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("\n\tPrevent software from being whitelisted automatically?"):
			print("Preventing automatic whitelisting...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsigned', 'off'], stdout=sp.PIPE)
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsignedapp', 'off'], stdout=sp.PIPE)

		print("Resetting firewall to finalize changes...")
		sp.run(['sudo', 'pkill', '-HUP', 'socketfilterfw'], stdout=sp.PIPE)

	if prompt_yes_no("\nDisable Captive Portal Assistant and force login through browser?"):
		print("Disabling Captive Portal Assistant...")
		sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/SystemConfiguration/com.apple.captive.control', 'Active', '-bool', 'false'], stdout=sp.PIPE)


# TODO: Fix all the file not found errors
def metadata_storage_config():
	if prompt_yes_no("Clear language modeling, spelling and suggestion data and disable data collection?"):
		if prompt_yes_no("\tAre you sure?"):
			print("Removing language modeling, spelling and suggestion data and disabling data collection...")
			sp.run(['rm', '-rfv', '"~/Library/LanguageModeling/*"', '"~/Library/Spelling/*"', '"~/Library/Suggestions/*"'], stdout=sp.PIPE)
			sp.run(['chmod', '-R', '000', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)
			sp.run(['chflags', '-R', 'uchg', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)

	if prompt_yes_no("\nClear QuickLook metadata and disable data collection?"):
		print("Removing QuickLook metadata and disabling logging...")
		sp.run(['rm', '-rfv', '"~/Library/Application Support/Quick Look/*"'], stdout=sp.PIPE)
		sp.run(['chmod', '-R', '000', '"~/Library/Application Support/Quick Look"'], stdout=sp.PIPE)
		sp.run(['chflags', '-R', 'uchg', '"~/Library/Application Support/Quick Look"'], stdout=sp.PIPE)

	if prompt_yes_no("\nClear SiriAnalytics database and disable data collection? This will break Siri."):
		if prompt_yes_no("\tThis WILL break Siri. Are you sure you want to continue?"):
			if prompt_yes_no("\tLike really sure?"):
				print("Respectable choice. Removing Siri's complimentary monitoring services...")
				sp.run(['rm', '-rfv', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)
				sp.run(['chmod', '-R', '000', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)
				sp.run(['chflags', '-R', 'uchg', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)

	# TODO: Fix this... File Not Found Error
	# if prompt_yes_no("Clear Quarantine Data and disable data collection from downloaded files?"):
		# print("Clearing metadata and disabling logging...")
		# sp.run([':>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)
		# sp.run(['sudo', 'chflags', 'schg', '~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)


def general_safety_config():
	if prompt_yes_no("Lock Mac as soon as screen saver starts?"):
		print("Configuring...")
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPassword', '-int', '1'], stdout=sp.PIPE)
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPasswordDelay', '-int', '0'], stdout=sp.PIPE)

	if prompt_yes_no("\nDisplay all file extensions?"):
		print("Configuring...")
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'AppleShowAllExtensions', '-bool', 'true'], stdout=sp.PIPE)
	if prompt_yes_no("\nDisable saving to the cloud by default?"):
		print("Configuring...")
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'NSDocumentSaveNewDocumentsToCloud', '-bool', 'false'], stdout=sp.PIPE)
	if prompt_yes_no("\nShow hidden files in Finder?"):
		print("Configuring...")
		sp.run(['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-boolean', 'true'], stdout=sp.PIPE)


if __name__ == '__main__':
	splash_intro()

	print_section_header("CONNECTIVITY CONFIGURATION")
	connectivity_config()

	print_section_header("USER DATA COLLECTION")
	metadata_storage_config()

	print_section_header("GENERAL SAFETY")
	general_safety_config()

	print("Configuration complete!")