function containsNumbers(str) {
    return /[0-9]/.test(str);
  }


function containsPercent(str){
    let pattern = /%/;
    return pattern.test(str);
}

function containsLetters(str){
    let pattern = /[a-z]/g;
    return pattern.test(str);
}


/**
 * Sorts an HTML table
 * 
 * @param {HTMLTableElement} table the table to sort
 * @param {number} column the index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending or descending order
 */
function sortTableByColumn(table, column, asc = true){
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    //sort each row
    const sortedRows = rows.sort((a,b) => {
        let aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
        let bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();

        aColText = aColText.toLowerCase();
        bColText = bColText.toLowerCase();

        if (containsNumbers(aColText) && containsNumbers(bColText) && !(containsLetters(aColText)) && !(containsLetters(bColText))){

            console.log("HAS NUMBERS");
            if (containsPercent(aColText)){
                console.log("HAS PERCENT");
                aColText = aColText.replace('%','');
                bColText = bColText.replace('%','');
            }

            
            return Number(aColText) > Number(bColText) ? (1*dirModifier) : (-1 * dirModifier);
        }
        else {
            console.log("NO NUMBERS");
            return aColText > bColText ? (1*dirModifier) : (-1 * dirModifier);
        }
        

    });
   
    while (tBody.firstChild){
        tBody.removeChild(tBody.firstChild);
    }
    
    tBody.append(...sortedRows);

    //remember how column is currently sorted
    table.querySelectorAll('th').forEach(th => th.classList.remove('th-sort-asc', 'th-sort-desc'));
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle('th-sort-asc',asc);
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle('th-sort-desc',!asc);
}

document.querySelectorAll(".table-striped th").forEach(headerCell => {

    headerCell.addEventListener("click", () =>{

        const tableElement = headerCell.parentElement.parentElement.parentElement; 
        //                                   returns index of this ------------------------------v
    //                   while looking in here -----------------------------v
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains('th-sort-asc');

        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });

});

sortTableByColumn(document.querySelector('table'),0)