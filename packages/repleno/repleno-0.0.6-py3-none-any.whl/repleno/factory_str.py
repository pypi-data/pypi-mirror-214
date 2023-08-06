import csv
import hashlib
from collections import deque
from tqdm import tqdm

"""
This class exists to create a string representation of the factory object and
thus create a serialisable object.

Due to the recursive nature of the bill of materials, if you try to serialise an
instance of factory, you will very likely get a "maximum recursion exceeded"
error, and you will not be able to seriable. 

To overcome this problem, this class was created.

Usage
=====

Use the `stringify` method to convert your csv data into a dictionary that will
be used by all the other FactoryStr class functions. In other words, the input
of all functions (except stringify) is the object that the function `stringify`
returns.

"""

# TODO: instead of extract codes, use split_sku and return a tuple


class OutputFormatter:
    """
    Makes things easier to store in a standard dictionary
    """

    def __init__(self, max_stack_size=None):
        self.records = {}
        self.highest_level = None
        self.max_stack_size = max_stack_size
        self.stack_size = 0

    def store(self, sku, parent_skus, child_skus, direction, level=0):
        if not isinstance(sku, SKU):
            raise TypeError(f"sku must be an instance of Links, not of {type(sku)}")

        if isinstance(parent_skus, SKU):
            parent_skus = [parent_skus]

        if isinstance(child_skus, SKU):
            child_skus = [child_skus]

        # check stack size
        self.stack_size += 1
        if self.max_stack_size and self.stack_size > self.max_stack_size:
            raise BufferError("Stack size exceeded maximum stack size.")

        # create key if does not exist
        self.records.setdefault(
            sku,
            {
                "sku_level": 0,
                "parent_skus": set(),
                "child_skus": set(),
            },
        )

        # store the values
        if parent_skus:
            self.records[sku]["parent_skus"] = self.records[sku]["parent_skus"].union(
                parent_skus
            )

        if child_skus:
            self.records[sku]["child_skus"] = self.records[sku]["child_skus"].union(
                child_skus
            )

        self.records[sku]["sku_level"] = level

        # check level
        if self.highest_level is None or self.highest_level < level:
            self.highest_level = level

        if direction not in ["children", "parents"]:
            raise TypeError(f"direction must be one either 'children' or 'parents'")

        if direction == "children":
            if level < self.records[sku]["sku_level"]:
                self.records[sku]["sku_level"] = level

        if direction == "parents":
            if level > self.records[sku]["sku_level"]:
                self.records[sku]["sku_level"] = level

    def get_output(self, only_list=False):
        if only_list:
            skus = self.records.keys()
            return [(sku.location, sku.item) for sku in skus]

        f_result = deque()
        sku_id_pairs = {}

        for sku, val in self.records.items():
            sku_string = sku.location + sku.item

            # Get or generate hash for all skus in this iteration
            # Why? Hash skus to avoid having special characters in ID
            sku_id_pairs.setdefault(
                sku, hashlib.sha256(sku_string.encode()).hexdigest()
            )
            sku_id = sku_id_pairs[sku]

            parent_ids = set()
            for p_sku in val["parent_skus"]:
                parent_sku_string = p_sku.location + p_sku.item
                p_id = sku_id_pairs.setdefault(
                    p_sku, hashlib.sha256(parent_sku_string.encode()).hexdigest()
                )
                parent_ids.add(p_id)

            child_ids = set()
            for c_sku in val["child_skus"]:
                child_sku_string = c_sku.location + c_sku.item
                c_id = sku_id_pairs.setdefault(
                    c_sku, hashlib.sha256(child_sku_string.encode()).hexdigest()
                )
                child_ids.add(c_id)

            id_prefix = "id_"  # so ID always starts with letters
            record = {
                "id": id_prefix + sku_id,
                "location": sku.location,
                "item_number": sku.item,
                "parents": list(sorted([id_prefix + i for i in parent_ids])),
                # "children":
                "level": ((-1) * (val["sku_level"] - self.highest_level)) + 1,
                "stocking_type": sku.stocking_type,
                "sellable_flag": sku.sellable,
            }

            # Add items without parents at the beginning of the list
            if len(val["parent_skus"]) == 0:
                f_result.appendleft(record)
            else:
                f_result.append(record)

        return list(f_result)


class SKU:
    __slot__ = ["location", "item", "stocking_type", "sellable", "phantom"]

    def __init__(
        self, location, item, stocking_type=None, sellable=False, phantom=False
    ) -> None:
        self.location = location
        self.item = item
        self.stocking_type = stocking_type
        self.sellable = sellable
        self.phantom = phantom

    def __repr__(self) -> str:
        return f"SKU({self.location}, {self.item})"

    def __eq__(self, other):
        if isinstance(other, SKU):
            return (self.location, self.item) == (other.location, other.item)
        return False

    def __hash__(self):
        return hash((self.location, self.item))

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.__slot__):
            raise StopIteration
        value = getattr(self, self.__slot__[self.index])
        self.index += 1
        return value


class Link:
    __slot__ = ["sku", "sku_child", "quantity"]

    def __init__(self, sku, next_sku, quantity) -> None:
        self.sku = sku
        self.next_sku = next_sku
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Link('{self.sku}'=>'{self.next_sku}')"

    def __eq__(self, other):
        if isinstance(other, SKU):
            return (self.sku, self.next_sku) == (other.sku, other.sku_child)
        return False

    def __hash__(self):
        return hash((self.sku, self.next_sku))


class Node:
    __slot__ = ["sku", "parents", "children"]

    def __init__(self, sku) -> None:
        if not isinstance(sku, SKU):
            raise TypeError(f"sku must be an instance of SKU, and not of {type(sku)}")

        self.sku = sku
        self.parent_links = set()  # set(Links)
        self.child_links = set()  # set(Links)

    def __repr__(self) -> str:
        return f"Node({self.sku}, {len(self.parent_links)}p, {len(self.child_links)}c)"

    @property
    def parent_skus(self):
        return [link.next_sku for link in self.parent_links]

    @property
    def child_skus(self):
        return [link.next_sku for link in self.child_links]
    
    @property
    def active_parent_skus(self):
        all_skus = [link.next_sku for link in self.parent_links]
        return [sku for sku in all_skus if sku.stocking_type != "O"]

    @property
    def active_child_skus(self):
        all_skus = [link.next_sku for link in self.child_links]
        return [sku for sku in all_skus if sku.stocking_type != "O"]


class FactoryStr:
    def __init__(self) -> None:
        self.sku_node_pairs = {}  # { SKU, Node }

    def load_data(self, filename):
        """
        It needs a csv with the following column names (names are optional, sorting is mandatory):

        1. parent_code
        2. parent_location
        3. child_code
        4. qty
        5. stocking_type_child
        6. stocking_type_parent
        7. sellable flag

        """
        # check if file exists
        # check if columns exist

        skus = {}
        links = {}
        with open(filename, "r") as f:
            reader = csv.reader(f)
            next(reader)

            for row in tqdm(reader, desc="Building model"):
                (
                    item,
                    location,
                    child_item,
                    qty,
                    stk_type_child,
                    stk_type,
                    sell_flag,
                ) = row

                # custom logic
                sell_flag = True if sell_flag == "Y" else False

                sku = skus.setdefault(
                    (location, item),
                    SKU(location, item, stocking_type=stk_type, sellable=sell_flag),
                )
                child_sku = skus.setdefault(
                    (location, child_item),
                    SKU(location, child_item, stocking_type=stk_type_child),
                )

                qty = 0 if qty == "0" or not qty or float(qty) == 0 else float(qty)
                link = links.setdefault((sku, child_sku), Link(sku, child_sku, qty))
                inverse_qty = 0 if qty == 0 else 1 / qty
                inversed_link = links.setdefault(
                    (child_sku, sku), Link(child_sku, sku, inverse_qty)
                )

                node = self.sku_node_pairs.setdefault(sku, Node(sku))
                node.child_links.add(link)

                node_child = self.sku_node_pairs.setdefault(child_sku, Node(child_sku))
                node_child.parent_links.add(inversed_link)

    def get_nodes(self, skus):
        return [self.sku_node_pairs[sku] for sku in skus]

    def get_lineage(
        self,
        location,
        item,
        include_obsoletes=True,
        max_stack_size=None,
    ):
        """
        It gets all the parents and children of a location + item code.

        It returns a list of dictionaries containing the following keys:
        {
            "id": the hashed string of location + item_number,
            "location": the location code,
            "item_number": the item code,
            "parents": the ID's of the immediate parents,
            "children": the ID's of the immediate children,
            "stocking_type": the stocking type,
            "level": starts at 0 with root items and increases by +1,
        }

        The parents list contains only items that have id's
        """

        input_node = self.sku_node_pairs.get(SKU(location, item))

        if not input_node:
            raise KeyError(f"The location-item pair has not been found: '{location}' - '{item}'")
        if not include_obsoletes and input_node.sku.stocking_type == "O":
            return []

        output = OutputFormatter(max_stack_size=max_stack_size)

        # add current items and iterate over the children
        # ===============================================

        parent_skus = input_node.parent_skus if include_obsoletes else input_node.active_parent_skus
        queue = [(parent_skus, input_node, 0)]
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, node, level = queue.pop(0)

                child_skus = node.child_skus if include_obsoletes else node.active_child_skus

                output.store(
                    sku=node.sku,
                    parent_skus=sku_ancestor,
                    child_skus=child_skus,
                    level=level,
                    direction="children",
                )

                child_nodes = self.get_nodes(child_skus)
                for child_node in child_nodes:
                    queue.append((node.sku, child_node, level - 1))

        # iterate over the parents
        # ==========================
        # get parent nodes from node

        child_skus = input_node.child_skus if include_obsoletes else input_node.active_child_skus
        queue = [(child_skus, input_node, 0)]
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, node, level = queue.pop(0)

                parent_skus = node.parent_skus if include_obsoletes else node.active_parent_skus

                output.store(
                    sku=node.sku,
                    parent_skus=parent_skus,
                    child_skus=sku_ancestor,
                    level=level,
                    direction="parents",
                )

                parent_nodes = self.get_nodes(parent_skus)
                for parent_node in parent_nodes:
                    queue.append((node.sku, parent_node, level + 1))

        return output.get_output()




    def get_collaterals(
        self,
        location,
        item,
        include_obsoletes=False,
        max_stack_size=None,
        only_list=False,
    ):
        """
        It generates a list of all items that meet the following criteria:
            1. Items that use item_code as input material for their produciton;
            2. Items that are used as input material for item_code's production;
            3. Any indirect items that satisfy the point 1 or 2.

        It returns a list of dictionaries with the following keys:

            TODO: complete doscstring

        """
        input_node = self.sku_node_pairs.get(SKU(location, item))

        if not input_node:
            raise KeyError(f"The location-item pair has not been found: '{location}' - '{item}'")
        if not include_obsoletes and input_node.sku.stocking_type == "O":
            return []

        output = OutputFormatter(max_stack_size=max_stack_size)

        output = self._scan_this_and_parents(
            input_node=input_node,
            collaterals=output,
            include_obsoletes=include_obsoletes,
        )
        output = self._scan_children(
            collaterals=output,
            current_node=input_node,
            level=0,
            include_obsoletes=include_obsoletes,
        )

        return output.get_output(only_list)

    def _scan_this_and_parents(self, input_node, collaterals, include_obsoletes):
        p_collaterals = collaterals

        child_skus = input_node.child_skus if include_obsoletes else input_node.active_child_skus
        queue = [(child_skus, input_node, 0)]
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, node, level = queue.pop(0)

                # Scan the children and add the result to p_collaterals
                p_collaterals = self._scan_children(collaterals=p_collaterals, current_node=node, level=level, include_obsoletes=include_obsoletes)

                # Filter out obsoletes if needed
                parent_skus = node.parent_skus if include_obsoletes else node.active_parent_skus

                # Add parent to collaterals
                p_collaterals.store(
                    sku=node.sku,
                    parent_skus=parent_skus,
                    child_skus=sku_ancestor,
                    level=level,
                    direction="parents",
                )

                # Move to next parents
                parent_nodes = self.get_nodes(parent_skus)
                for parent_node in parent_nodes:
                    queue.append((node.sku, parent_node, level + 1))

        return p_collaterals

    def _scan_children(self, collaterals, current_node, level, include_obsoletes):
        """
        Check if child items should be part of collaterals when self is being
        obsoleted
        """

        # Start from the children
        child_skus = current_node.child_skus if include_obsoletes else current_node.active_child_skus
        child_nodes = self.get_nodes(child_skus)

        # Remove the child node that the scan is coming from
        # ?????

        queue = [(current_node.sku, child_node, level - 1) for child_node in child_nodes]
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, node, level = queue.pop(0)

                # Logic to see if child should be added
                sellable = node.sku.sellable
                child_skus = node.parent_skus
                collaterals_set = set(collaterals.records.keys())
                all_parents_in_collaterals = not bool(set(child_skus) - collaterals_set)
                add_children = not sellable and ((len(child_skus) <= 1) or (all_parents_in_collaterals))

                if add_children:
                    # Filter out obsoletes if needed
                    child_skus = node.child_skus if include_obsoletes else node.active_child_skus

                    # Add child to collaterals
                    collaterals.store(
                        sku=node.sku,
                        parent_skus=sku_ancestor,
                        child_skus=child_skus,
                        level=level,
                        direction="children",
                    )

                    # Move to next children
                    child_nodes = self.get_nodes(child_skus)
                    for child_node in child_nodes:
                        queue.append((node.sku, child_node, level - 1))
        
        return collaterals
