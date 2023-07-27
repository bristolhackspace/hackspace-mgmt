$("[data-suppress-enter]").keypress(function(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
    }
});