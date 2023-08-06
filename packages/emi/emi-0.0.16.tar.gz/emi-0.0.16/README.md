# Eons Modular Interface

Use the Eons Modular Interface (EMI) to configure systems.

EMI is a state manager that uses the [Eons python library](https://github.com/Eons-dev/lib_eons) by executing arbitrary actions which are provided by the repository (per Eons).  
The default repository is https://infrastructure.tech.

This means `emi install a_package` will execute the "install" action and provide it with the arguments "a_package".

Basically, we're iterating on the tried-and-true universal install script:  
[<img src="https://imgs.xkcd.com/comics/universal_install_script.png">](https://xkcd.com/1654/)

## Installation
`pip install emi`

## Usage

Emi is a state manager; it establishes reproducibility. This means that if emi reports that 2 systems are identical (and has not been subverted), those 2 systems will behave the same. 

Use emi to change the state of a system. This change will be recorded for later comparison. This is similar to your bash history: you'll be able to look through what you did and replicate that work later on or on another machine.

Emi should behave as a typical package manager: you can `install`, `update` and `remove` packages. Plus, a whole lot more ;)

Emi uses the current user's home directory to store configuration and data relating to operations (e.g. what packages at what versions have been installed where).

Because emi is built on Eons, the actions you request do not have to be installed prior: anything not found in your home directory will be automatically downloaded for you.

### Verbiage

Emi makes use of 2 metaphors: commerce for actions and library science for data.

**Merx**  
Actions intended for use with emi will be labeled as "Merx". This derives from latin: "emi Merx" is roughly "I bought the goods", Merx being goods or wares. In this case any "goods" available for "purchase" may be "bought" (e.g. downloaded; there is no exchange of currency in emi, only information) by emi.

A Merx may be invoked through its `Transaction()` method, which is called by its `Function()` (per `Eons.Functor`; meaning `Merx()` calls `Merx.Transaction()`). `Transaction()` is what you'll want to override when creating your own Merx.

NOTE: you'll also want to override the `Merx.Rollback()` method for when things go wrong.

**Tomes**  
Packages intended for use in Merx are called "Tomes", i.e. semantically heavy symbols. "heavy" here alludes to the fact that Tomes and what they act upon may contain multiple libraries. However, each Tome, be it a library itself, a set of binaries, or even just a simple environment variable, is still referenced by emi as a single symbol (i.e. name).

A Tome on the default repository will typically be a zip containing directories like "bin", "inc", "lib", etc. It is up to the package maintainer to adhere to these standards or to be consistent in their own (e.g. for use with their own Merx). Each maintainer is likewise responsible for ensuring their Tome's cross-platform viability and documentation.

To restate the above, `emi install a_package`, when using the default install script and repo through Eons, will generate 2 requests:
1. `merx_install` will be downloaded and placed in `~/.eons/merx/install.py`.
2. `tome_a_package` will be downloaded to `~/.eons/tmp/a_package/` and used as an arg in the `install.py` `Merx.Transaction()`.

[EBBS](https://github.com/Eons-dev/bin_ebbs) is used to build Tomes; EMI is used to install them. Actions intended for use in ebbs are called "Builders"; actions intended for use in EMI are called Merx.

Merx, as a noun, rather than the typical verb (the same as "installation" vs "install", "removal" vs "remove", etc.) can be rationalized as a requested change. For example, the emi analogy follows that a merchant would "sell you a change" in your system, provided that you give them the knowledge of how to do that (i.e. the Tomes). This is like asking a contractor to build a new room onto your <span style="color:blue">house</span>, only the contractor would need to know the blueprint for the room ahead of time and have all the materials accessible.

### Arguments

`emi merx1/merx2 tome1 tome2 tome3 --extra args`

Emi allows for args to be used in multiple ways. You can supply as many Tomes as you would like (including none); you can also supply extra arguments as provided by Eons (e.g. `--extra-arg value`).

Everything beyond the Merx (first arg), which is not preceded by '--', is made available to the Merx as a Tome. However, once '--' is found, all remaining arguments are interpreted as key-value pairs that are available in the `executor.extraArgs` and thus can be `Fetch()`ed. This behavior is identical to EBBS and other Eons implementations except that the Merx and Tomes come before any extra arguments.

It is up to the Merx to decide what to do with the Tomes it is given. Usually, multiple args past the 2nd (and before extra args) equate to multiple packages to install, remove, etc. but that is only convention and in now way required. A Merx could interpret a series of Tomes as a series of actions to execute in sequence or anything else it would like.

It is always preferred to have many different, interacting Merx than to have a single Merx with many options (i.e. modules are preferred over monoliths). For example, `apt install -y` in proper emi style would be rewritten as `apt auto-install` or, even better `apt auto/install`. Eons makes it possible to execute Functors in sequence. Emi uses this system to evaluate a series of Merx that you can specify by separating each with a '/'. Emi only takes a single "merx" argument, but you can use that to execute as many Merx as you'd like. For example, we could have `emi install ...`, `emi auto/install ...`, or even `emi selective/auto/install ...`. This relies on the Eons sequence mechanics to enable `auto` to change the behavior of `install`, `selective` to change the behavior of both `auto` and `install`, etc. You can pass both members (variables) and methods (functions) this way; thus, your Merx can be as modular as your heart desires! Of course, you can also choose to use extra arguments to augment your Merx; `emi install ... --auto true` is just as valid.

The only difference between `auto/install` and `install ... --auto true` (besides the latter being longer to type) is extensibility. When using `install ... --auto true`, the `auto` keyword should exist as an `optionalKWArg` in some base class of `install`, and your other Merx should inherit from that base class as well. Using a common base class helps create consistency. On the other hand, `auto/install` uses [the Eons Implicit Inheritance system](https://github.com/eons-dev/lib_eons#implicit-inheritance) to endow `install` with functionality from `auto`. This means that, if you design your classes to properly use Implicit Inheritance, you don't have to create consistency by managing inheritance (or multiple inheritance) yourself, nor would you have to refactor your code to add features from a third party Merx. Instead, you'd just have to start typing that third party Merx before yours and off you'd go! Ultimately, Implicit Inheritance is Ra tool to make your life and the life of your users easier. If you find this system to be confusing or cumbersome, just add `____KWArgs` to your Merx and have your users supply additional cli arguments.

### Directories

Emi will attempt to use the best directory for the current user by first testing access to common system directories (i.e. check for admin privileges). If a Tome can be written to a system directory for use by all users, it will be. Otherwise, the Tome will be written to `~/.eons/`. This behavior can be overwritten by specifying `..._path` in the config (see below), where `...` is whichever path you'd like to override (e.g. `bin_path`, `inc_path`, `lib_path`, etc.).

All other data, including the config file and database are stored in `~/.eons/`.

**WINDOWS USERS**: You must set all `..._paths` in your config.json or rely only on local user installations (i.e. in the `~/.Eons/` folder). Automatic support for system path discovery on Windows may be added in a future release.

#### Merx

All Merx are placed in `~/.eons/merx`. These are saved indefinitely.
You can also create your own Merx in that directory, and they will be automatically usable by emi. The `~/.Eons/merx` directory is the `eons.Executor.repo.store`, i.e. where the self-registering functors for emi (the Merx) are kept.

#### Tomes

Tomes are downloaded to `~/.eons/tmp`. Currently, these are saved indefinitely but that will be changed in a future release. The idea is that a Merx should move the contents of the Tome to the appropriate location in the filesystem and record that location in the database (see below).

### Configuration

Emi uses the default config file `~/.eons/config.json`. While this can be overridden, it is much preferred to leave it as is.

This configuration file is used for all `eons.Executor.Fetch()` calls, which means any Merx that `Fetch()`s a value can find it in this config.

### Database

Emi uses a [SQLite](https://www.sqlite.org/index.html) database to keep track of all Merx transaction and the locations of all Tomes. 

This database is stored in `~/.eons/catalog.db`.

All columns which can have multiple entries will be semicolon delimited.

#### Tomes

A record of all Tomes is kept in the `tomes` table:  
Name | Data Type | Not NULL |
:--- | :-------- | :------: |
id | INTEGER | true |
name | VARCHAR | false |
version | VARCHAR | false |
installed_at | VARCHAR | false |
retrieved_from | VARCHAR | false |
first_retrieved_on | FLOAT | false |
last_retrieved_on | FLOAT | false |
additional_notes | VARCHAR | false |

#### Transactions

Everytime emi is invoked, it will record the Transaction it executes.
These data are stored in the `transactions` table:  
Name | Data Type | Not NULL |
:--- | :-------- | :------: |
id | INTEGER | true |
when | FLOAT | false |
merx | VARCHAR | false |
tomes | VARCHAR | false |
result | INTEGER | false |

### Repository

Online repository settings can be specified with:
```
--repo-store (default = ./eons/)
--repo-url (default = https://api.infrastructure.tech/v1/package)
--repo-username
--repo-password
```

Keep in mind that `emi --repo-store ... merx1/merx2 tomes` on the command line is equivalent to having `"repo_store": "..."` in the ~/.eons/config.json and calling `emi merx1/merx2 tomes`.
Please don't store your credentials in the config.

NOTE: you do not need to supply any repo settings to download packages from the public repository.
For more info on the repo integration, see [the Eons library](https://github.com/Eons-dev/lib_eons#online-repository)
