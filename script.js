document.getElementById('analyze-button').addEventListener('click', function() {
    var text = document.getElementById('text-input').value;
    // Here you will handle the text, send it to the backend, and get the result
    // For demonstration, let's just log it to the console
    console.log("Text to analyze:", text);
    // After getting the result from the backend, update the UI
    // document.getElementById('result').innerText = 'Sentiment: Positive'; // Example
});
