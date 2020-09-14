CLI_NAME = project-cli

install: uninstall
	sudo cp ./$(CLI_NAME) /usr/bin/$(CLI_NAME)
	sudo chmod +x /usr/bin/$(CLI_NAME)

install-dev: uninstall
	sudo ln -s $(PWD)/$(CLI_NAME) /usr/bin/$(CLI_NAME)
	sudo chmod +x /usr/bin/$(CLI_NAME)

install-summon-provider:
	sudo mkdir -p /usr/local/lib/summon
	sudo cp ./$(CLI_NAME)-summon-provider /usr/local/lib/summon/kv-cli
	sudo chmod +x /usr/local/lib/summon/kv-cli

uninstall:
	sudo rm -f /usr/bin/$(CLI_NAME)