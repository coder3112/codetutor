#! /usr/bin/env sh

echo "Prestart"

# Run migrations
piccolo migrations new user --auto
piccolo migrations new session_auth --auto

# End