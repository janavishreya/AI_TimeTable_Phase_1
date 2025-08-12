document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("timetable-form");

    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent form reload
            
            let formData = new FormData(form);

            fetch('/generate_timetable', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                displayTimetable(data);
            })
            .catch(error => console.error("Error:", error));
        });
    }
});

function displayTimetable(timetable) {
    const timetableDisplay = document.getElementById("timetable-display");
    timetableDisplay.innerHTML = "";

    let table = document.createElement("table");

    // Table Header
    let thead = document.createElement("thead");
    let headerRow = document.createElement("tr");
    let days = Object.keys(timetable);

    headerRow.innerHTML = `<th>Period</th>`;
    days.forEach(day => {
        headerRow.innerHTML += `<th>${day}</th>`;
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Table Body
    let tbody = document.createElement("tbody");
    let periods = timetable[days[0]].length;  // Get number of periods

    for (let i = 0; i < periods; i++) {
        let row = document.createElement("tr");
        row.innerHTML = `<td>Period ${i + 1}</td>`;

        days.forEach(day => {
            row.innerHTML += `<td>${timetable[day][i]}</td>`;
        });

        tbody.appendChild(row);
    }

    table.appendChild(tbody);
    timetableDisplay.appendChild(table);
}
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const loginCard = document.getElementById("loginCard");

    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent instant form submission

        // Add sliding effect
        loginCard.style.transform = "translateX(-100vw)";

        // Wait for animation to complete before submitting
        setTimeout(() => {
            loginForm.submit();
        }, 600);
    });
});

    const cards = document.querySelectorAll('.card');

    cards.forEach((card) => {
        card.addEventListener('click', (e) => {
            document.body.classList.add('slide-left');
            setTimeout(() => {
                window.location.href = card.getAttribute('href');
            }, 600); // Delay navigation to match the slide animation
            e.preventDefault();
        });
    });
