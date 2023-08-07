httpie-http-message-signatures
==============================

An authentication plugin for [HTTPie][1], implementing the [IETF HTTP Message Signatures][2] draft specification.

This is an incompatible replacement for and not to be confused with the ["Cavage" HTTP Signatures][3] draft.

Installation
------------

The preferred installation method is via the [`httpie cli plugins` utility][4]:

    $ httpie cli plugins install httpie-http-message-signatures

You may also download this repository and install from a local source:

    $ cd httpie-http-message-signatures
    $ httpie cli plugins install .

Last but not least, you can install via `pip` as well:

    $ pip install --upgrade httpie-http-message-signatures

Usage
-----

Use `message-signature` as the auth-type:

    http -A message-signature ...

The HTTP Message Signature draft allows for a whole bunch of parameters to influence the signature. Because this can
get somewhat overwhelming quickly, this plugin allows the parameters to be passed in two different ways:

1. `-a`/`--auth` command line parameter

   This allows passing arguments inline, in the following format:

       key_id ":" key [":" covered_component_ids]

   In other words, the key id, followed by a `:`, followed by the private key as base 64 encoded string, *optionally*
   followed by another `:` and a list of comma-separated covered component ids. For example:

       $ http -A message-signature -a foobar:cDf/J30Q7EtXmZZ91j4OLg== example.com
       $ http -A message-signature -a foobar:cDf/J30Q7EtXmZZ91j4OLg==:@authority,@method example.com

2. `~/.httpmessagesignaturesrc` file

   If no parameters are passed via `-a`/`--auth`, the plugin will look for a file called `.httpmessagesignaturesrc`
   in the home directory. This file is a simple [INI-like file format][5], which contains sections for different hosts,
   each with their own settings. A `[DEFAULT]` section can be used to set defaults for all hosts. For example:

       [DEFAULT]
       covered_component_ids = @method,@authority,@target-uri,content-digest

       [example.com]
       key_id = foobar
       key = cDf/J30Q7EtXmZZ91j4OLg==

       [*.example.com]
       key_id = uydnfpw0xnegmpx2op3rhw2qm
       key = nkAFfoSEN/rXWu6PrqsmntUeeSZ+aEoGD9YmxIxwjNxdlHPO4QYcSS+4aRroRHl92vEEipRCsr+j2tFVlPimfA==
       covered_component_ids = @method,@authority,@path,@query-params,content-digest

   Host names allow for wildcard patterns.

### Covered component ids

Different parts of the HTTP request can be included in the signature. By default, these components are included:

- `@method`
- `@authority`
- `@target-uri`

You can override this default list via the optional third command line argument or the `covered_component_ids` value
in the `~/.httpmessagesignaturesrc` file. The plugin recognizes two special component ids:

1. `content-digest`

   When specifying `content-digest` as a covered component, and the request has a request body, the plugin will add a
   `Content-Digest` header to the request and include it in the signature. This allows easy signing of request bodies.

2. `@query-params`

   The default `@target-uri` component signs the entire URI, including query parameters. Depending on your use case, 
   you may need to sign the request path and query parameters separately. For this case the specification requires 
   for every signed query parameter to be listed separately as its own component. E.g. a request to
   `http://example.com/foo/?bar=baz&quux=42` would have to look like this:

       $ http -A message-signature \
              -a 'foobar:cDf/J30Q7EtXmZZ91j4OLg==:"@query-params";name="bar","@query-params";name="quux"' \
              example.com bar==baz quux==42

   Since this is of course highly inconvenient, the special component id `@query-params` will automatically be expanded
   to include all passed query parameters. So the above request can be shortened to:

       $ http -A message-signature -a foobar:cDf/J30Q7EtXmZZ91j4OLg==:@query-params example.com bar==baz quux==42

See the specification for a [complete list of derived component names][6], but an incomplete list is presented here:

- `@method`
- `@target-uri`
- `@authority`
- `@scheme`
- `@request-target`
- `@path`
- `@query`
- `@query-param`

Implementation
--------------

This plugin is a wrapper around [http-message-signatures][7].


  [1]: https://httpie.io
  [2]: https://datatracker.ietf.org/doc/draft-ietf-httpbis-message-signatures/
  [3]: https://datatracker.ietf.org/doc/draft-cavage-http-signatures/
  [4]: https://httpie.io/docs/cli/httpie-cli-plugins-install
  [5]: https://docs.python.org/3/library/configparser.html
  [6]: https://www.ietf.org/archive/id/draft-ietf-httpbis-message-signatures-17.html#name-derived-components
  [7]: https://pypi.org/project/http-message-signatures/