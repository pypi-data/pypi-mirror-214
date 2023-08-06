import mcfc


def success(*objects):
    mcfc.echo("&a✔&r", *objects)

def info(*objects):
    mcfc.echo("&bℹ&r", *objects)

def error(*objects):
    mcfc.echo("&c✖&r", *objects)

def warn(*objects):
    mcfc.echo("&e⚠&r", *objects)

