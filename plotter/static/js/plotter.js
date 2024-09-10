document.addEventListener('DOMContentLoaded', function() {
    console.log("Document loaded and DOM fully parsed");

    const plotForm = document.getElementById('plotForm');
    const presetField = document.getElementById('id_preset');

    // Fetch presets from the JSON file
    fetch('/static/presets/class_presets.json')
        .then(response => response.json())
        .then(presets => {
            console.log("Presets loaded:", presets);

            // Function to update form fields with preset values
            function updateFormFields(presetValues) {
                for (const fieldId in presetValues) {
                    const field = document.getElementById(`id_${fieldId}`);
                    if (field) {
                        field.value = presetValues[fieldId];
                    }
                }
                // Re-render MathJax to ensure the equations are displayed correctly
                if (window.MathJax) {
                    console.log("Re-rendering MathJax");
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                }
            }

            // Add event listener directly to the presetField
            presetField.addEventListener('change', function() {
                console.log("Preset changed to:", presetField.value);
                
                // If preset is selected, update form fields with preset values
                if (presets[presetField.value]) {
                    updateFormFields(presets[presetField.value]);

                    // Optionally, you can submit the form to update the calculated outputs
                    handleFormSubmit(new Event('submit'));
                }
            });

            // Automatically switch preset to 'custom' when any input changes
            const formFields = plotForm.querySelectorAll('input, select, textarea');
            formFields.forEach(field => {
                if (field.id !== 'id_preset') {
                    field.addEventListener('input', function() {
                        console.log("Field changed:", field.id);
                        if (presetField.value !== 'custom') {
                            presetField.value = 'custom';
                            console.log("Preset changed to 'custom' due to modification in form field:", field.id);
                        }
                    });
                }
            });

            // Trigger form submission when pressing "Enter" in any input field
            plotForm.addEventListener('keydown', function(event) {
                console.log("Keydown event detected:", event.key);
                if (event.key === 'Enter') {
                    event.preventDefault(); // Prevent default form submission
                    console.log("Enter key pressed, submitting form via AJAX");
                    handleFormSubmit(event); // Manually handle form submission
                }
            });

            function handleFormSubmit(event) {
                if (event) event.preventDefault();
                console.log("Form submission triggered");

                const formData = new FormData(plotForm);
                console.log("Form data prepared for submission:", formData);

                fetch("", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                })
                .then(response => {
                    console.log("Response received from server:", response);
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(html => {
                    console.log("HTML received from server, updating plot");
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = html;

                    // Update the plot container with the new plot
                    const newPlot = tempDiv.querySelector('#plot-container').innerHTML;
                    document.getElementById("plot-container").innerHTML = newPlot;

                    // Update the calculated values
                    document.querySelector('.readonly-field.vmin').textContent = tempDiv.querySelector('.readonly-field.vmin').textContent;

                    for (let idx = 1; idx <= 7; idx++) {
                        document.querySelector(`.readonly-field.re_v${idx}`).textContent = tempDiv.querySelector(`.readonly-field.re_v${idx}`).textContent;
                        document.querySelector(`.readonly-field.im_v${idx}`).textContent = tempDiv.querySelector(`.readonly-field.im_v${idx}`).textContent;
                    }

                    document.querySelector('.readonly-field.pout').textContent = tempDiv.querySelector('.readonly-field.pout').textContent;
                    document.querySelector('.readonly-field.eta').textContent = tempDiv.querySelector('.readonly-field.eta').textContent;

                    // Re-render MathJax for the updated content
                    if (window.MathJax) {
                        console.log("Re-rendering MathJax");
                        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                    }

                    // Update the save link with the new plot URL
                    const plotImage = document.getElementById('generated-plot');
                    const saveGraphLink = document.getElementById('save-graph-link');

                    if (plotImage && saveGraphLink) {
                        saveGraphLink.href = plotImage.src; // Update the href with the new plot URL
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }

            // Automatically submit the form when the format is changed
            const formatSelect = document.getElementById('id_output_format');
            if (formatSelect) {
                formatSelect.addEventListener('change', () => {
                    console.log("Output format changed, re-submitting form");
                    handleFormSubmit(new Event('submit'));
                });
            }
        })
        .catch(error => {
            console.error("Error loading presets:", error);
        });
});
