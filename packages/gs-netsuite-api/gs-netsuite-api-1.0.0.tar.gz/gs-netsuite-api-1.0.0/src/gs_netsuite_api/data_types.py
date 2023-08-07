import dataclasses
import datetime
from typing import List


__all__ = [
    "RecordRef",
    "ProductData",
    "ProductAvailability",
    "PurchaseOrderData",
    "PurchaseOrderLineData",
    "SaleOrderData",
    "SaleOrderLineData",
    "ItemPicking",
    "ItemMove",
]


@dataclasses.dataclass
class RecordRef:
    internalId: int
    name: str

    @staticmethod
    def from_rec_named(record) -> "RecordRef":
        return RecordRef(internalId=record.internalId, name=record.name)


@dataclasses.dataclass
class ProductData(RecordRef):
    """
    Classe contenant les champs "Catalogue" du fichier excel
    """

    ean13: str
    hs_code: str
    price_ttc: float
    categories: List[RecordRef]
    ref: str
    url_site: str
    qty_available: float
    next_arrival_date: datetime.datetime
    create_date: datetime.datetime
    last_write_date: datetime.datetime
    images: str
    availabilities: List["ProductAvailability"] = dataclasses.field(default_factory=list, repr=True)


@dataclasses.dataclass
class ProductAvailability:
    product: RecordRef
    location: RecordRef
    last_change_date: datetime.datetime
    quantity_on_hand: float
    quantity_on_order: float
    quantity_committed: float
    quantity_back_ordered: float
    quantity_available: float


@dataclasses.dataclass
class PurchaseOrderLineData(RecordRef):
    """
    FROM : transactions/purchases.xsd
    COMPLEXE_TYPE:
    """

    product: RecordRef
    expected_receipt_date: datetime.datetime
    amount_tax_excluded: float
    amount_tax: float
    amount_tax_included: float
    order_qty: float
    recieved_qty: float
    billed_qty: float
    closed: bool


@dataclasses.dataclass
class PurchaseOrderData(RecordRef):
    """
    Classe contenant les champs de vente
    """

    currency: RecordRef
    supplier: RecordRef
    employee: RecordRef
    total_tax_excluded: float
    total_tax: float
    total_tax_included: float
    order_date: datetime.datetime
    state: str
    lines: List[PurchaseOrderLineData] = dataclasses.field(default_factory=list, repr=True)


@dataclasses.dataclass
class SaleOrderLineData(RecordRef):
    product: RecordRef
    amount_tax_excluded: float
    amount_tax: float
    tax_rate: float
    amount_tax_included: float
    order_qty: float
    billed_qty: float
    backordered_qty: float
    committed_qty: float
    available_qty: float
    on_hand_qty: float
    closed: bool


@dataclasses.dataclass
class SaleOrderData(RecordRef):
    """
    Classe contenant les champs de vente
    """

    currency: RecordRef
    supplier: RecordRef
    total_tax_excluded: float
    total_tax: float
    total_tax_included: float
    order_date: datetime.datetime
    state: str
    discount_amount: float
    shipping_cost: float
    is_quote: bool
    lines: List[SaleOrderLineData] = dataclasses.field(default_factory=list, repr=True)


@dataclasses.dataclass
class ItemMove(RecordRef):
    """
    Class convertit depuis
    purchase.xsd ItemReceiptItem
    contenant aussi les champs de Record defini dans core.xsd
    """

    product: RecordRef
    location: RecordRef
    quantity: float
    quantity_remaining: float


@dataclasses.dataclass
class ItemPicking(RecordRef):
    """
    Class convertit depuis
    purchase.xsd ItemReceipt

    contient des line depuis itemList.item -> ItemReceiptItem
    """

    create_date: datetime.datetime
    last_write_date: datetime.datetime
    date_done: datetime.datetime
    origin: RecordRef
    lines: List[ItemMove] = dataclasses.field(default_factory=list, repr=True)


@dataclasses.dataclass
class InventoryAdjustment(RecordRef):
    create_date: datetime.datetime
    last_write_date: datetime.datetime
    date_done: datetime.datetime
    location: RecordRef
    adj_location: RecordRef
    lines: List["InventoryAdjustmentLine"] = dataclasses.field(default_factory=list, repr=True)


@dataclasses.dataclass
class InventoryAdjustmentLine(RecordRef):
    product: RecordRef
    units: RecordRef
    quantity_on_hand: float
    current_value: float
    adjust_qty_by: float
    new_quantity: float
    inventory_detail: str
