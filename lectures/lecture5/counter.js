window.localStorage.getItem("counter") ?? window.localStorage.setItem("counter", 0);

function count() {
    let counter = window.localStorage.getItem("counter");
    counter++;
    document.querySelector("h1").innerHTML = counter;

    window.localStorage.setItem("counter", counter);
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("button").onclick = count;
    document.querySelector("h1").innerText = window.localStorage.getItem("counter");
})