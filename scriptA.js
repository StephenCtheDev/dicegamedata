let totalRolls = 0; // Counter for the total number of rolls
let rollResults = {}; // Stores the count of each dice combination

// Function to simulate rolling two dice and update the UI
async function rollDice() {
    const dice = document.querySelectorAll('.dice');
    const output = document.getElementById('output');
    const rollCountElement = document.getElementById('roll-count');
    const rollOddsElement = document.getElementById('roll-odds');
    let die1Value = 0;
    let die2Value = 0;

    dice.forEach((die, index) => {
        die.querySelectorAll('.face').forEach(face => {
            face.classList.remove('active');
        });

        const numberRolled = Math.floor(Math.random() * 6) + 1;

        if (index === 0) {
            die1Value = numberRolled;
        } else if (index === 1) {
            die2Value = numberRolled;
        }

        const x = Math.floor(Math.random() * 360);
        const y = Math.floor(Math.random() * 360);

        const activeFace = die.querySelectorAll('.face')[numberRolled - 1];
        activeFace.classList.add('active');

        // Rotate the dice to simulate rolling
        const rotations = [0, 90, 180, 270];
        die.style.transform = `rotateX(${x + (rotations[numberRolled % 4])}deg) rotateY(${y}deg) rotateZ(0deg)`;
    });

    totalRolls++; // Increment the total roll counter
    rollCountElement.textContent = `Total Rolls: ${totalRolls}`;

    let combo = `${die1Value}-${die2Value}`;
    rollResults[combo] = (rollResults[combo] || 0) + 1;

    let odds = ((rollResults[combo] / totalRolls) * 100).toFixed(2);
    rollOddsElement.textContent = `Odds: ${odds}%`;

    output.textContent = `Die 1: ${die1Value}, Die 2: ${die2Value}`;

    await sendRollToServer(die1Value, die2Value); // Send the roll data to the server
    await updateGrid(); // this will fetch from the database
}

// Function to send roll results to the server for database storage
async function sendRollToServer(die1, die2) {
    try {
        await fetch('http://127.0.0.1:5000/roll_dice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ die1, die2 })
        });
    } catch (error) {
        console.error('Error sending roll data:', error);
    }
}

// Function to update the grid dynamically based on roll results
// Function to refresh the grid after every roll
async function updateGrid() {
    await fetchAndUpdateGrid(); // Re-fetch data from the database
}


// Function to get the latest roll counts from the database and update the grid
async function fetchAndUpdateGrid() {
    try {
        const response = await fetch('http://127.0.0.1:5000/get_rolls_count');
        const rollCounts = await response.json(); // Get JSON data

        // Loop through each cell and update it based on DB values
        Object.keys(rollCounts).forEach(combo => {
            const cell = document.getElementById(`cell-${combo}`);
            if (cell) {
                cell.textContent = rollCounts[combo]; // Update the cell with count
            }
        });
    } catch (error) {
        console.error('Error fetching roll counts:', error);
    }
}

// Call this function when the page loads
window.onload = function() {
    fetchAndUpdateGrid();
};

