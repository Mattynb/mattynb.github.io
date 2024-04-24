function updateDuration(taskName) {
    fetch('/get_duration/' + taskName)
        .then(response => response.json())
        .then(data => {
            document.getElementById('duration-' + taskName).innerText = data.duration.toFixed(2) + ' minutes';
        })
        .catch(error => console.error('Error:', error));
}

setInterval(function() {
    // Assuming you have an identifier for each task to separate them
    ['TaskA', 'TaskB', 'TaskC', 'TaskD', 'TaskE'].forEach(taskName => {
        updateDuration(taskName);
    });
}, 5000);  // Update every 5000 milliseconds (5 seconds)
