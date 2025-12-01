from functools import partial

from fastapi import Depends, Request

from drivers.helpers.hetoas import ListingParams, create_hateoas_response


def hateoas_dependency(request: Request, listing_params: ListingParams = Depends()):
    return partial(
        create_hateoas_response, request=request, listing_params=listing_params
    )
