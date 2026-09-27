import time
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# LCD configuration
lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16,
    rows=2,
    pin_rs=26,
    pin_e=19,
    pins_data=[13, 6, 5, 11],
    auto_linebreaks=False
)


def show_message(message, delay=2):
    """
    Display a message on the LCD.
    Long messages scroll from right to left.
    """
    message = message.strip()

    if not message:
        return

    # Display short messages directly
    if len(message) <= 32:
        lcd.clear()

        first_line = message[:16]
        second_line = message[16:32]

        lcd.write_string(first_line)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(second_line)

        time.sleep(delay)

    # Scroll long messages
    else:
        scroll_text = " " * 16 + message + " " * 16

        for position in range(len(scroll_text) - 15):
            lcd.clear()
            lcd.write_string(scroll_text[position:position + 16])
            time.sleep(0.3)


try:
    lcd.clear()
    lcd.write_string("Digital Notice")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Board Ready")
    time.sleep(2)

    while True:
        print("\nDigital Notice Board")
        print("1. Display a notice")
        print("2. Clear display")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            notice = input("Enter notice: ")
            show_message(notice)

        elif choice == "2":
            lcd.clear()
            print("Display cleared.")

        elif choice == "3":
            break

        else:
            print("Invalid choice.")

except KeyboardInterrupt:
    print("\nProgram stopped.")

finally:
    lcd.clear()
    GPIO.cleanup()
