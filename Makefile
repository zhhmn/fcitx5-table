HUMA_RIME_DIR ?= ${HOME}/.local/share/fcitx5/rime
FCITX5_USER_DIR ?= ${HOME}/.local/share/fcitx5

build:
	python transform.py $(HUMA_RIME_DIR)
	libime_tabledict huma.txt huma.main.dict
	libime_tabledict huma-ci.txt huma-ci.main.dict
	libime_tabledict huma-full.txt huma-full.main.dict
	libime_tabledict huma-ci-full.txt huma-ci-full.main.dict

deploy: build
	mkdir -p $(FCITX5_USER_DIR)/inputmethod
	cp huma{,-ci}{,-full}.conf $(FCITX5_USER_DIR)/inputmethod
	cp huma{,-ci}{,-full}.main.dict $(FCITX5_USER_DIR)/table

ICON_DIR := ${HOME}/.local/share/icons/hicolor/
APP_NAME := fcitx-tiger

deploy_icons:
	mkdir -p $(HOME)/.local/share/icons/hicolor/{16x16,24x24,48x48}/apps
		for size in 16x16 24x24 48x48; do \
			cp icons/tiger-$$size.png $(HOME)/.local/share/icons/hicolor/$$size/apps/fcitx-tiger.png; \
		done
	gtk-update-icon-cache -ft $(HOME)/.local/share/icons/hicolor/

zip: build
	zip -j huma-fcitx.zip huma*.conf huma*.main.dict icons/fcitx-tiger.png
