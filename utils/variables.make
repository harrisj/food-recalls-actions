PYTHON := pipenv run python -W ignore
JUPYTER := $(PYTHON) ./utils/run.py

# Define ANSI color codes
RESET_COLOR   = \033[m

BLUE       = \033[1;34m
YELLOW     = \033[1;33m
GREEN      = \033[1;32m
RED        = \033[1;31m
BLACK      = \033[1;30m
MAGENTA    = \033[1;35m
CYAN       = \033[1;36m
WHITE      = \033[1;37m

DBLUE      = \033[0;34m
DYELLOW    = \033[0;33m
DGREEN     = \033[0;32m
DRED       = \033[0;31m
DBLACK     = \033[0;30m
DMAGENTA   = \033[0;35m
DCYAN      = \033[0;36m
DWHITE     = \033[0;37m

BG_WHITE   = \033[47m
BG_RED     = \033[41m
BG_GREEN   = \033[42m
BG_YELLOW  = \033[43m
BG_BLUE    = \033[44m
BG_MAGENTA = \033[45m
BG_CYAN    = \033[46m

# Name some of the colors
COM_COLOR   = $(DBLUE)
OBJ_COLOR   = $(DCYAN)
OK_COLOR    = $(DGREEN)
ERROR_COLOR = $(DRED)
WARN_COLOR  = $(DYELLOW)
NO_COLOR    = $(RESET_COLOR)

OK_STRING    = "[OK]"
ERROR_STRING = "[ERROR]"
WARN_STRING  = "[WARNING]"

define start
    @echo "$(COM_COLOR)######$(NO_COLOR)\r";
    @echo "🚦 $(WARN_COLOR)Starting $(1) $(@F)$(NO_COLOR)\r";
endef

define finish
    @echo "🏁 $(OK_COLOR)Finished$(NO_COLOR)\r";
    @echo "$(COM_COLOR)------$(NO_COLOR)\r";
    @echo "\r";
endef

define python
    @echo "🐍🤖 $(OBJ_COLOR)Executing Python script $(1)$(NO_COLOR)\r";
    @$(PYTHON) $(1)
endef

define jupyter
    @echo "🐍🗒️ $(OBJ_COLOR)Executing Jupyter notebook $(1)$(NO_COLOR)\r";
    @$(JUPYTER) $(1)
endef

define make
    @echo "🔨🗒️ $(OBJ_COLOR)Executing Makefile $(1)$(NO_COLOR)\r";
	$(call start,$(MAKENAME))
    @$(MAKE) --no-print-directory -f $(1)
endef
