document.getElementById('solveBtn').addEventListener('click', async () => {
    const problem = document.getElementById('problemInput').value;

    if (!problem) {
        alert("Please enter a math problem!");
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem })
    });

    const data = await response.json();
    if (data.result !== null) {
        document.getElementById('result').innerText = `Result: ${data.result}`;
        document.getElementById('steps').innerHTML = data.steps.map(step => `<li>${step}</li>`).join('');
        document.getElementById('confidence').innerText = `Confidence: ${(data.confidence * 100).toFixed(2)}%`;
    } else {
        document.getElementById('result').innerText = "Unable to solve the problem";
    }
});
