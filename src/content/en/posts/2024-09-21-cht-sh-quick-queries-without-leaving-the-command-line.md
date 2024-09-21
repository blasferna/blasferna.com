---
title: cht.sh: Quick Queries Without Leaving the Command Line
slug: cht-sh-quick-queries-without-leaving-the-command-line
date: 2024-09-21
summary: Discover cht.sh, a tool that allows you to quickly obtain information about Linux commands and programming modules directly from your terminal.
language: en
topic: linux
---

## Introduction

Many times when we are working on a server without a graphical interface and need additional information about a command we are going to execute, for example: copying or moving a file, compressing, downloading from the internet, etc.

We could turn to Google or directly ask ChatGPT, right? Yes, but that would mean minimizing the terminal if we're connected via [SSH](https://en.wikipedia.org/wiki/Secure_Shell) and opening the browser, or it simply wouldn't be possible if we're in front of the server.

Today I bring you a resource that will allow us to obtain a cheat sheet in a practical way directly from the terminal.

The resource is [`cht.sh`](http://cht.sh/), which is simply a set of pages that return text formatted for terminals and is used in combination with [`curl`](https://en.wikipedia.org/wiki/CURL).

## Requirements

- We'll need the server to have internet access.
- Know the command to use.
- Have [curl](https://en.wikipedia.org/wiki/CURL) installed, which comes pre-installed on most Linux systems and lately in the latest versions of Windows.

## Usage

To use [`cht.sh`](http://cht.sh/), we simply need to make a request with the name of the command or tool we want to get more information about, and we'll immediately receive a quick guide with examples.

```bash
curl cht.sh/[replace with the desired command or tool]

```

In the following example, we'll see how to get a quick guide for the `mv` command:

```bash
curl cht.sh/mv

```

This will show us a concise list of the most common options and usage examples for the `mv` command:

```bash
$  curl cheat.sh/mv
 cheat:mv
# To move a file from one place to another:
mv <src> <dest>

# To move a file from one place to another and automatically overwrite if the destination file exists:
# (This will override any previous -i or -n args)
mv -f <src> <dest>

# To move a file from one place to another but ask before overwriting an existing file:
# (This will override any previous -f or -n args)
mv -i <src> <dest>

# To move a file from one place to another but never overwrite anything:
# (This will override any previous -f or -i args)
mv -n <src> <dest>

# To move listed file(s) to a directory
mv -t <dest> <file>...

 tldr:mv
# mv
# Move or rename files and directories.
# More information: <https://www.gnu.org/software/coreutils/mv>.

# Rename a file or directory when the target is not an existing directory:
mv source target

# Move a file or directory into an existing directory:
mv source existing_directory

# Move multiple files into an existing directory, keeping the filenames unchanged:
mv source1 source2 source3 existing_directory

# Do not prompt for confirmation before overwriting existing files:
mv -f source target

# Prompt for confirmation before overwriting existing files, regardless of file permissions:
mv -i source target

# Do not overwrite existing files at the target:
mv -n source target

# Move files in verbose mode, showing files after they are moved:
mv -v source target

$

```

The information it provides is more than enough to complete the operation safely.

In addition to obtaining more information about some Linux commands, [cht.sh](http://cht.sh/) also offers the possibility of accessing documentation for programming language modules, for example:

```bash
curl cht.sh/python/requests

```

This gives us a basic guide on how we can use the `requests` module in Python.

```bash
#  [Since v1.2.3](https://2.python-
#  requests.org/en/master/api/requests.PreparedRequest) Requests added
#  the PreparedRequest object. As per the documentation "it contains the
#  exact bytes that will be sent to the server".
#
#  One can use this to pretty print a request, like so:

 import requests

 req = requests.Request('POST','<http://stackoverflow.com>',headers={'X-Custom':'Test'},data='a=1&b=2')
 prepared = req.prepare()

 def pretty_print_POST(req):
     """
     At this point it is completely built and ready
     to be fired; it is "prepared".

     However pay attention at the formatting used in
     this function because it is programmed to be pretty
     printed and may differ from the actual request.
     """
     print('{}\\n{}\\r\\n{}\\r\\n\\r\\n{}'.format(
         '-----------START-----------',
         req.method + ' ' + req.url,
         '\\r\\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
         req.body,
     ))

 pretty_print_POST(prepared)

#  which produces:

 -----------START-----------
 POST <http://stackoverflow.com/>
 Content-Length: 7
 X-Custom: Test

 a=1&b=2

#  Then you can send the actual request with this:

 s = requests.Session()
 s.send(prepared)

#  These links are to the latest documentation available, so they might
#  change in content:
#  [Advanced - Prepared requests](https://2.python-
#  requests.org/en/master/user/advanced/id3) and [API - Lower level
#  classes](<https://2.python-requests.org/en/master/api/lower-level->
#  classes)
#
#  [AntonioHerraizS] [so/q/20658572] [cc by-sa 3.0]

```

## Conclusion

[cht.sh](http://cht.sh/) is an interesting resource for system administrators and developers who frequently work in command-line environments. It provides quick and convenient access to crucial information about Linux commands as well as programming modules, without the need to leave the terminal. This efficiency not only saves time but also improves productivity by allowing users to obtain the information they need without interrupting their workflow.