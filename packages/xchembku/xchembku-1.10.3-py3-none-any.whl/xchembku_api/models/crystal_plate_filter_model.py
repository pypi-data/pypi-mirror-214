from typing import Optional

from pydantic import BaseModel


class CrystalPlateFilterModel(BaseModel):
    """
    Model containing crystal plate query filter.
    """

    uuid: Optional[str] = None
    visit: Optional[str] = None
    barcode: Optional[str] = None
    include_errors: Optional[bool] = None
    limit: Optional[int] = None
    direction: Optional[int] = None

    # Allow searching starting from a particular plate id.
    from_formulatrix__plate__id: Optional[int] = None

    # These choices are only used in the report query.
    needing_intervention: Optional[bool] = None
