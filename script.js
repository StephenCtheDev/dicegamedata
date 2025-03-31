let totalRolls = 0; // Counter for the total number of rolls
let rollResults = {}; // Stores the count of each dice combination

function rollDice() {
    const dice = document.querySelectorAll('.dice');
    const output = document.getElementById('output');
    const rollCountElement = document.getElementById('roll-count');
    const rollOddsElement = document.getElementById('roll-odds');
    let die1Value = 0;
    let die2Value = 0;

    dice.forEach((die, index) => {
        // Remove any existing active class
        die.querySelectorAll('.face').forEach(face => {
            face.classList.remove('active');
        });

        const numberRolled = Math.floor(Math.random() * 6) + 1;

        // Assign the rolled value to the corresponding die variable
        if (index === 0) {
            die1Value = numberRolled;
        } else if (index === 1) {
            die2Value = numberRolled;
        }

        const x = Math.floor(Math.random() * 360);
        const y = Math.floor(Math.random() * 360);

        // Apply active class to the face corresponding to the rolled number
        const activeFace = die.querySelectorAll('.face')[numberRolled - 1];
        activeFace.classList.add('active');

        // Rotate the die based on the rolled number
        switch (numberRolled) {
            case 1:
                die.style.transform = `rotateX(${x}deg) rotateY(${y}deg) rotateZ(0deg)`;
                break;
            case 2:
                die.style.transform = `rotateX(${x + 90}deg) rotateY(${y}deg) rotateZ(0deg)`;
                break;
            case 3:
                die.style.transform = `rotateX(${x + 180}deg) rotateY(${y}deg) rotateZ(0deg)`;
                break;
            case 4:
                die.style.transform = `rotateX(${x + 270}deg) rotateY(${y}deg) rotateZ(0deg)`;
                break;
            case 5:
                die.style.transform = `rotateX(${x}deg) rotateY(${y + 90}deg) rotateZ(0deg)`;
                break;
            case 6:
                die.style.transform = `rotateX(${x}deg) rotateY(${y - 90}deg) rotateZ(0deg)`;
                break;
        }
    });

    // Update total roll count
    totalRolls++;
    rollCountElement.textContent = `Total Rolls: ${totalRolls}`;

    // Store the dice combination result
    let combo = `${die1Value}-${die2Value}`;
    rollResults[combo] = (rollResults[combo] || 0) + 1;

    // Calculate the odds of the current combination
    let odds = ((rollResults[combo] / totalRolls) * 100).toFixed(2);
    rollOddsElement.textContent = `Odds: ${odds}%`;

    // Update the output text to show the value of each die
    output.textContent = `Die 1: ${die1Value}, Die 2: ${die2Value}`;
}

