# if using vs code insiders then create an alias as code for convienience
if ! which code >/dev/null && which code-insiders >/dev/null; then
    alias code=$(which code-insiders)
fi

# Add a new line at the end of the command prompt
PS1=${PS1%?}
PS1=${PS1%?}\\n'$ '
