#/bin/sh

# This file is run when the container is started.
# If you need custom initialization, add them here.

# if using github codespace then add some aliases
if [ "$CODESPACES" == "true" ]; then
    git config --local alias.co "checkout"
    git config --local alias.br "branch"
    git config --local alias.ci "commit"
    git config --local alias.s "status -s"
    git config --local alias.type "cat-file -t"
    git config --local alias.dump "cat-file -p"
fi


if [ x"$LOCAL_GIT_AUTHOR_NAME" != "x" ]; then
    git config --local user.name "$LOCAL_GIT_AUTHOR_NAME" || true
fi
if [ x"$LOCAL_GIT_AUTHOR_EMAIL" != "x" ]; then
    git config --local user.email $LOCAL_GIT_AUTHOR_EMAIL || true
fi

echo "Startup Success!!!"
