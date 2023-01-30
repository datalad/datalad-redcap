User guide
==========

REDCap API
----------

This extension uses REDCap's API (application programming interface)
to communicate with the REDCap server. The ability to use the API
depends on REDCap user permissions, which can be granted by the REDCap
instance administrator.

To use the extension, you must have API Export privileges in the
project. Additional permissions, such as "De-Identified", "Remove All
Identifier Fields", or "Full Data Set", can determine the scope of
your access. User permissions can be granted by the REDCap instance
administrator.

To use the extension, you need an API token, which will be used to
authenticate all requests sent to the REDCap server. You will find it
in the Applications / API page in REDCap's project menu. You may have
to request the token first. The token is user-specific and valid for a
specific project.

Consult the Help & FAQ section of your REDCap portal for details.

Usage example
-------------

In the example below we will demonstrate exporting data from a single
form.

The extension operates in existing DataLad datasets. We start this
example by creating an empty dataset::
  
  datalad create my-project
  cd my-project

Let's assume the form from which we want to export responses is called
"abcd" (note: if your form name contains spaces, you need to replace
them with underscores), and we want to save the export in a file named
``abcd.csv``::

  datalad export-redcap-form https://example.redcap.com/api/ abcd abcd.csv

If this is the first time you connect to this REDCap instance, you
will be prompted for your API token (see Credentials section
below). DataLad will then retrieve the form data, write them to the
specified file, and save the change in the dataset.

Any time you need to update your dataset, you can repeat the export
command::

  datalad export-redcap-form https://example.redcap.com/api/ abcd abcd.csv

This will create a new commit if the exported data differs from your
local copy (local content will be overwritten). If there are no
changes, no new commit will be created. The file to which exported
data are written must be in "clean" state, i.e., not have any changes
that weren't saved in version control.

If you don't know the form name upfront, want to find out which forms
are available, or what exactly REDCap recognizes as a form name, you
can use the ``redcap-query`` command::

  datalad redcap-query https://example.redcap.com/api/

The ``export-redcap-form`` command supports several additional
options. For example, you can export several forms into a single file,
choose not to include the survey identifier and timestamp columns, or
skip the saving step if you want to do ``datalad save`` yourself,
later. To see the list of available options, you can use the
``--help`` parameter, just like for any other DataLad command::

  datalad export-redcap-form --help

Note on git-annex
-----------------

In the example above we created a new dataset with a default
configuration, which means all files will be annexed (i.e. magaged by
git-annex). Whether or not that is the desired behaviour (an
alternative would be to track the files with Git) is ultimately up to
you to decide.

Keep in mind that when it comes to creating dataset siblings, annexed
files can be `shared separately
<http://handbook.datalad.org/en/latest/basics/101-138-sharethirdparty.html#dataset-contents-and-third-party-services-influence-sharing>`_
from the Git part of the dataset. And if you store annexed contents in
remote hosting, you may also be interested in `git-annex encryption
<https://git-annex.branchable.com/encryption/>`_ options.

You can control which files are annexed *vs* tracked with Git using
the ``annex.largefiles`` configuration option in the
``.gitattributes`` file.

Credentials
-----------

DataLad will store or retrieve your API token using your operating
system's keyring service.

In general, the first time you connect to the REDCap server, you will
be prompted for the token. If data retrieval succeeds, you will also
be prompted to save and name the credential (with ``redcap-<api url>``
being the default).

When you connect to the same REDCap instance again, DataLad will use,
by default, the last credential successfuly used for that API URL.

If you have access to multiple projects on the same instance, you can
create differently named credentials and use the ``--credential``
parameter, supported by all commands used to communicate with REDCap.

You can use the `datalad credentials
<http://docs.datalad.org/projects/next/en/latest/generated/man/datalad-credentials.html>`_
command from DataLad Next extension (which is installed as a
dependency for the REDCap extension) to manage (e.g. query, set or
remove) credentials known to DataLad.
