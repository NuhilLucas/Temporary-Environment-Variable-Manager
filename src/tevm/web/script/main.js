let iEnvarCount = 0;

document.getElementById("envar-config").addEventListener("click", function(event) {
    if (event.target.closest(".trow-rembtn")) {
        event.target.closest("tr").remove();
        return;
    }

    if (event.target.closest(".trow-addbtn")) {
        const tableBody = document.querySelector("#envar-config tbody");
        const bottomRow = document.querySelector('.trow-addbtn').closest("tr");
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" name="key" id="${iEnvarCount}" placeholder="输入变量名"></td>
            <td><input type="text" name="value" id="${iEnvarCount+1}" placeholder="输入变量值"></td>
            <td class="trow-rembtn trow-btn"><i class="femj fe-reduce remove-btn" id="rem-row"></i></td>
        `;
        iEnvarCount+=2
        tableBody.insertBefore(newRow, bottomRow);
        bottomRow.scrollIntoView({ behavior: "smooth", block: "nearest" });
        return;
    }
});

document.getElementById("config-preview-btn").addEventListener("click", function(event) {
    console.log("config-preview-btn")
})

document.getElementById("config-save-btn").addEventListener("click", function(event) {
    console.log("config-save-btn")
})