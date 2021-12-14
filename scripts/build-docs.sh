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
#[REQUIRED]

#[SOURCE]

#--------------------------- Environment Variables ---------------------------#
#[REQUIRED]


#[DEFAULTS]


#[CONSTANTS]

#-------------------------------- Alias Values -------------------------------#

#--------------------------------- Sourcing ----------------------------------#
#[SOURCE]

#[ALL_VARIABLES_ARRAY]

#============================= Script Functions ==============================#


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

