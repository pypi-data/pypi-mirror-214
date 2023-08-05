from pydantic import validate_arguments
from typing import Optional
import httpx

from .utils.product_url import extract_shop_id_and_product_id_from_url
from .settings import DEFAULT_ORIGIN_URL

class Shopee:
    @validate_arguments
    def __init__(
        self,
        origin_url = DEFAULT_ORIGIN_URL
    ) -> None:
        self._origin_url = origin_url

    @validate_arguments
    def fetch_product(
        self,
        *,
        url: Optional[str] = None,
        id: Optional[str] = None,
        shop_id: Optional[str] = None
    ) -> dict:
        if (
            url is None and
            id is None and
            shop_id is None
        ):
            raise Exception("You must at least pass the URL of the product or its id and the shop!")

        if url is None:
            if id is None or shop_id is None:
                raise Exception("You must at least pass the URL of the product or its id and the shop!")

        else:
            shop_id_and_product_id = extract_shop_id_and_product_id_from_url(url)
            shop_id = shop_id_and_product_id["shop_id"]
            id = shop_id_and_product_id["product_id"]

        url = f"{self._origin_url}/api/v4/item/get"

        params = {
            "shopid": shop_id,
            "itemid": id
        }

        response = httpx.get(
            url = url,
            params = params
        )

        data = response.json()

        return data