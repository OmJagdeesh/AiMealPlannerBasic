document.getElementById('generate').addEventListener('click', async () => {
    const carbs = document.getElementById('carbs').value;
    const protein = document.getElementById('protein').value;
    const fat = document.getElementById('fat').value;
    const meal_type = document.getElementById('meal_type').value;
    const cuisine_type = document.getElementById('cuisine_type').value;

    const data = new URLSearchParams({
        carbs,
        protein,
        fat,
        meal_type,
        cuisine_type
    });

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        const result = await response.json();
        if (result.meal_plan) {
            // Replace newlines with HTML <br> to preserve formatting
            document.getElementById('result').innerHTML = result.meal_plan.replace(/\n/g, '<br>');
        } else {
            document.getElementById('result').textContent = result.error;
        }
    } catch (error) {
        document.getElementById('result').textContent = "Error fetching meal plan.";
    }
});

// Clear button functionality
document.getElementById('clear').addEventListener('click', () => {
    // Reset slider values to 0
    document.getElementById('carbs').value = 0;
    document.getElementById('protein').value = 0;
    document.getElementById('fat').value = 0;

    // Reset output values next to sliders
    document.querySelectorAll('output').forEach(output => {
        output.value = 0;
    });

    // Reset the meal type and cuisine type to default
    document.getElementById('meal_type').selectedIndex = 0;
    document.getElementById('cuisine_type').selectedIndex = 0;

    // Clear the result display area
    document.getElementById('result').innerHTML = '';
});

// Copy to clipboard functionality
document.getElementById('copy').addEventListener('click', () => {
    const resultText = document.getElementById('result').innerText; // Get the text to copy
    if (resultText) {
        navigator.clipboard.writeText(resultText) // Copy to clipboard
            .then(() => {
                alert('Meal plan copied to clipboard!'); // Notify the user
            })
            .catch(err => {
                console.error('Failed to copy: ', err); // Log any error
            });
    } else {
        alert('No meal plan to copy!'); // Notify if there's nothing to copy
    }
});
