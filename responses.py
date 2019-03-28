import copy
import simplejson as json

from flask import Response, current_app, render_template, g, \
    escape, request


def jsonapi_wrapper(
        content,
        mimetype='application/vnd.api+json',
        headers=None,
        status=200
        ):
    if headers is None:
        headers = g.resp["headers"]
    return Response(
        content,
        mimetype=mimetype,
        headers=headers,
        status=status
    )


def jsonapi_unauthorised(detail, source=None, code=None, docs=''):
    return Response(
        render_template(
            'jsonapi-401.json',
            detail=detail,
            source=source,
            code=code,
            docs=current_app.config['API_DOCS_ROOT'] + 'v' +
            current_app.config['API_DOCS_VERSION'] + '/' + docs
        ),
        mimetype='application/vnd.api+json',
        headers=g.resp["headers"],
        status=401
    )


def jsonapi_internal_error(e):
    # TODO: add logging
    print("\n\nInternal error")
    print(e)
    return jsonapi_wrapper(
        render_template(
            'jsonapi-500.json',
            detail="An Internal Error has occured. Sorry about that.",
            source=escape(request.url)
        ),
        status=500
    )
    

def jsonapi_errors_constructor(
        detail,
        manual_doc,
        manual_code,
        status=400,
        source=None
        ):
    err_messages = {
        'errors': []
    }
    err_messages['errors'].append(
        {
            'detail': detail,
            
        }
    )
    return jsonapi_errors(
            err_messages=err_messages,
            status=status,
            manual_doc=manual_doc,
            manual_code=manual_code
    )

def jsonapi_errors(
        err_messages,       # The error exception from marshmallow
        status=400,         # http status code to return
        manual_code=None,   # For a single error e.g. IncorrectTypeError,
                            # the code number to be addeded
        manual_doc=None     # For a single error e.g. IncorrectTypeError,
                            # the docs path (minus the API_DOCS_ROOT which is
                            # added by this function)
        ):
    msg = copy.deepcopy(err_messages)
    if len(msg['errors']) is 1:
        if manual_code:
            msg['errors'][0].update({'code': manual_code})
        if manual_doc:
            msg['errors'][0].update(
                {
                    'links': {
                        'self': current_app.config['API_DOCS_ROOT'] +
                        'v' + current_app.config['API_DOCS_VERSION'] + '/' +
                        manual_doc
                    }
                }
            )

    for i in range(len(msg['errors'])):
        parts = msg['errors'][i]['detail'].split(':#:')
        if len(parts) is 3:
            parts = msg['errors'][i].update(
                {
                    'detail': parts[0],
                    'code': parts[1],
                    'links': {
                        'self': current_app.config['API_DOCS_ROOT'] +
                        'v' + current_app.config['API_DOCS_VERSION'] + '/' +
                        parts[2]
                    }
                }
            )

    return jsonapi_wrapper(
        json.dumps(
          msg,
          sort_keys=True,
          indent=4
        ),
        status=status
    )
