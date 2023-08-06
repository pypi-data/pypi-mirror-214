from __future__ import annotations
from datetime import datetime
from typing import List, Dict, Union
from .utils import *

from repleno.order import Order
from repleno.item import Item
from repleno.item import ItemType
from repleno.order import OrderType

import warnings


# future improvements
# todo: get collaterals by getting the tree, and if list is needed, traverse it (do it while keeping in mind performance)
# todo: in factory, develop mrp that is focused on obsoletion, covering the 3 scenarios (scrap everything, produce and scrap, produce everything)
# todo: method for flushing any general label from root to child nodes.

# todo: when parameters are being loaded and column is not perfectly what's in the file, no warning is issue! Or if column is not found.
# todo: R: if one component goes out of stock, what's the impact on the finished goods in units?
# todo: during MRP, if an order is issued to a specific item and the long time of this item is longer than the sales lead time, issue a warning (?)
# todo: add average sales as property to the item class and flush down a category (VS and sub-VS)
# todo: consider the different UoM's
# todo: per component, shows how much of its demand impact finished goods. If 1 component goes into only 1 FG, then 100%
# todo: allow user to specify date formatting


class Factory:
    def __init__(self, bill_of_materials=None, parameters=None, mps=None):
        self._items = {}

        if bill_of_materials:
            self.load_bill_of_materials(bill_of_materials)

        if parameters:
            self.load_parameters(parameters)

        self._mps = []
        if mps:
            self.load_mps(mps)

        self._cache = {}  # don't use @lru_cache because of memory leak

    @property
    def items_mapping(self):
        return self._items

    @property
    def items(self):
        output_list = [item[1] for item in self._items.items()]

        return output_list

    @property
    def item_codes(self):
        output_list = [item[0] for item in self._items.items()]

        return output_list

    @property
    def mps(self):
        return self._format_order_list_for_output(self._mps)

    def get_item(self, code):
        code_fmt = str(code).strip().upper().lstrip("0")

        return self._items.get(code_fmt, None)

    def _get_item_or_create(self, value: Union[str, Item]) -> Item:
        """Helper method to get an Item from a string or create it"""

        if isinstance(value, str):
            item = self.get_item(value)
            if item is None:
                return Item(value)
            else:
                return item

        if isinstance(value, Item):
            return value

        raise TypeError("item argument must be a string or an Item instance.")

    # TODO: change code so everything becomes at the SKU level, not item level
    def add_parent_child_relationship(
        self,
        parent,
        child,
        qty=1,
        parent_location=None,
        child_location=None,
    ):
        # Get/instantiate item objects
        parent_item = self._get_item_or_create(parent)
        child_item = self._get_item_or_create(child)

        # Populate the unit of measures, if any
        if parent_location is not None:
            parent_item.unit_of_measure = parent_location
        if child_location is not None:
            child_item.unit_of_measure = child_location

        # Link the item object to others
        parent_item._add_child(child_item, qty)
        self._register_item_in_factory(parent_item, child_item)

    def _register_item_in_factory(self, parent_item, child_item):
        # Add to factory items dict
        parent_item = self._items.setdefault(parent_item.code, parent_item)
        child_item = self._items.setdefault(child_item.code, child_item)

    def load_bill_of_materials(
        self,
        data: Union[str, List[Dict]],
        mapping: List[Dict[str, str]] = {},
    ):
        mandatory_field_mapping = {
            "parent_code": mapping.get("parent_code", "parent_code"),
            "child_code": mapping.get("child_code", "child_code"),
        }

        optional_field_mapping = {
            "parent_location": mapping.get("parent_location", "parent_location"),
            "child_location": mapping.get("child_location", "child_location"),
            "qty": mapping.get("qty", "qty"),
        }

        # todo: not a good method name - not single responsiblity
        data = select_fields(data, mandatory_field_mapping, optional_field_mapping)

        if isinstance(data, list) and data:
            for i in data:
                parent = i["parent_code"]
                child = i["child_code"]

                # use .get method for optional fields to avoid raising exceptions
                self.add_parent_child_relationship(
                    parent,
                    child,
                    i.get("qty"),
                    i.get("parent_location"),
                    i.get("child_location"),
                )

            return

        raise ValueError(
            "Invalid argument. It must be a csv file path or a list of dictionaries."
        )


    def load_parameters(
        self,
        data,
        field_mapping={},
    ):
        """
        Load parameters into the model.

        Args:
            - data (Union[str, List[Dict]]): The input data, either a csv file
            with the below columns names or a list of dictionary with the below key names:
                1. "item_code"
                2. "inventory_balance": optional
                3. "lead_time": optional
                4. "minimum_order_qty": optional
                5. "batch_qty": optional
                6. "safety_stock_qty": optional
                7. "classification": optional
            In case the data does not have these columns, use the field_mapping
            parameter for mapping.
            - field_mapping (List[Dict[str, str]], optional): When the columns
            in the data are not the default ones. Defaults to an empty dictionary.
            e.g.:
                {
                    "item_code": "<field_name_in_data_with_parent_code>",
                    "lead_time": "leadtime"
                    "safety_stock_qty": "ss"
                }

        Raises:
            ValueError: If the input data is invalid.

        Returns:
            None
        """

        mandatory_field_mapping = {
            "item_code": field_mapping.get("item_code", "item_code"),
        }
        optional_field_mapping = {
            "inventory_balance": field_mapping.get(
                "inventory_balance", "inventory_balance"
            ),
            "lead_time": field_mapping.get("lead_time", "lead_time"),
            "minimum_order_qty": field_mapping.get(
                "minimum_order_qty", "minimum_order_qty"
            ),
            "batch_qty": field_mapping.get("batch_qty", "batch_qty"),
            "safety_stock_qty": field_mapping.get(
                "safety_stock_qty", "safety_stock_qty"
            ),
            "classification": field_mapping.get("classification", "classification"),
        }
        data = select_fields(data, mandatory_field_mapping, optional_field_mapping)

        if isinstance(data, list):
            for dict in data:
                try:
                    item_code = dict.get("item_code")
                    item = self.get_item(item_code)

                    if item is None:
                        warnings.warn(
                            f"'{dict['item_code']}' has no associated BOM.",
                            UserWarning,
                            stacklevel=2,
                        )
                        continue

                    inventory = dict.get("inventory_balance", None)
                    if inventory:
                        item.inventory_balance = inventory

                    lead_time = dict.get("lead_time", None)
                    if lead_time:
                        item.lead_time = lead_time

                    minimum_order_qty = dict.get("minimum_order_qty", None)
                    if minimum_order_qty:
                        item.minimum_order_qty = minimum_order_qty

                    batch_qty = dict.get("batch_qty", None)
                    if batch_qty:
                        item.batch_qty = batch_qty

                    safety_stock = dict.get("safety_stock_qty", None)
                    if safety_stock:
                        item.safety_stock_qty = safety_stock

                    classification = dict.get("classification", None)
                    if classification:
                        item.classification = classification

                except Exception as e:
                    print(f"Item code: '{item_code}' raised the exception: {e}.\n")
                    raise

            return

        raise ValueError(
            "Invalid argument. It must be a csv file path or a list of dictionaries."
        )

    def load_mps(self, data, field_mapping={}, date_format="%Y-%m-%d"):
        """
        Load the master production schedule (MPS) in the model.

        Args:
            - data (Union[str, List[Dict]]): The input data, either a csv file
            with the below columns names or a list of dictionary with the below key names:
                1. "item_code"
                2. "due_date"
                3. "qty"
            In case the data does not have these columns, use the field_mapping
            parameter for mapping.
            - field_mapping (List[Dict[str, str]], optional): When the columns
            in the data are not the default ones. Defaults to an empty dictionary.
            e.g.:
                {
                    "item_code": "<field_name_in_data_with_parent_code>",
                    "due_date": "production_date"
                    "qty": "quantity"
                }

        Raises:
            ValueError: If the input data is invalid.

        Returns:
            None
        """

        mandatory_field_mapping = {
            "item_code": field_mapping.get("item_code", "item_code"),
            "due_date": field_mapping.get("due_date", "due_date"),
            "qty": field_mapping.get("qty", "qty"),
        }
        data = select_fields(data, mandatory_field_mapping)

        if isinstance(data, list):
            for i in data:
                item = self.get_item(i["item_code"])

                if item is None:
                    warnings.warn(
                        f"'{i['item_code']}' has no associated BOM, hence no MRP will be initiated for it.",
                        UserWarning,
                        stacklevel=2,
                    )
                    continue

                try:
                    order = Order(
                        item,
                        datetime.strptime(i["due_date"], date_format),
                        convert_to_float(i["qty"]),
                    )

                    self._mps.append(order)

                except Exception as e:
                    print(f"Item code: '{i['item_code']}' raised the exception: {e}.\n")
                    raise

            return

        raise ValueError(
            "Invalid argument. It must be a csv file path or a list of dictionaries."
        )

    # todo: rename to get material_requirements or something like that
    def run_mrp(self, output=""):
        """Explodes the requirements from the parent nodes to their child nodes
        (lower levels).

        Inventory takes into account the inventory on hand and already released
        orders.

        Parameter must be a dictionary with `key = node_name` and
        `value = qty`.

        >>> production_schedule = {'Bicycle': 10, 'Car': 40}
        >>> tree.explode_requirements(production_schedule)

        Returns:
            dict: returns a dictionary with two lists: purchase orders and work
            orders.

            csv: if output path is given, a csv file is created in that path.

        """
        # check if path exist
        if not self._mps:
            raise ValueError("Empty MPS. Load an MPS into the model to run the MRP.")

        final_orders = []
        for mps_order in self._mps:
            orders = self._compute_child_requirements(mps_order)
            final_orders += orders

        final_orders = self._populate_order_type(final_orders)

        if output:
            data = self._format_order_list_for_csv(final_orders)
            to_csv(data, output)
        else:
            # transform the list of orders into a list of dictionaries

            return self._format_order_list_for_output(final_orders)

    def _format_order_list_for_output(self, orders):
        """
        Transforms a list of orders into a list of dictionaries
        """
        output = []
        for i in orders:
            output.append(
                {
                    "item_code": i.item.code,
                    "due_date": f"{i.due_date:%Y-%m-%d}",
                    "qty": i.qty,
                    "type": i.type.value,
                }
            )

        return output

    def _compute_child_requirements(self, top_order):
        """Breaks down the top level order into dependent orders for individual
        subassemblies, component parts and raw materials that are required to
        produce the top level order.

        >>> ord = Order(Order('20220101', Bicycle, 2)) # 2 Bikes for 01/01/22
        >>> explode_bom(ord)
        Order('20220101', 'Wheel', 4), Order('20220101', 'Frame', '2') ...

        P.S.: function not taking lead times into account yet.

        """
        # How it works?
        # It traverses the tree and for each stock unit iterates over its child
        # stock units. For each child stock unit, calculate the following:
        #
        # Scenarios                                             A   B   C
        # ----------------------------------------------------------------
        # current_inventory                                     2   5   3
        # gross_order                                          -6  -3  -3
        # new_inventory                                        -4   2   0
        # net_order (to replenish inventory)                    4   -   -
        # net_order_rounded (according to lot size)             5   -   -
        # final_inventory (net_order_rounded - gross_order)     1   -   -
        # ----------------------------------------------------------------

        if not isinstance(top_order, Order):
            raise AttributeError("work_orders must be instance of WorkOrder.")

        result = []
        queue = []

        queue.append(top_order)

        # Traverse pre-order
        while len(queue) != 0:
            # Get last order added on the queue and get the net of it
            gross_order = queue.pop()
            net_order = self._get_net_workorder(gross_order)

            # adjust inventories acc. to new order
            item = gross_order.item
            inventory_net_gross_diff = net_order.qty - gross_order.qty
            item.inventory_balance += inventory_net_gross_diff

            if net_order.qty != 0:
                result.append(net_order)

                # adjust the lead time
                gross_order.due_date = remove_business_days(
                    gross_order.due_date, item.lead_time
                )

                # get gross order for child and add it to the queue
                for child_links in item.child_links:
                    gross_req_qty = net_order.qty * child_links.qty

                    queue.append(
                        Order(child_links.item, top_order.due_date, gross_req_qty)
                    )

        return result

    def _get_net_workorder(self, order: Order) -> Order:
        """Subtracts the order qty from the inventory balance for this
        stock unit and if inventory falls below zero returns an order with the
        net requirements lot sized.

        """
        net_quantity = order.qty

        # account for inventory on hand or backorder
        net_quantity -= order.item.inventory_balance

        # account for safety stock
        net_quantity += order.item.get_missing_safety_stock_qty()

        if net_quantity > 0:
            net_qty_rounded = order.item.lot_size(net_quantity)
            return Order(order.item, order.due_date, net_qty_rounded)
        else:
            return Order(order.item, order.due_date, 0)

    def _populate_order_type(self, orders: List[Order]):
        """Populate the type property of Order instances

        Args:
            orders (List[_Order]): list of Order instances
        """
        for order in orders:
            if order.item.type == ItemType.CHILD:
                order.type = OrderType.PURCHASE_ORDER
            else:
                order.type = OrderType.WORK_ORDER

        return orders

    # todo: move this near the properties
    @property
    def abc_classifications(self):
        result = {}
        for item in self.items:
            result[item.code] = item.classification

        return result

    def export_abc_classifications(self, csv_path):
        to_csv(
            self._format_abc_classification_for_csv(self.abc_classifications), csv_path
        )

    def _format_order_list_for_csv(self, data: List[Order]) -> List:
        headers = ["Type", "Due Date", "Item", "Quantity"]
        output = [headers]

        for order in data:
            type = order.type.value
            due_date = f"{order._due_date:%Y-%m-%d}"
            item_code = f"{str(order._item.code)}"
            qty = order._qty

            output.append([type, due_date, item_code, qty])

        return output

    def _format_abc_classification_for_csv(self, data) -> List:
        headers = ["Item", "Classification"]
        output = [headers]

        for item, classification in data.items:
            output.append([item, classification])

        return output

    def _group_and_sort_item_quantities_by_date(self, required_orders, open_orders):
        required_orders_hashed = hash_dicts_list(required_orders)
        open_orders_hashed = hash_dicts_list(open_orders)

        if (required_orders_hashed, open_orders_hashed) in self._cache:
            return self._cache[(required_orders_hashed, open_orders_hashed)]

        # Convert dictionaries of Order objects
        required_orders_fmt = [
            Order(
                Item(o["item_code"]),
                datetime.strptime(o["due_date"], "%Y-%m-%d").date(),
                o["qty"],
            )
            for o in required_orders
        ]
        open_orders_fmt = [
            Order(
                Item(o["item_code"]),
                datetime.strptime(o["due_date"], "%Y-%m-%d").date(),
                o["qty"],
            )
            for o in open_orders
        ]

        # Use a dictionary to keep track of dates and quantities for each item_code.
        # The dictionary has item_code as the key, and its value is a list of all
        # orders (required + open) stored as tuples.
        # Each tuple contains order date and quantity
        quantities = {}

        for order in required_orders_fmt:
            item = order.item.code
            date = order.due_date
            quantity = order.qty * (-1)
            if item not in quantities:
                quantities[item] = []
            quantities[item].append((date, quantity))

        for order in open_orders_fmt:
            item = order.item.code
            date = order.due_date
            quantity = order.qty
            if item not in quantities:
                quantities[item] = []
            quantities[item].append((date, quantity))

        # For each item_code, sort the tuples by date in ascending order
        for item in quantities:
            quantities[item].sort(key=lambda x: x[0])

        self._cache[(required_orders_hashed, open_orders_hashed)] = quantities
        return quantities

    # todo: rename qty to quantity and adjust this as well all over the project
    def get_inventory_over_time(
        self,
        required_orders,
        open_orders,
        item_codes=[],
        shortages_only=False,
        required_orders_field_mapping={},
        open_orders_field_mapping={},
        to_csv_path=None,
    ):
        """
        Calculates the difference in quantities across time for each item_code in the
        required_orders and open_orders lists.

        Args:
            - required_orders (List[Dict[str, any]]): A list of dictionaries
            representing required orders.  Each dictionary contains the
            following keys: 'product', 'date' and 'quantity'.  This is usually
            the return value of the `run_mrp` method.

            - open_orders (List[Dict[str, any]]): A list of dictionaries
            representing open orders.  Each dictionary contains the following
            keys: 'product', 'date' and 'quantity'. The quantities here are
            always positive.

        Returns:
            - List[Dict[str, any]]: A list of dictionaries representing the
            difference in quantities across time.  Each dictionary contains the
            following keys: 'item_code', 'date_from', 'date_to', 'qty'.  If the 'to'
            key is None, it means that there are not other orders modifying the
            quantity anymore.
        """

        ro_field_mapping = {
            "item_code": required_orders_field_mapping.get("item_code", "item_code"),
            "due_date": required_orders_field_mapping.get("due_date", "due_date"),
            "qty": required_orders_field_mapping.get("qty", "qty"),
        }
        required_orders = select_fields(required_orders, ro_field_mapping)

        oo_field_mapping = {
            "item_code": open_orders_field_mapping.get("item_code", "item_code"),
            "due_date": open_orders_field_mapping.get("due_date", "due_date"),
            "qty": open_orders_field_mapping.get("qty", "qty"),
        }
        open_orders = select_fields(open_orders, oo_field_mapping)

        # Group all orders and organise them in following format: List({'item': (date, qty)})
        quantities = self._group_and_sort_item_quantities_by_date(
            required_orders, open_orders
        )

        # For each item, iterate through its tuples (date, qty)
        result = []
        for item in quantities:
            if item_codes and item not in item_codes:
                continue

            qty = 0
            prev_date = None
            for date, quantity in quantities[item]:
                if prev_date is None:  # for first tuple
                    qty += quantity
                    prev_date = date
                    continue

                if shortages_only and qty > 0:
                    qty += quantity
                    prev_date = date
                    continue

                record = {
                    "item_code": item,
                    "date_from": prev_date,
                    "date_to": date,
                    "qty": qty,
                }
                result.append(record)
                qty += quantity
                prev_date = date

            # For last tuple
            result.append(
                {
                    "item_code": item,
                    "date_from": prev_date,
                    "date_to": None,
                    "qty": qty,
                }
            )

        if to_csv_path is not None:
            result_fmt = self._format_inventory_over_time_output_for_csv(result)
            to_csv(result_fmt, to_csv_path)
        else:
            return result

    def _format_inventory_over_time_output_for_csv(self, data) -> List:
        headers = ["Item", "From", "To", "Quantity"]
        output = [headers]

        for d in data:
            item = d["item_code"]
            date_from = f"{d['date_from']:%Y-%m-%d}"
            date_to = f"{d['date_to']:%Y-%m-%d}" if d["date_to"] is not None else ""
            qty = d["qty"]

            output.append([item, date_from, date_to, qty])

        return output

    def get_adjacency_list(self, related_to_item=None):
        """
        Returns a JSON-formatted string representing the factory portfolio using
        the adjacency list model.

        The returned JSON string represents a tree structure, where each node is
        represented as an object with an 'id' field and a 'children' field. The
        'id' field is a unique identifier for the node, and the 'children' field
        is an array of objects representing the node's children.

        Returns:
            A JSON-formatted string representing the internal data of the class
            using the adjacency list model.
        """

        # Store the result of get_ids() in a dictionary to avoid recomputing it
        # in every iteration
        ids_dict = {item: index for index, item in enumerate(self.items)}

        if related_to_item:
            pass

        else:
            # Use list comprehension to iterate over self.items, as it's faster
            output = [
                {
                    "id": ids_dict[item],
                    "item_code": item.code,
                    "parent_ids": [ids_dict[p] for p in item.parents],
                    "child_ids": [ids_dict[c] for c in item.children],
                }
                for item in self.items
            ]

        return output

def run():
    pass
