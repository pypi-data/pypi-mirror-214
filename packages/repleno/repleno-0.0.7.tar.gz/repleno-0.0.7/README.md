
# Bill of Materials (BOM)



## Quickstart

Begin by importing the Repleno module:

.. code-block:: python
    import repleno as rpl


### Instantiate object

Instantite a factory object

.. code-block:: python 

    # The below variable represents the following BOM structure:
    #       A  
    #     / | \
    #    B  C  D
    #     \   /
    #       E
    #
    bom_data = [
        { "item": "A", "child": "B", "quantity": 1 },
        { "item": "A", "child": "C", "quantity": 2 },
        { "item": "A", "child": "D", "quantity": 0.3 },
        { "item": "B", "child": "E", "quantity": 2.5 },
        { "item": "D", "child": "E", "quantity": 1 },
    ]

    # Instantiate a factory object
    fact = rpl.Factory(bom_data)

    print(fact.get_item("A").children)
    print(fact.get_item("A").parents)
    





## Usage


### Instantiate object with a CSV file

As it's very common to have data in a CSV file when working in supply chain. 

.. code-block:: python

    fact = rpl.Factory(r"path/to/file.csv")




## Limitations

1. It does not consider different unit of measures (UoM). Every item in the BOM should have one single unit of measure. 

    Example:
    
        .. code-block:: python

            bom_data = [
                { "item": "A", "child": "B", "quantity": 2 },  # item B UoM = Units
                { "item": "B", "child": "E", "quantity": 3 },  # item B UoM = Packs
            ]
        



## Roadmap
