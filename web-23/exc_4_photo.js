// Add to onclick attribute of button

function imageClick() {
    // Modify img source to user's inputted URL
    let url = document.querySelector("input").value
    document.getElementById("photo").src = url;
}
