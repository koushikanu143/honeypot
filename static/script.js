async function loadLogs(){

    const res = await fetch("/logs")
    const data = await res.json()

    const table = document.getElementById("logtable")

    // clear old rows except header
    table.innerHTML = `
        <tr>
        <th>Time</th>
        <th>IP</th>
        <th>Username</th>
        <th>Browser</th>
        </tr>
    `

    data.reverse().forEach(log =>{

        let row = table.insertRow()

        row.insertCell(0).innerText = log.time
        row.insertCell(1).innerText = log.ip
        row.insertCell(2).innerText = log.username
        row.insertCell(3).innerText = log.browser

    })

}

setInterval(loadLogs,3000)