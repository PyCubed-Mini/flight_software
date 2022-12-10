# driver
mkdir -p lib/configuration
find ./lib -type f -exec chmod 644 {} + # make files writable to update them
cp ../state_machine/drivers/pycubedmini/lib/pycubed_rfm9x_fsk.py ./lib/
cp ../state_machine/drivers/pycubedmini/lib/configuration/radio_configuration.py ./lib/configuration/
find ./lib -type f -exec chmod 444 {} + # make files read-only to prevent changes

# tasko
mkdir -p tasko
find ./tasko -type f -exec chmod 644 {} + # make files writable to update them
cp -r ../state_machine/frame/tasko ./
find ./tasko -type f -exec chmod 444 {} + # make files read-only to prevent changes

# radio_utils
mkdir -p radio_utils
find ./radio_utils -type f -exec chmod 644 {} + # make files writable to update them
cp -r ../state_machine/applications/flight/lib/radio_utils ./
find ./radio_utils -type f -exec chmod 444 {} + # make files read-only to prevent changes