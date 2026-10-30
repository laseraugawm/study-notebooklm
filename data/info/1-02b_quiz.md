# IoT Quiz

## Question 1
In the clap-controlled light experiment using the micro:bit, what is the valid numerical range for input sound detected by the built-in microphone, and what threshold value was set in the textbook algorithm to trigger a state change?

- [x] Range: $0$ to $255$; Threshold: $100$
- [ ] Range: $-1024$ to $+1024$; Threshold: $100$
- [ ] Range: $0$ to $100$; Threshold: $50$
- [ ] Range: $0$ to $1024$; Threshold: $500$

**Hint:** Consider the standard 8-bit integer range used for sound intensity input on the micro:bit.

## Question 2
In the clap-controlled light algorithm, why is a $0.5$-second ($500\text{ ms}$) pause executed immediately after detecting a clap sound?

- [x] To prevent a single physical clap from being registered multiple times consecutively.
- [ ] To give the LED display screen sufficient time to charge before turning on.
- [ ] To automatically reset the internal state variable `tag` back to $0$.
- [ ] To allow the micro:bit to switch from MakeCode block mode to Python text mode.

**Hint:** Think about how fast program loops execute relative to the duration of a sound wave in air.

## Question 3
In the restaurant calling system activity using multiple micro:bits, what rule must be followed regarding the radio group settings?

- [x] All table devices and the display device belonging to the same group must share the exact same radio group number.
- [ ] Each table device must use a unique radio group number that is different from the display device.
- [ ] The display device must cycle through radio group numbers every second to scan for tables.
- [ ] Radio group numbers are fixed by hardware and cannot be customized in software.

**Hint:** Consider how devices filter wireless broadcasts so that signals from one table group do not interfere with adjacent groups.

## Question 4
In the pedestrian signal light activity, how does the mobile receiving device alter its acoustic warning when the remaining time drops to $5$ seconds or below ($5$ down to $1$)?

- [x] It changes the tone output from 'Mi' to a higher-pitched 'Sol' note.
- [ ] It switches the tone output from 'Sol' down to a lower-pitched 'Do' note.
- [ ] It increases the duration of the 'Mi' tone from $500\text{ ms}$ to $1000\text{ ms}$.
- [ ] It mutes all sound alerts and relies exclusively on visual LED numbers.

**Hint:** Recall how musical pitch changes to indicate heightened urgency as time runs out.

## Question 5
In the safety monitoring device attached to a bathroom door, how is inactivity detected using x-axis acceleration readings $a$ and $b$ taken $100\text{ ms}$ apart?

- [x] Inactivity is recorded if $a - b < 100$.
- [ ] Inactivity is recorded if $a + b > 1024$.
- [ ] Inactivity is recorded if $a \times b = 0$.
- [ ] Inactivity is recorded if $a - b > 500$.

**Hint:** Consider whether movement creates a large difference or a small difference between two consecutive sensor readings.

## Question 6
In the bathroom door monitoring system, a `count` threshold of $100$ represents $10\text{ seconds}$ of inactivity (with each check taking $100\text{ ms}$). To extend this movement detection threshold to $5\text{ hours}$, what must the target `count` value be?

- [x] $180,000$
- [ ] $18,000$
- [ ] $36,000$
- [ ] $500,000$

**Hint:** Calculate the total number of $100\text{ ms}$ sampling intervals contained within $5\text{ hours}$ ($5 \times 3,600\text{ seconds}$). 

## Question 7
According to the networking concepts presented in the material, which device is required to connect an internal private network to an external network like the Internet?

- [x] Router
- [ ] Switch
- [ ] Hub
- [ ] Access Point (AP)

**Hint:** Think about the device responsible for routing traffic between distinct, separate network boundaries.

## Question 8
Which short-range wireless communication technology operates typically within $10\text{ meters}$ and is commonly used to connect devices like wireless earphones and AI speakers?

- [x] Bluetooth
- [ ] Wi-Fi
- [ ] NFC
- [ ] Electronic Tag (RFID)

**Hint:** Focus on the personal area network standard standardly used for low-power audio streaming over short distances.

## Question 9
What visual feedback appears on a table device's LED matrix immediately after a user presses Button A in the restaurant calling system?

- [x] A checkmark ('V') is displayed for 1 second.
- [ ] The assigned table number scrolls across the matrix.
- [ ] All 25 LEDs remain continuously lit until serviced.
- [ ] A bell icon flashes accompanied by a chime.

**Hint:** Recall the single character used to give immediate visual feedback to the customer that their button press was registered.

## Question 10
According to the micro:bit v2 hardware layout, which component is located on the FRONT face of the board?

- [x] Built-in microphone
- [ ] Radio antenna
- [ ] System speaker
- [ ] Accelerometer sensor

**Hint:** Think about which component needs to receive user sound input directly from the front user perspective.

## Question 11
When running the clapping light program in the web browser simulator without a physical micro:bit connected, what issue occurs if the sound level slider remains above $100$ continuously?

- [x] The simulator continually registers loud sound, causing the LED to repeatedly flash ON and OFF.
- [ ] The MakeCode editor crashes and automatically resets all declared variables.
- [ ] The code execution automatically switches from Block coding to Python mode.
- [ ] The virtual speaker emits an error beep and disables sound input.

**Hint:** Consider how continuous detection of sound above threshold re-triggers the state toggle logic repeatedly.

## Question 12
In the pedestrian signal light algorithm, how long after displaying 'green' does the signal device wait before starting to broadcast countdown radio signals?

- [x] $10\text{ seconds}$ ($10,000\text{ ms}$)
- [ ] $20\text{ seconds}$ ($20,000\text{ ms}$)
- [ ] $5\text{ seconds}$ ($5,000\text{ ms}$)
- [ ] $1\text{ second}$ ($1,000\text{ ms}$)

**Hint:** The signal stays green for 20 seconds total, and the countdown warns pedestrians during the last 10 seconds.
