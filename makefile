APP_DIR=hacktheplanet

.PHONY: test list clean

test:
	mpremote mkdir :/apps/${APP_DIR}
	mpremote cp app.py :/apps/${APP_DIR}/app.py
	mpremote cp metadata.json :/apps/${APP_DIR}/metadata.json
	make reset

reset:
	mpremote reset

list:
	mpremote fs ls :/apps
	mpremote fs ls :/apps/${APP_DIR} || echo "No app dir"

clean:
	mpremote fs rm :/apps/${APP_DIR}/app.py || true
	mpremote fs rm :/apps/${APP_DIR}/metadata.json || true
	mpremote fs rmdir :/apps/${APP_DIR}
