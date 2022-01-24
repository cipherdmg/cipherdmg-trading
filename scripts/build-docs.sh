# shellcheck shell=bash
###############################################################################
# @author Cipher DMG (cipherdmg@gmail.com)
# @file build-docs.sh
# @description A library to setup read the docs
#   * https://docs.readthedocs.io
#
#

#
###############################################################################
# shellcheck disable=SC2164,SC1091,SC2129,SC2120,SC2145,SC2155
#[SOURCE]
# shellcheck source=common-functions.sh
source "${SCRIPTS_HOME}/common/common-functions.sh"

# shellcheck source=windows/beyond-compare.sh
source "${SCRIPTS_HOME}/windows/beyond-compare.sh"

#--------------------------- Environment Variables ---------------------------#
#[REQUIRED]
if [[ -z "${CIPHERDMG_HOME}" ]] ; then export CIPHERDMG_HOME="${DEV_PROJECTS}/cipherdmg-trading"; fi
if [[ -z "${CIPHERDMG_HOME_PROJECT}" ]] ; then export CIPHERDMG_HOME_PROJECT="${CIPHERDMG_HOME##*/}"; fi

#[REQUIRED]
export TRADING_VIEW_BACKUP_DIR="${CIPHERDMG_HOME}/tradingview/backup"
export STRATBOT_PY="${CIPHERDMG_HOME}/stratbot/stratbot.py"
export STRATBOTAPI_PY="${CIPHERDMG_HOME}/stratbot/stratbotapi.py"
export STRATBOT_BACKUP_DIR="${CIPHERDMG_HOME}/stratbot/backup"

export INDICATOR_PINE="${CIPHERDMG_HOME}/tradingview/cypherdmg-the-strat.pine"

#[DEFAULTS]


#[CONSTANTS]

#-------------------------------- Alias Values -------------------------------#
alias cdc="cd ${CIPHERDMG_HOME}"

#--------------------------------- Sourcing ----------------------------------#
#[SOURCE]

#[ALL_VARIABLES_ARRAY]

#============================= Script Functions ==============================#

###############################################################################
# @description Daily Backup
#
# @noargs
#
backupIB(){
    local description=("Backup Interactive Broker Trader Workstation" "${@}")
    if logEntry "${description[@]}" ; then return ;fi

    datestamp #Initialize a new DATESTAMP for the backup

    #Backup Development
    rmf "${DEV_PROJECTS}/Jts"

    cpf "/c/Jts" "${DEV_PROJECTS}/Jts"

    backupDevProject "${DEV_PROJECTS}/Jts"

    rmf "${DEV_PROJECTS}/Jts"

    logExit #Call Exit Function
}


###############################################################################
# @description Backup questrade.py
# @noargs
# @internal
#
backupStratBot(){
    backupFile "${STRATBOT_PY}" "${STRATBOT_BACKUP_DIR}"
    backupFile "${STRATBOTAPI_PY}" "${STRATBOT_BACKUP_DIR}"
}

###############################################################################
# @description Backup cypherdmg-the-strat.pine
# @noargs
# @internal
#
backupTradingviewIndicator(){ backupFile "${INDICATOR_PINE}" "${TRADING_VIEW_BACKUP_DIR}";}



###############################################################################
# @description Install MKDocs for Python
#   * [MKDocs](https://www.mkdocs.org)
#   * [MKDocs Read The Docs](https://docs.readthedocs.io/en/stable/intro/getting-started-with-mkdocs.html)
#   * [Setup Sphinx Theme](https://github.com/readthedocs/sphinx_rtd_theme)
#
# @internal
#
installMkDocsReadTheDocs(){

    if [[ "${*}" =~ "-sudo" ]] ; then local sudo="sudo" ; else local sudo=""; fi

    #Install Mkdocs and Themes
    #sudo pip3 install mkdocs==1.1.2
    ${sudo} pip3 install mkdocs

    #Install Mkdocs Themes
    #https://github.com/cjsheets/mkdocs-rtd-dropdown
    ${sudo} pip3 install mkdocs-rtd-dropdown

    #https://pypi.org/project/mkdocs-macros-plugin/
    ${sudo} pip3 install mkdocs-macros-plugin

    #mkdocs-material
    #https://github.com/squidfunk/mkdocs-material
    ${sudo} pip3 install mkdocs-material

    #Extra
    #[mkdocs-windmill](https://github.com/gristlabs/mkdocs-windmill)
    #${sudo} pip3 install mkdocs-windmill

    #[mkdocs-bootstrap](https://mkdocs.github.io/mkdocs-bootstrap/)
    #${sudo} pip3 install mkdocs-bootstrap

    #[mkdocs-bootswatch](https://github.com/mkdocs/mkdocs-bootswatch)
    #${sudo} pip3 install mkdocs-bootswatch

    #[mkdocs-psinder](https://michaeltlombardi.github.io/mkdocs-psinder)
    #${sudo} pip3 install mkdocs-psinder

    #[mkdocs-bootstrap4](https://github.com/byrnereese/mkdocs-bootstrap4)
    #${sudo} pip3 install mkdocs-bootstrap4

    #[GitBook Theme](https://gitlab.com/lramage/mkdocs-gitbook-theme)
    #${sudo} pip3 install mkdocs-gitbook
}

###############################################################################
# @description Backup all /cipherdmg-trading package
# @noargs
# @internal
#
backupCipherScripts(){ datestamp; backupDevProject "${CIPHERDMG_HOME}"; }

###############################################################################
# @description Backup /cipherdmg-trading from GitHub
# @arg $1 string v{Version Tab} i.e v1.0.0
#
backupCipherScriptsFromGithub(){ backupProjectFromGithub "git@github.ibm.com:cipherdmg/cipherdmg-trading.git" "${CIPHERDMG_HOME}" "${@}"; }

###############################################################################
# @description Build Trading Docs
#
# @internal
#
buildDocsTrading(){

    local local_project="/dev-projects/cipherdmg-trading"
    local docs_dir="${local_project}/docs-template"
    if [[ -d "${docs_dir}/site" ]] ; then rm -rf "${docs_dir}/site"; fi

    cd "${docs_dir}"
    mkdocs build

    if [[ -d "${local_project}/docs" ]] ; then rm -rf "${local_project}/docs"; fi

    #Copy the docs
    cp -rf "${docs_dir}/site" "${local_project}/docs"
}

