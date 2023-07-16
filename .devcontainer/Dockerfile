FROM mcr.microsoft.com/devcontainers/base:jammy
# FROM mcr.microsoft.com/devcontainers/base:jammy 

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=root

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \ 
    && apt-get install -y build-essential --no-install-recommends make \
    ca-certificates \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev

# Python and poetry installation
USER $USER
ARG HOME="/root"
ARG PYTHON_VERSION=3.10

ENV PYENV_ROOT="${HOME}/.pyenv" \
    LANG=C.UTF-8

ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH"

RUN echo "done 0" \
    && curl https://pyenv.run | bash \
    && echo "done 1" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "done 2" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "done 3" \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true


WORKDIR /workspace/sphinx-cli-help
COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install $(test "$RUN_ENV" == production && echo "--no-dev") --no-interaction --no-ansi --no-root --no-cache

# Cannot persist python version into build here so, get the python version and run all the commands the use it.
RUN MY_PY_VER=$(python -c "import sys; major, minor = sys.version_info[:2]; print(f'{major}.{minor}');" ) \
    && echo "Python version: $MY_PY_VER" \
    && echo "/workspace/sphinx-cli-help" >> "/workspace/sphinx-cli-help/.venv/lib/python$MY_PY_VER/site-packages/sphinx_cli_help.pth"

COPY ./.devcontainer/startup.sh /usr/local/bin/startup.sh
COPY ./.devcontainer/res/venv/bin/cli-hlp /workspace/sphinx-cli-help/.venv/bin/cli-hlp
COPY ./.devcontainer/root/bashrc.sh /root/.bashrc
COPY ./.devcontainer/root/bashrc_custom.sh /root/.bashrc_custom
RUN chmod +x /workspace/sphinx-cli-help/.venv/bin/cli-hlp \
    && chmod +x "/usr/local/bin/startup.sh"
