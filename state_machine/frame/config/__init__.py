from config.driver import driver_config as dc

driver_config = dc
application_config = {}
try:
    import application_config as ac
    if hasattr(ac, 'application_config'):
        application_config = ac.application_config
    if hasattr(ac, 'driver_config'):
        for param in ac.driver_config:
            driver_config[param] = ac.driver_config[param]
except ImportError:
    print('No application config found')
