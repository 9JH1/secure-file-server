
function getData(endpoint) {
    return fetch(`http://192.168.68.105:5000/${endpoint}`)
        .then((res) => res.text())
        .catch((error) => {
            console.error(error);
        });
}
function scrollToBottom(element) {
    element.scroll({ top: element.scrollHeight, behavior: 'smooth' });
}

(async () => {
    const terminal = document.getElementById("logs")
    String(await getData("logs")).split("\n").forEach((line) => {
        const ip = line.split("- -")[0]
        const date = String(String(line.split("]")[0]).split("[")[1]).split(" ")[0]
        const time = String(String(line.split("]")[0]).split("[")[1]).split(" ")[1]
        const request_status = String(String(line.split("\"")[2]).split("-")[0]).replaceAll(' ', '')
        const request_type = String(String(line.split("HTTP")[0]).split("\"")[1]).split(" ")[0]
        const request_path = String(String(line.split("HTTP")[0]).split("\"")[1]).split(" ")[1]
        let status_color = ""
        if (
            date != undefined &&
            time != undefined &&
            request_type != undefined &&
            request_path != undefined &&
            request_status != undefined

        ) {
            const newline = document.createElement("p");
            if (request_status == "200") {
                status_color = "good"
            } else if (request_status == "500", request_status == "404") {
                status_color = "bad"
            } else {
                status_color = "medium"
            }
            newline.innerHTML = `<span class="datetime">${date + " " + time}</span> <span class="type">${request_type}</span> <span class="path">${request_path}</span> -> <span class="status" style="color: var(--accent-${status_color})">${request_status}</span>`
            terminal.append(newline)

        }

    })
    scrollToBottom(terminal)
})()

