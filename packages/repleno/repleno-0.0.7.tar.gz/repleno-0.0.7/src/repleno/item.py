from __future__ import annotations

from enum import Enum
from typing import List
from repleno.utils import *
import warnings

import pptree

import logging


class ItemType(Enum):
    PARENT = "ultimate parent"
    INTERMEDIATE = "intermediate"
    CHILD = "ultimate child"
    UNDEFINED = "undefined"


class _ItemLink:
    def __init__(self, child: Item, qty: float):
        if not isinstance(child, Item):
            raise TypeError(f"child argument must be an Item instance.")

        self.item = child
        self.qty = qty

    def __repr__(self):
        return f"{self.item}"

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        if value is None:
            self._qty = 1
            return
        value = convert_to_float(value)

        if value <= 0:
            raise ValueError("Quantity must be a positive number.")

        self._qty = value


class Item:
    """Any single article held in stock inside of the factory. It can be any
    item finished good (FG), semi-assemblies or raw-materials.
    """

    classification_rank = {
        "AX": 90,
        "AY": 80,
        "AZ": 70,
        "BX": 60,
        "BY": 50,
        "BZ": 40,
        "CX": 30,
        "CY": 20,
        "CZ": 10,
        "NA": 00,
    }

    def __init__(
        self,
        code,
        inventory_balance: float = 0,
        minimum_order_qty: float = 1,
        batch_qty: float = 0,
        safety_stock_qty: float = 0,
        lead_time: int = 0,
        unit_of_measure="",
        classification="NA",
        sellable=False,
    ):
        """
        Initialise a new instance of Item.

        Args:
            code (_type_): _description_
            inventory_balance (float, optional): _description_. Defaults to 0.
            minimum_order_qty (float, optional): _description_. Defaults to 1.
            batch_qty (float, optional): _description_. Defaults to 0.
            safety_stock_qty (float, optional): _description_. Defaults to 0.
            lead_time (int, optional): _description_. Defaults to 0.
            unit_of_measure (str, optional): _description_. Defaults to "".
            classification (str, optional): _description_. Defaults to "NA".
            - sellable (bool, optional): True if item type is ultimate parent,
            False otherwise. It can be changed manually for cases when item is
            used both as component to another item and at the same time is
            sellable.  Defaults to False.
        """
        # Links between items
        self._child_links: List[_ItemLink] = []
        self._parent_links: List[_ItemLink] = []

        self.code = code
        self.inventory_balance = inventory_balance
        self.minimum_order_qty = minimum_order_qty
        self.batch_qty = batch_qty
        self.safety_stock_qty = safety_stock_qty
        self.lead_time = lead_time
        self.unit_of_measure = unit_of_measure
        self.sellable = sellable

        # necessary if setter gets classification before assigning a classification
        self._classification = "NA"
        self.classification = classification
        self._type = ItemType.UNDEFINED

        # Only used in the visualisation by pptree
        self._pptree_parents: List[Item] = []
        self._pptree_children: List[Item] = []

    def __repr__(self):
        return f"Item(code={self.code}, inventory_balance={self._inventory_balance}, minimum_order_qty={self._minimum_order_qty}, batch_qty={self._batch_qty}, safety_stock_qty={self._safety_stock_qty}, lead_time={self._lead_time}, classification= {self._classification}, selleable={self.sellable}, type={self._type})"

    def __str__(self):
        return f"{self.code}"

    # Children
    # ========================

    @property
    def children(self):
        """Returns all the immediate child items."""
        output = []
        for child_link in self._child_links:
            output.append(child_link.item)

        return output

    @property
    def child_links(self):
        """Returns all the immediate child items along with the quantities."""
        return self._child_links

    @property
    def ultimate_children(self):
        """Return all the lowermost/lowest child items in this bill of materials.
        
        Note: list may contain duplicate parent items.
        """
        return self._get_leaf_nodes("children")

    @property
    def all_children(self):
        """Return all the child items in the bill of materials (from immediate to ultimate items)"""
        return self._level_order_traverse("children")

    # Parents
    # =======================

    @property
    def parents(self):
        """Returns all the immediate parent items."""
        output = []
        for parent_link in self._parent_links:
            output.append(parent_link.item)

        return output

    @property
    def parent_links(self):
        """Returns all the immediate parent items along with the quantities."""
        return self._parent_links

    @property
    def ultimate_parents(self):
        """Return all the topmost/highest parent items in this bill of materials.
        
        Note: list may contain duplicate parent items.
        """
        return self._get_leaf_nodes("parents")

    @property
    def all_parents(self):
        """Return all the parent items in the bill of materials (from immediate to ultimate items)"""
        return self._level_order_traverse("parents")

    # Others
    # =========================

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        # Remove empty spaces from both sides and leading zeros
        if not value or not isinstance(value, str):
            raise ValueError(
                f"{value} is not a valid Item code. Enter a valid non-empty string."
            )

        self._code = value.strip().upper().lstrip("0")

    @property
    def inventory_balance(self):
        """Get the value of inventory qty."""
        return self._inventory_balance

    @inventory_balance.setter
    def inventory_balance(self, value):
        try:
            value = float(value)
        except TypeError:
            print("minimum order qty must be an integer or a float.")
            raise
        self._inventory_balance = float(value)

    @property
    def minimum_order_qty(self):
        """Get the value of minimum order qty."""
        return self._minimum_order_qty

    @minimum_order_qty.setter
    def minimum_order_qty(self, value):
        """Set the value of minimum order qty."""
        try:
            value = float(value)
        except TypeError:
            print("minimum order qty must be an integer or a float.")
            raise

        if value <= 0:
            raise ValueError(f"minimum order qty must be a positive number.")

        self._minimum_order_qty = float(value)

    @property
    def batch_qty(self):
        """Get the value of rounding value qty."""
        return self._batch_qty

    @batch_qty.setter
    def batch_qty(self, value):
        """Set the value of rounding value qty."""
        try:
            value = float(value)
        except TypeError:
            print("rounding value qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"rounding value qty must be a positive number.")

        self._batch_qty = float(value)

    @property
    def safety_stock_qty(self):
        """Get the value of safety stock qty."""
        return self._safety_stock_qty

    @safety_stock_qty.setter
    def safety_stock_qty(self, value):
        """Set the value of safety stock qty."""
        try:
            value = float(value)
        except TypeError:
            print("safety stock qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"safety stock qty must be a positive number.")

        self._safety_stock_qty = float(value)

    @property
    def lead_time(self):
        """Get the value of lead time."""
        return self._lead_time

    @lead_time.setter
    def lead_time(self, value):
        """Set the value of lead time."""
        try:
            value = float(value)
        except TypeError:
            print("lead time must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"lead time must be a positive number.")

        self._lead_time = int(value)

    @property
    def unit_of_measure(self):
        """Get the value of unit of measure."""
        return self._unit_of_measure

    @unit_of_measure.setter
    def unit_of_measure(self, value):
        """Set the value of lead time."""

        if not isinstance(value, str):
            raise TypeError("Unit of measure must be a string.")

        self._unit_of_measure = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, ItemType):
            raise TypeError(
                f"Argument must be of type NodeType.\nYour value is:{value} and type: {type(value)}"
            )

        if value == ItemType.INTERMEDIATE:
            raise ValueError(
                f"You can only assign the values: PARENT and CHILD.\nYour value is: {value.name}"
            )

        # current   new     result
        # ===========================
        # None      parent  parent
        # None      child   child
        # child     parent  intermediate
        # child     child   child
        # parent    parent  parent
        # parent    child   intermediate

        if value != self._type:
            if self._type == ItemType.UNDEFINED:
                self._type = value
            else:
                self._type = ItemType.INTERMEDIATE

    @property
    def classification(self):
        return self._classification

    def _level_order_traverse(self, direction):
        # try to get the attribute
        if getattr(self, direction) is None:
            raise AttributeError(
                f"Attribute {direction} not found in class {self.__class__.__name__}"
            )

        stack = getattr(self, direction)  # self should not be in the output
        result = []

        while stack:
            node = stack.pop()
            result.append(node)

            for nodes in getattr(node, direction):
                stack.append(nodes)

        return result

    def _get_leaf_nodes(self, direction):
        if getattr(self, direction) is None:
            raise AttributeError(
                f"Attribute {direction} not found in class {self.__class__.__name__}"
            )

        stack = getattr(self, direction)
        root_nodes = []

        while stack:
            node = stack.pop()
            if len(getattr(node, direction)) == 0:
                root_nodes.append(node)
            else:
                stack += getattr(node, direction)

        return root_nodes



    @classification.setter
    def classification(self, value):
        """
        Sets the value of classification

        Args:
            value (str): the length must be two and the first letter must be
            either A, B, or C and the second letter must be X, Y, or Z.

            e.g.:
                AX
                AY
                BZ
                CZ
        """

        new_classification = self.classification_rank.get(value)
        if new_classification is None:
            raise ValueError(
                f"Value '{new_classification}' not found in classifications."
            )

        if self._is_classification_higher(self.classification, value):
            self._classification = value
            self._flush_classifications(value)

    @property
    def sellable(self):
        return self._sellable

    @sellable.setter
    def sellable(self, value):
        if not isinstance(value, bool):
            raise TypeError("Input must be a boolean.")
        self._sellable = value

    def _flush_classifications(self, new_value):
        """
        Push this item classification down to their children and update the
        childrens classification if needed.

        Classification is updated only when the new classification has a higher
        score than the current classification.

        Args:
            new_classification (str): new classification for this item.
        """
        queue = [self]

        while queue:
            for _ in range(len(queue)):
                node = queue.pop()

                if self._is_classification_higher(node.classification, new_value):
                    node.classification = new_value

                for child_link in node._child_links:
                    queue.append(child_link.item)

    def _is_classification_higher(self, current, new):
        return self.classification_rank[current] < self.classification_rank[new]

    def get_missing_safety_stock_qty(self):
        if self.inventory_balance < 0:
            return self.safety_stock_qty

        if self.inventory_balance < self.safety_stock_qty:
            return self.safety_stock_qty - self.inventory_balance
        else:
            return 0

    def lot_size(self, order_qty):
        """Rounds the order quantity to the nearest multiple of the minimum order quantity.

        If a rounding order quantity is specified, the rounded value will be a multiple
        of the rounding value that is higher than the minimum order quantity.

        Args:
            order_qty (float): The order quantity to round.

        Returns:
            float: The rounded order quantity.

        """
        if order_qty == 0:
            return 0

        if self.batch_qty:
            min_qty = self.minimum_order_qty or 0
            order_qty = max(order_qty, min_qty)
            return get_next_multiple(order_qty, self.batch_qty)

        if self.minimum_order_qty:
            return max(order_qty, self.minimum_order_qty)

    def _add_child(self, child_node, qty=1):
        """
        Note: this is an internal method that can be used externally only by the
        Factory class. This is because the Factory needs to register it to keep
        track of all the items.

        """
        if not isinstance(child_node, Item):
            raise TypeError("child_node argument must be of type Item.")

        if self.code == child_node.code:
            warnings.warn(
                f"parent and child codes cannot be the same.\n{child_node.code} is parent and child at the same time"
            )
        
        self._check_for_recursion(child_node)
        self._update_types(child_node)
        self._update_sellable_flag(child_node)
        self._add_child_for_pptree_visualisation(child_node)

        # Link both ways: parent > child and child > parent
        qty = convert_to_float(qty)
        self._child_links.append(_ItemLink(child_node, qty))
        if qty == 0:
            child_node._parent_links.append(_ItemLink(self, 0))
        elif qty is None:
            child_node._parent_links.append(_ItemLink(self, 1))
        else:
            child_node._parent_links.append(_ItemLink(self, 1 / qty))


    def _check_for_recursion(self, child_node):
        if child_node in self.all_parents:
            raise ValueError(
                f"Linking the parent-child relationship ('{self.code}'>>'{child_node.code}') resulted in recursion."
            )

    def _update_types(self, child_node):
        self.type = ItemType.PARENT
        child_node.type = ItemType.CHILD

    def _update_sellable_flag(self, child_node):
        if self.type == ItemType.PARENT:
            self.sellable = True

        if child_node.type == ItemType.PARENT:
            self.sellable = True

    def _add_child_for_pptree_visualisation(self, child_node):
        child_node._pptree_parents.append(self)
        self._pptree_children.append(child_node)

    def show(self, direction="children"):
        if direction not in ["children", "parents"]:
            raise ValueError('direction arg must be "children" or "parents"')
        else:
            # second argument is property name of Node that holds next node
            pptree.print_tree(self, childattr="_pptree_" + direction)

    def get_phaseout_collaterals(self, tree=False):
        """
        Returns all items that should be phased out together

        Args:
            tree (bool, optional): If true, it returns the same item with the
            prefix "po_" and linked to this item are the item collaterals.
            Defaults to False and returns only a list of item codes that are
            collaterals.

        Returns:
            list or Item: returns a list if tree is False, otherwise it returns
            an Item.
        """
        logging.debug(f"Getting collaterals for {self.code}")

        po_self = Item(self.code)

        parent_collat, po_self = self._link_parents_to_po_item(po_self)
        child_collat, po_self = self._link_child_to_po_item(parent_collat, po_self)

        all_collaterals = set()
        all_collaterals.update(parent_collat)
        all_collaterals.update(child_collat)
        all_collaterals.discard(self.code)

        if tree:
            return po_self
        else:
            return all_collaterals

    def _link_parents_to_po_item(self, po_self):
        """
        Check if parent items should be part of collaterals when self is being
        obsoleted
        """
        if po_self is not None and not isinstance(po_self, Item):
            raise TypeError(
                f"input is an instance of {type(po_self)}, it must be of type Item."
            )

        logging.debug(f"traversing {len(self.parents)} parents for item {self.code}")

        # Insert None so the new tree can be linked to po_self
        stack = [(parent, None) for parent in self.parents]
        collat_list = set()

        while stack:
            parent, child = stack.pop()

            # === for tree ===
            if child is None:
                po_child = po_self
            else:
                po_child = Item(child.code)

            po_parent = Item(parent.code)
            po_parent._add_child(po_child)

            # === for list ===
            collat_list.add(parent.code)
            collaterals, po_parent = parent._link_child_to_po_item(
                collat_list, po_parent
            )
            collat_list.update(collaterals)

            # === traversal ===
            child = parent
            for p in child.parents[::-1]:
                if p.code is not collaterals:
                    stack.append((p, child))

        return collat_list, po_self

    def _link_child_to_po_item(self, collaterals, po_self):
        """
        Check if child items should be part of collaterals when self is being
        obsoleted
        """
        if po_self is not None and not isinstance(po_self, Item):
            raise TypeError(
                f"input is an instance of {type(po_self)}, it must be of type Item."
            )

        stack = [(None, child) for child in self.children]
        result = set()

        while stack:
            parent, child = stack.pop()

            po_child = Item(child.code)
            if parent is None:
                po_parent = po_self
            else:
                po_parent = Item(parent.code)

            not_sellable_single_parent = len(child.parents) <= 1 and not child.sellable

            parents_code = [i.code for i in child.parents]
            all_parents_in_collaterals = not bool(set(parents_code) - collaterals)
            not_sellable_all_parents_in_collaterals = (
                len(child.parents) > 1
                and all_parents_in_collaterals
                and not child.sellable
            )

            if not_sellable_single_parent or not_sellable_all_parents_in_collaterals:
                # for tree
                child_codes = [i.code for i in po_parent.children]
                if po_child.code not in child_codes:
                    po_parent._add_child(po_child)

                # for list
                result.add(child.code)

                parent = child
                for c in parent.children[::-1]:
                    if c.code is not collaterals:
                        stack.append((parent, c))

        return result, po_self

    def _are_levels_equal(self, node, direction, past_node=None):
        anti_direction = "parents" if direction == "children" else "children"

        if not self and not node:
            # both nodes are empty, so they're equal
            return True
        elif not self or not node:
            # one node is empty and the other is not, so they're not equal
            return False
        elif self.code != node.code:
            # the nodes have different values, so the trees are not equal
            return False
        elif len(getattr(self, direction)) != len(getattr(node, direction)):
            # the nodes have different numbers of children, so the trees are not equal
            return False
        elif past_node is not None and len(getattr(self, anti_direction)) > 1:
            # recursively check the children of the parents or the parents of the children
            # perform the check in the other direction
            # get nodes in the other direction but remove the previous one
            # (where it's coming from) to avoid infine recursion
            # (bouncing back and forth between child-parent)
            next_nodes = getattr(self, anti_direction)
            next_nodes.remove(past_node)

            other_next_nodes = getattr(node, anti_direction)
            return self._move_to_next_level(
                next_nodes, other_next_nodes, anti_direction
            )

        else:
            # recursively check if each parent/child of node1 is equal to any
            # parent/child of node2
            next_nodes = getattr(self, direction)
            other_next_nodes = getattr(node, direction)
            return self._move_to_next_level(next_nodes, other_next_nodes, direction)

    def _move_to_next_level(self, next_nodes, other_next_nodes, direction):
        for next_node in next_nodes:
            found_match = False
            for other_next_node in other_next_nodes:
                if next_node._are_levels_equal(other_next_node, direction, self):
                    found_match = True
                    break
            if not found_match:
                return False
        return True

    def is_tree_equal(self, node):
        """
        Recursively checks all children and parents to see if self and node
        parameter belong to a tree with the same item codes.

        Args:
            node (Item): Second that self is compared to.

        Returns:
            bool: True if all tree is equal, False otherwise.

        """
        upwards = self._are_levels_equal(node, "parents")
        downwards = self._are_levels_equal(node, "children")

        return upwards and downwards



    def get_lineage(
        self,
        location,
        item,
        include_obsoletes=True,
        max_stack_size=None,
    ):

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
        pass
