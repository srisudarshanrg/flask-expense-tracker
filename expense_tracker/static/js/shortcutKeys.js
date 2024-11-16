window.addEventListener("keydown", shortcutKeys)

function shortcutKeys(event) {
    if (event.altKey && event.key.toLowerCase() == "s") {
        document.getElementById("searchExpense").focus()
    }
}