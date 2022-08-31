const initColumns = (disable = []) => {
    const columns = [
        {
            name: "cutpot",
            items: [
                {
                    name: "Cut",
                    value: "cut"
                },
                {
                    name: "Pot",
                    value: "pot"
                },
                {
                    name: "Other",
                    value: "other"
                }
            ],
            dropdown: true,
            isActive: true,
            rules: "required|oneOf:cut,pot,other"
        },
        {
            name: "icon",
            items: [
                {
                    name: "New",
                    value: "new"
                },
                {
                    name: "Special offer",
                    value: "special_offer"
                },
                {
                    name: "Recommended",
                    value: "recommended"
                },
                {
                    name: "Rare",
                    value: "rare"
                }
            ],
            dropdown: true,
            isActive: true,
            rules: "oneOf:new,special_offer,recommended,rare"
        },
        {
            name: "origin",
            isActive: true
        },
        {
            name: "family",
            header: true,
            items: [
                {
                    code: '001',
                    name: "product 1",
                    value: "product 1"
                },
                {
                    code: '002',
                    name: "product 2",
                    value: "product 2"
                },
                {
                    code: '003',
                    name: "product 3",
                    value: "product 3"
                },
                {
                    code: '004',
                    name: "product 4",
                    value: "product 4"
                }
            ],
            dropdown: true,
            isActive: true,
            required: true,
            rules: "required"
        },
        {
            name: "variety",
            isActive: true,
            required: true,
            rules: "required"
        },
        {
            name: "color",
            isActive: true
        },
        {
            name: "grade",
            isActive: true,
            help: "The flower quality (Selected, Standard, etc...), or consistent length of stem, size of bloom."
        },
        {
            name: "quantity",
            isActive: true,
            required: true,
            rules: "required",
            type: "number",
            help: "Number of units in each box"
        },
        {
            name: "unit",
            isActive: true,
            help: "E.g: stem, branch, etc.",
            rules: "required",
            required: true
        },
        {
            name: "pieces_per_unit",
            isActive: true,
            help: "Number of pieces per each unit. E.g. stems per bunch",
            type: "number",
            rules: "min_value:1"
        },
        {
            name: "box_weight",
            isActive: true,
            type: "number"
        },
        {
            name: "price",
            isActive: true,
            required: true,
            rules: "required|greater_than_zero",
            help: "Price per unit"
        },
        {
            name: "note",
            isActive: true,
            help: "Additional information for an item"
        },
        {
            name: "private_note",
            isActive: true,
            help: "Note for internal use, not visible to merchants. The note will also show up in orders."
        },
        {
            name: "sold_out",
            isActive: true,
            rules: "isBool"
        },
        {
            name: "images",
            isActive: true
        }
    ]

    columns.forEach(col => {
        col.isActive = disable.indexOf(col.name) === -1
    })

    return columns
}


const initRow = (columns, data = null) => {
    // columns: string[]
    let row = {}
    columns.forEach((name) => {
        row[name] = null
    })

    if (data) {
        Object.keys(data).forEach((key) => {
            row[key] = data[key]
        })
    }
    return [row]
}


const checkLastRow = (rows, indexCurrentRowInput) => {
    return rows.length - 1 === indexCurrentRowInput
}


const autoAddEmptyRow = (rows, indexCurrentRowInput) => {
    if (checkLastRow(rows, indexCurrentRowInput)) return addOneRow(rows)
}


const addOneRow = (rows, index = null, data = null) => {
    /*
    {
        row: $table.rows[cursor.rowIndex],
        rowIndex: cursor.rowIndex,
        column: $table.columns[cursor.columnIndex],
        columnIndex: cursor.columnIndex,
        rows,
        rowIndexes,
        columns,
        columnIndexes,
    }
    */
    // exp: { color: 'red', box_type: 'L' }
    const column = Object.keys(rows[0])
    let newRow = initRow(column, data)[0]

    const indexInsert = index ? index : rows.length
    rows.splice(indexInsert, 0, newRow)
    return rows
}

const addRows = (rows, numberRowAdd = 1, index = null, isAbove = false) => {
    const indexInsert = index !== null ? (isAbove ? index : index + 1) : rows.length - 1
    for (let i = 0; i < numberRowAdd; i++) {
        rows = addOneRow(rows, indexInsert)
    }
    return rows
}

const deleteRows = (rows, numberRowDelete, index) => {
    rows.splice(index, numberRowDelete)
    return rows
}

const copyRows = (rows, newRows, index) => {
    const indexInsert = index + 1
    newRows.forEach((newRow) => {
        rows.splice(indexInsert, 0, newRow)
    })
    return rows
}

export {
    initRow,
    addOneRow,
    addRows,
    deleteRows,
    copyRows,
    autoAddEmptyRow,
    initColumns
}