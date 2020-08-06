#133

#used in example tables.

class LinkedListItem:
    """
    object for an item in the list.

    """
    def __init__(self):
        self.nextItem = None

    def setLink(self, nextItem):
        """
        gives the item the nect item in the list

        """
        self.nextItem = nextItem


class LinkedList:
    def __init__(self, newItems=[]):
        self.headItem = None
        for item in newItems:
            self.insert(item)

    def len(self, item):
        """
        goes though all items in the list by going ot the next item in the list unitll no items left.
        :param current item to go from
        :return: next item item in the list.
        """
        if item:
            return 1 + self.len(item.nextItem)
        return 0

    def __iter__(self):
        """
        replaces the base iter function, generates the next item in the list so the list can be looped though
        :return(yield): next item in the list.
        """
        pointer = self.headItem
        while pointer:
            yield pointer
            pointer = pointer.nextItem

    def __len__(self):
        return self.len(self.headItem)

    def contains(self, itemToFind, currentItem):
        """
        goes though all items in the list
        by going ot the next item in the list unitll item specified is found

        :param(itemToFind) item that the function has to find existence of in list
        :param(currentItem) item in the
        :return(1): True, if the item specified has been found
        :return(2): current item into the function
        """
        if itemToFind == currentItem:
            return True
        if currentItem.nextItem is not None:
            return self.contains(itemToFind, currentItem.nextItem)
        return False

    def __contains__(self, itemToFind):
        return self.contains(itemToFind, self.headItem)

    def insert(self, item: LinkedListItem):
        """
        if the lst is empty , sets item as head item of list, otherwise, loops though the list to find the last item in the list.
        sets new item as the next item for the previous item that was previously at the end of the list.
        :param item to be added into the list
        """
        if self.headItem:  # non empty list
            pointer = self.headItem
            while pointer.nextItem is not None:
                pointer = pointer.nextItem
            pointer.setLink(item)
        else:  # empty list
            self.headItem = item

    def delete(self, itemtoBeDeleted):
        """
         if item1 is item before itemtoBeDeleted , and item2 is object after itemtoBeDeleted.
         item1's next item is set to item2, skipping itemtoBeDeleted so it is no linger part of the item chain.


        :param current item to deleted
        :return: if item deleted will return True, if unable to locate item , will return False
        """
        pointer = self.headItem
        while pointer:
            if pointer.nextItem == itemtoBeDeleted:
                pointer.nextItem = pointer.nextItem.nextItem
                return True
            pointer = pointer.nextItem
        return False
