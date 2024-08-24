document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeSwitch = document.getElementById('theme-switch');
    themeSwitch.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        }
    });

    // Apply saved theme on load
    if (localStorage.getItem('theme') === 'dark') {
        themeSwitch.checked = true;
        document.body.classList.add('dark-theme');
    }

    // Handle form submission via AJAX
    document.getElementById('plotForm').addEventListener('submit', handleFormSubmit);

    function handleFormSubmit(event) {
        event.preventDefault();

        const multiplierInput = document.getElementById("id_multiplier");

        if (multiplierInput.value === "") {
            multiplierInput.focus();
            return false;
        }

        const formData = new FormData(document.getElementById("plotForm"));

        fetch("", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.text())
        .then(html => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;

            const newPlot = tempDiv.querySelector('#plot-container').innerHTML;
            document.getElementById("plot-container").innerHTML = newPlot;

            multiplierInput.focus();
        })
        .catch(error => console.error('Error:', error));

        return false;
    }

    // Function to handle the format change and submit the form automatically
    function formatChanged() {
        handleFormSubmit(new Event('submit'));
    }
});
