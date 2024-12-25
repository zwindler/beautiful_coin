// Fetch the form and output elements
const form = document.getElementById('generator-form');
const output = document.getElementById('output');

// Toggle collapsible sections
document.querySelectorAll('.collapsible').forEach(button => {
    button.addEventListener('click', () => {
        const content = button.nextElementSibling;
        if (content.style.display === 'block' || content.style.display === '') {
            content.style.display = 'none';
        } else {
            content.style.display = 'block';
        }
    });
});

// Fetch generated SVGs
async function fetchGeneratedCoin() {
    const formData = new FormData(form);
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            output.innerHTML = `
                <div class="coin-container">
                    <div>${data.heads}</div>
                </div>
                <div class="coin-container">
                    <div>${data.tails}</div>
                </div>
            `;
        } else {
            output.innerHTML = `<p>Error generating SVGs. Please try again.</p>`;
        }
    } catch (error) {
        output.innerHTML = `<p>Error connecting to the server. Please try again.</p>`;
    }
}

// Trigger the generation on page load
document.addEventListener('DOMContentLoaded', fetchGeneratedCoin);

// Trigger the generation on form changes
form.addEventListener('change', fetchGeneratedCoin);

// Show text fields only when "none" (Text) is selected
function toggleTextInputs(selectId, textInputId) {
    const selectElement = document.getElementById(selectId);
    const textInputDiv = document.getElementById(textInputId);

    if (selectElement.value === "none") {
        textInputDiv.style.display = "block";
    } else {
        textInputDiv.style.display = "none";
    }
}

// Initialize visibility on page load
document.addEventListener("DOMContentLoaded", () => {
    toggleTextInputs('sides-heads', 'text-input-heads');
    toggleTextInputs('sides-tails', 'text-input-tails');
});