# zeldaspeedruns

`zeldaspeedruns` is the backend server of the ZeldaSpeedRuns website. It will provide, in the future, capabilities to
manage volunteers, schedule events, and more. Right now, the website is in very early stages.

## Quick start

### Requirements

There are several requirements that must be fulfilled before you can run `zeldaspeedruns`.

#### Python

The source base is automatically tested against Python 3.7, 3.8, and 3.9. Older versions may work but are not supported.
It is recommended that you use Python 3.9.

#### C/C++ Compiler

This project makes use of several compiled dependencies. If you are developing on Windows you will need to have a C/C++
build chain installed. You have a build chain installed if you selected that option during the Python installation, if
you didn't, you should
[follow these instructions](https://wiki.python.org/moin/WindowsCompilers#Microsoft_Visual_C.2B-.2B-_14.2_standalone:_Build_Tools_for_Visual_Studio_2019_.28x86.2C_x64.2C_ARM.2C_ARM64.29)
to install and set them up.

Alternatively, you can develop inside a Linux environment using WSL2.

### Set up instructions

**It is highly recommended you set up a virtual environment to isolate dependencies.**

1. Clone this repository.
2. (Optional, **highly recommended**) Run `python3 -m venv venv` and `source venv/bin/activate` to set up a virtual
   environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy `zeldaspeedruns/settings.py.example` to `zeldaspeedruns/settings.py`.
5. You will need to edit `settings.py` with your Twitch and Discord client credentials. Please see the section on
   *Configuration* below.
7. Run `python manage.py migrate` to initialize the database.
8. Run `python manage.py runserver` to start up the development server.
9. (Optional) Run `python manage.py createsuperuser` to create an administrative superuser that you can work with.
10. (Optional) Run `docker-compose up --build -d` to install services like a development SMTP server.

The application will now be running at `localhost:8000`. If the application refuses to run and spits out an error
because of missing credentials, please see the section below on Twitch/Discord API credentials.

## Configuration

### Twitch/Discord API Credentials

The ZSR website makes use of Discord and Twitch integration. In your `settings.py` set the values of
`SOCIAL_AUTH_DISCORD_KEY`, `SOCIAL_AUTH_DISCORD_SECRET`, `SOCIAL_AUTH_TWITCH_KEY`, and `SOCIAL_AUTH_TWITCH_SECRET` to
your developer keys.

- You can create a Discord API key here: https://discord.com/developers/applications
- You can create a Twitch API key here: https://dev.twitch.tv/console

### Running with Twitch and Discord integration

If you do not want to develop with Discord and Twitch functionality enabled, you can simply comment out the backends 
and their configuration in your `settings.py` file like this:

```python
AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.discord.DiscordOAuth2',
    # 'social_core.backends.twitch.TwitchOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# SOCIAL_AUTH_DISCORD_KEY = os.environ['SOCIAL_AUTH_DISCORD_KEY']
# SOCIAL_AUTH_DISCORD_SECRET = os.environ['SOCIAL_AUTH_DISCORD_SECRET']
# SOCIAL_AUTH_TWITCH_KEY = os.environ['SOCIAL_AUTH_TWITCH_KEY']
# SOCIAL_AUTH_TWITCH_SECRET = os.environ['SOCIAL_AUTH_TWITCH_SECRET']
```

#### SMTP Server

You may have noticed that if you tried to change or recover your password, that you will be met with an error screen.
While the site works fine for development without an SMTP server, you may want to set one up. For development purposes
there is a Docker Compose environment configured that provides an SMTP server.

To run it, simply execute `docker-compose up --build -d` from the repository root. You will need Docker installed on
your machine for this. You can find the SMTP's web environment on `localhost:8025`, which is where any mail sent by the
ZSR application will end up.

The SMTP server itself will be running on `localhost:1025`, which is the default configuration in `settings.py`, so it
should just work.

See also the Django documentation on
[configuring SMTP for dev](https://docs.djangoproject.com/en/3.2/topics/email/#configuring-email-for-development).
